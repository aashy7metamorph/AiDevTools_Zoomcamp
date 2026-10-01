from django.urls import path

from . import views

urlpatterns = [
    path("", views.chore_board, name="chore_board"),
    path("members/", views.member_list, name="member_list"),
    path("chores/new/", views.chore_create, name="chore_create"),
    path("chores/<int:chore_id>/done/", views.chore_done, name="chore_done"),
]