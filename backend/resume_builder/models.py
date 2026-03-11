"""
Resume builder: students build ATS-friendly resumes from profile data
"""
from django.conf import settings
from django.db import models
from students.models import StudentProfile


class Resume(models.Model):
    student = models.OneToOneField(StudentProfile, on_delete=models.CASCADE, related_name="resume")
    headline = models.CharField(max_length=200, blank=True)
    summary = models.TextField(blank=True)
    skills = models.JSONField(default=list)  # ["Python", "Django", ...]
    education_json = models.JSONField(default=list)  # [{institution, degree, year, ...}]
    experience_json = models.JSONField(default=list)  # [{company, role, duration, ...}]
    projects_json = models.JSONField(default=list)   # [{title, description, ...}]
    raw_text = models.TextField(blank=True)  # flattened text for screener
    pdf_file = models.FileField(upload_to="resumes/%Y/%m/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Resume — {self.student.user.get_username()}"
