from rest_framework import generics, permissions
from students.models import StudentProfile
from .models import Resume
from .serializers import ResumeSerializer


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "student"


class ResumeDetail(generics.RetrieveUpdateAPIView):
    serializer_class = ResumeSerializer
    permission_classes = [IsStudent]

    def get_object(self):
        profile, _ = StudentProfile.objects.get_or_create(user=self.request.user)
        resume, _ = Resume.objects.get_or_create(student=profile)
        return resume
