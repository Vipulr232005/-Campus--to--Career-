"""
Resume Screener: stores job–resume match scores and rank (NLP + ML)
"""
from django.db import models
from companies.models import Job, Application
from resume_builder.models import Resume


class ScreeningResult(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name="screening_result")
    match_score = models.FloatField()
    rank = models.PositiveIntegerField()
    # Top matching keywords/features (for explainability)
    matched_keywords = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-match_score"]
