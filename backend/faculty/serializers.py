from rest_framework import serializers
from .models import Alert
from students.serializers import StudentProfileSerializer


class AlertSerializer(serializers.ModelSerializer):
    student_detail = StudentProfileSerializer(source="student", read_only=True)

    class Meta:
        model = Alert
        fields = ("id", "student", "student_detail", "severity", "message", "risk_score", "acknowledged", "created_at", "created_by")
        read_only_fields = ("created_by", "created_at")
