"""
ML Risk Engine: stores predicted dropout risk per student (from scikit-learn pipeline)
"""
from django.conf import settings
from django.db import models
from students.models import StudentProfile


class RiskPrediction(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="risk_predictions")
    risk_score = models.FloatField()  # 0–1, higher = more at-risk
    risk_label = models.CharField(max_length=20, blank=True)  # e.g. "low", "medium", "high"
    # Features used (for explainability)
    features_json = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = "created_at"
