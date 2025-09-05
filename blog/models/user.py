from django.db import models
from django.contrib.auth.models import AbstractUser
from base.models import BaseModel


class User(AbstractUser, BaseModel):
    USER_ADMIN = "A"
    USER_VIEWER = "V"
    USER_WRITER = "W"

    USER_ROLE_CHOICES = [
        (USER_ADMIN, "admin"),
        (USER_VIEWER, "viewer"),
        (USER_WRITER, "writer"),
    ]
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    user_role = models.CharField(
        max_length=1, choices=USER_ROLE_CHOICES, default=USER_VIEWER
    )

    class Meta:
        permissions = [
            ("view_user_list", "Can view user list"),
            ("edit_user", "Can edit user"),
        ]
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

