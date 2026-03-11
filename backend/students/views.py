from rest_framework import generics, permissions
from rest_framework.decorators import permission_classes
from .models import StudentProfile, Course, AttendanceRecord, Grade, Assignment
from .serializers import (
    StudentProfileSerializer,
    CourseSerializer,
    AttendanceRecordSerializer,
    GradeSerializer,
    AssignmentSerializer,
)


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "student"


class StudentProfileDetail(generics.RetrieveUpdateAPIView):
    serializer_class = StudentProfileSerializer
    permission_classes = [IsStudent]

    def get_object(self):
        profile, _ = StudentProfile.objects.get_or_create(user=self.request.user)
        return profile


class CourseList(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]


class MyAttendanceList(generics.ListAPIView):
    serializer_class = AttendanceRecordSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        profile, _ = StudentProfile.objects.get_or_create(user=self.request.user)
        return AttendanceRecord.objects.filter(student=profile).select_related("course")


class MyGradesList(generics.ListAPIView):
    serializer_class = GradeSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        profile, _ = StudentProfile.objects.get_or_create(user=self.request.user)
        return Grade.objects.filter(student=profile).select_related("course")


class MyAssignmentsList(generics.ListAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        profile, _ = StudentProfile.objects.get_or_create(user=self.request.user)
        return Assignment.objects.filter(student=profile).select_related("course")
