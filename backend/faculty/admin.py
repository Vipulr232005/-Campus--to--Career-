from django.contrib import admin
from .models import Alert


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ("student", "severity", "risk_score", "acknowledged", "created_at")
