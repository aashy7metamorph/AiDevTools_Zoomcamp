from django.db import models


class Member(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Chore(models.Model):
    PENDING = "pending"
    COMPLETED = "completed"
    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (COMPLETED, "Completed"),
    ]

    title = models.CharField(max_length=200)
    assigned_to = models.ForeignKey(Member, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return self.title