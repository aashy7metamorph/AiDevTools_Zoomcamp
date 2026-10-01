from django.shortcuts import get_object_or_404, redirect, render

from .forms import ChoreForm, MemberForm
from .models import Chore, Member


def member_list(request):
    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("member_list")
    else:
        form = MemberForm()

    members = Member.objects.all()
    return render(request, "chores/member_list.html", {"members": members, "form": form})


def chore_create(request):
    if request.method == "POST":
        form = ChoreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("chore_create")
    else:
        form = ChoreForm()

    return render(request, "chores/chore_create.html", {"form": form})


def chore_board(request):
    chores = Chore.objects.order_by("pk")
    members = Member.objects.all()

    selected_member = None
    member_id = request.GET.get("member")
    if member_id:
        selected_member = get_object_or_404(Member, pk=member_id)
        chores = chores.filter(assigned_to=selected_member)

    return render(
        request,
        "chores/chore_board.html",
        {"chores": chores, "members": members, "selected_member": selected_member},
    )


def chore_done(request, chore_id):
    if request.method != "POST":
        return redirect("chore_board")
    chore = get_object_or_404(Chore, pk=chore_id)
    chore.status = Chore.COMPLETED
    chore.save()
    return redirect("chore_board")