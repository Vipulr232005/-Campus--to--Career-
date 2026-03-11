from rest_framework import generics, permissions
from students.models import StudentProfile
from .models import Job, Application
from .serializers import JobSerializer, ApplicationSerializer


class IsCompany(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "company"


class JobListCreate(generics.ListCreateAPIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self.request.user, "role", None) == "company":
            return Job.objects.filter(posted_by=self.request.user).order_by("-created_at")
        return Job.objects.filter(is_active=True).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)


class JobDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]


class ApplicationList(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsCompany]

    def get_queryset(self):
        job_id = self.kwargs.get("job_id")
        return Application.objects.filter(job_id=job_id).select_related("applicant", "applicant__user", "job").order_by("-match_score", "-applied_at")


class ApplicationCreate(generics.CreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        profile, _ = StudentProfile.objects.get_or_create(user=self.request.user)
        serializer.save(applicant=profile)
