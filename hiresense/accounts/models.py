"""
HireSense AI — Accounts app models
CustomUser with role (student / faculty / company)
"""
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('company', 'Company'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    phone = models.CharField(max_length=20, blank=True)
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    college = models.CharField(max_length=200, blank=True)
    is_profile_complete = models.BooleanField(default=False)

    def get_dashboard_url(self):
        if self.role == 'student':
            return '/student/dashboard/'
        if self.role == 'faculty':
            return '/faculty/dashboard/'
        if self.role == 'company':
            return '/company/dashboard/'
        return '/'
