"""
User model with 3 roles: Student, Faculty, Company
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = "student", "Student"
        FACULTY = "faculty", "Faculty"
        COMPANY = "company", "Company"

    role = models.CharField(max_length=20, choices=Role.choices)
    phone = models.CharField(max_length=15, blank=True)
    # Company-specific
    company_name = models.CharField(max_length=255, blank=True)
    # Faculty-specific (optional: link to department)
    department = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.get_username()} ({self.get_role_display()})"

    def get_role_display(self):
        return dict(self.Role.choices).get(self.role, self.role)
