from rest_framework import generics, permissions
from students.models import StudentProfile
from students.serializers import StudentProfileSerializer
from .models import Alert
from .serializers import AlertSerializer


class IsFaculty(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "faculty"


class AtRiskStudentsList(generics.ListAPIView):
    """List students with risk scores (from ML Risk Engine). Faculty only."""
    permission_classes = [IsFaculty]
    serializer_class = StudentProfileSerializer

    def get_queryset(self):
        # In real impl: join with risk scores from ml_risk_engine
        return StudentProfile.objects.all().select_related("user").order_by("-updated_at")[:100]


class AlertListCreate(generics.ListCreateAPIView):
    serializer_class = AlertSerializer
    permission_classes = [IsFaculty]

    def get_queryset(self):
        return Alert.objects.filter(created_by=self.request.user).select_related("student", "student__user").order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
