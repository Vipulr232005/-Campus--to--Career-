from django.contrib import admin
from .models import ScreeningResult


@admin.register(ScreeningResult)
class ScreeningResultAdmin(admin.ModelAdmin):
    list_display = ("application", "match_score", "rank", "created_at")
