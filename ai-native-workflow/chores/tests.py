from django.test import TestCase
from django.urls import reverse

from .models import Chore, Member


class MemberModelTests(TestCase):
    def test_member_can_be_created_by_name(self):
        member = Member.objects.create(name="Alex")
        self.assertEqual(Member.objects.get(pk=member.pk).name, "Alex")


class MemberAddFlowTests(TestCase):
    def test_member_list_page_shows_add_form(self):
        response = self.client.get(reverse("member_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Add a member")

    def test_post_adds_member_and_redirects(self):
        response = self.client.post(reverse("member_list"), {"name": "Sam"})
        self.assertRedirects(response, reverse("member_list"))
        self.assertTrue(Member.objects.filter(name="Sam").exists())

    def test_saved_member_is_listed_and_available(self):
        self.client.post(reverse("member_list"), {"name": "Sam"})
        response = self.client.get(reverse("member_list"))
        self.assertContains(response, "Sam")
        self.assertEqual(list(Member.objects.values_list("name", flat=True)), ["Sam"])


class ChoreModelTests(TestCase):
    def test_new_chore_defaults_to_pending(self):
        member = Member.objects.create(name="Alex")
        chore = Chore.objects.create(title="Take out trash", assigned_to=member)
        self.assertEqual(chore.status, Chore.PENDING)


class ChoreCreateFlowTests(TestCase):
    def setUp(self):
        self.member = Member.objects.create(name="Alex")

    def test_chore_create_page_shows_form(self):
        response = self.client.get(reverse("chore_create"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create a Chore")

    def test_assignee_choices_come_from_saved_members(self):
        response = self.client.get(reverse("chore_create"))
        self.assertContains(response, "Alex")

    def test_post_creates_chore_assigned_to_existing_member(self):
        response = self.client.post(
            reverse("chore_create"),
            {"title": "Take out trash", "assigned_to": self.member.pk},
        )
        self.assertRedirects(response, reverse("chore_create"))
        chore = Chore.objects.get()
        self.assertEqual(chore.title, "Take out trash")
        self.assertEqual(chore.assigned_to, self.member)
        self.assertEqual(chore.status, Chore.PENDING)

    def test_chore_requires_an_assignment(self):
        response = self.client.post(reverse("chore_create"), {"title": "No assignee"})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Chore.objects.exists())


class ChoreBoardTests(TestCase):
    def setUp(self):
        self.alex = Member.objects.create(name="Alex")
        self.sam = Member.objects.create(name="Sam")

    def test_new_chore_appears_on_board_with_title_member_and_pending_status(self):
        self.client.post(
            reverse("chore_create"),
            {"title": "Wash dishes", "assigned_to": self.alex.pk},
        )
        response = self.client.get(reverse("chore_board"))
        self.assertContains(response, "Wash dishes")
        self.assertContains(response, "Alex")
        self.assertContains(response, "Pending")

    def test_board_shows_all_chores(self):
        Chore.objects.create(title="Wash dishes", assigned_to=self.alex)
        Chore.objects.create(title="Take out trash", assigned_to=self.sam)
        response = self.client.get(reverse("chore_board"))
        self.assertContains(response, "Wash dishes")
        self.assertContains(response, "Take out trash")
        self.assertContains(response, "Alex")
        self.assertContains(response, "Sam")

    def test_pending_and_completed_are_distinguishable(self):
        Chore.objects.create(title="Wash dishes", assigned_to=self.alex)
        Chore.objects.create(
            title="Take out trash", assigned_to=self.sam, status=Chore.COMPLETED
        )
        response = self.client.get(reverse("chore_board"))
        self.assertContains(response, "Pending")
        self.assertContains(response, "Completed")
        self.assertContains(response, "<del>Take out trash</del>", html=True)
        self.assertNotContains(response, "<del>Wash dishes</del>", html=True)

    def test_empty_board_shows_message(self):
        response = self.client.get(reverse("chore_board"))
        self.assertContains(response, "No chores yet")


class ChoreDoneTests(TestCase):
    def setUp(self):
        self.alex = Member.objects.create(name="Alex")
        self.chore = Chore.objects.create(title="Wash dishes", assigned_to=self.alex)

    def test_post_done_marks_chore_completed_and_redirects(self):
        response = self.client.post(reverse("chore_done", args=[self.chore.pk]))
        self.assertRedirects(response, reverse("chore_board"))
        self.chore.refresh_from_db()
        self.assertEqual(self.chore.status, Chore.COMPLETED)

    def test_board_shows_done_action_only_for_pending_chores(self):
        completed = Chore.objects.create(
            title="Take out trash", assigned_to=self.alex, status=Chore.COMPLETED
        )
        response = self.client.get(reverse("chore_board"))
        self.assertContains(
            response, f'action="{reverse("chore_done", args=[self.chore.pk])}"'
        )
        self.assertNotContains(
            response, f'action="{reverse("chore_done", args=[completed.pk])}"'
        )

    def test_done_requires_post(self):
        response = self.client.get(reverse("chore_done", args=[self.chore.pk]))
        self.assertRedirects(response, reverse("chore_board"))
        self.chore.refresh_from_db()
        self.assertEqual(self.chore.status, Chore.PENDING)

    def test_anonymous_client_can_complete_chore_no_auth(self):
        response = self.client.post(reverse("chore_done", args=[self.chore.pk]))
        self.assertRedirects(response, reverse("chore_board"))
        self.chore.refresh_from_db()
        self.assertEqual(self.chore.status, Chore.COMPLETED)


class ChoreFilterTests(TestCase):
    def setUp(self):
        self.alex = Member.objects.create(name="Alex")
        self.sam = Member.objects.create(name="Sam")
        self.alex_chore = Chore.objects.create(title="Wash dishes", assigned_to=self.alex)
        self.sam_chore = Chore.objects.create(title="Take out trash", assigned_to=self.sam)

    def test_no_filter_shows_all_chores(self):
        response = self.client.get(reverse("chore_board"))
        self.assertContains(response, "Wash dishes")
        self.assertContains(response, "Take out trash")

    def test_filter_shows_only_selected_member_chores(self):
        response = self.client.get(reverse("chore_board"), {"member": self.alex.pk})
        self.assertContains(response, "Wash dishes")
        self.assertNotContains(response, "Take out trash")

        response = self.client.get(reverse("chore_board"), {"member": self.sam.pk})
        self.assertContains(response, "Take out trash")
        self.assertNotContains(response, "Wash dishes")

    def test_filter_preserves_selected_member_in_ui(self):
        response = self.client.get(reverse("chore_board"), {"member": self.alex.pk})
        self.assertContains(
            response, f'<option value="{self.alex.pk}" selected>Alex</option>', html=True
        )

    def test_all_members_option_clears_filter(self):
        response = self.client.get(reverse("chore_board"))
        self.assertContains(response, '<option value="">All members</option>', html=True)