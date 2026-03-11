from rest_framework import serializers
from .models import Job, Application
from students.serializers import StudentProfileSerializer


class JobSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source="posted_by.company_name", read_only=True)

    class Meta:
        model = Job
        fields = ("id", "posted_by", "company_name", "title", "description", "requirements", "job_type", "location",
                  "salary_min", "salary_max", "is_active", "created_at", "updated_at")


class ApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source="job.title", read_only=True)
    applicant_detail = StudentProfileSerializer(source="applicant", read_only=True)

    class Meta:
        model = Application
        fields = ("id", "job", "job_title", "applicant", "applicant_detail", "status", "match_score", "rank", "applied_at")
        read_only_fields = ("applicant", "status", "match_score", "rank", "applied_at")
