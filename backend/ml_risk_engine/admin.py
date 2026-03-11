from django.contrib import admin
from .models import RiskPrediction


@admin.register(RiskPrediction)
class RiskPredictionAdmin(admin.ModelAdmin):
    list_display = ("student", "risk_score", "risk_label", "created_at")
    list_filter = ("risk_label",)
