"""
Faculty: at-risk students view, alerts (consumes ML Risk Engine output)
"""
from django.conf import settings
from django.db import models
from students.models import StudentProfile


class Alert(models.Model):
    class Severity(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"
        CRITICAL = "critical", "Critical"

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="alerts")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="sent_alerts")
    severity = models.CharField(max_length=20, choices=Severity.choices, default=Severity.MEDIUM)
    message = models.TextField()
    risk_score = models.FloatField(null=True, blank=True)  # from ML Risk Engine
    acknowledged = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
