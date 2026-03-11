from rest_framework import serializers
from .models import Resume


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ("id", "student", "headline", "summary", "skills", "education_json", "experience_json", "projects_json", "raw_text", "pdf_file", "created_at", "updated_at")
        read_only_fields = ("student", "raw_text", "created_at", "updated_at")
