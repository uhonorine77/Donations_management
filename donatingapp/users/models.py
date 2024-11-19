from django.contrib.auth.models import AbstractUser # type: ignore
from django.db import models # type: ignore
class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('donor', 'Donor'),
        ('user', 'User'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    def __str__(self):
        return f"{self.username}"
    class Meta:
        db_table = "users"