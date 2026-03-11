from rest_framework import generics, permissions, response
from companies.models import Job
from .services import run_screening_for_job


class IsCompany(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "company"


class RunScreeningView(generics.GenericAPIView):
    """Company: trigger ML ranking for a job's applications."""
    permission_classes = [IsCompany]

    def post(self, request, job_id):
        job = Job.objects.filter(id=job_id, posted_by=request.user).first()
        if not job:
            return response.Response({"detail": "Not found."}, status=404)
        count = run_screening_for_job(job_id)
        return response.Response({"job_id": job_id, "applications_ranked": count})
