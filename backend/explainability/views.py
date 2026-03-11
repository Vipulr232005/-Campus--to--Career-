from rest_framework import permissions, response
from rest_framework.decorators import api_view, permission_classes
from students.models import StudentProfile
from ml_risk_engine.services import predict_risk
from .services import explain_risk_with_shap, explain_ranking_with_shap
from resume_screener.models import ScreeningResult
from companies.models import Application


class IsFaculty(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "faculty"


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "student"


class IsCompany(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "company"


@api_view(["GET"])
@permission_classes([IsFaculty | IsStudent])
def explain_risk(request, student_id=None):
    """Explain why a student has a given dropout risk (for faculty or own profile)."""
    if student_id is None:
        if request.user.role != "student":
            return response.Response({"detail": "Supply student_id for faculty."}, status=400)
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    elif request.user.role == "faculty":
        profile = StudentProfile.objects.filter(id=student_id).first()
        if not profile:
            return response.Response({"detail": "Not found."}, status=404)
    else:
        return response.Response({"detail": "Not allowed."}, status=403)
    risk_score, risk_label, features = predict_risk(profile)
    explanation = explain_risk_with_shap(features, risk_score)
    explanation["risk_label"] = risk_label
    explanation["student_id"] = profile.id
    return response.Response(explanation)


@api_view(["GET"])
@permission_classes([IsCompany])
def explain_application_rank(request, application_id):
    """Explain why an application was ranked (matched keywords, etc.)."""
    app = Application.objects.filter(id=application_id, job__posted_by=request.user).select_related("job").first()
    if not app:
        return response.Response({"detail": "Not found."}, status=404)
    screening = getattr(app, "screening_result", None)
    if not screening:
        return response.Response({
            "application_id": application_id,
            "message": "Screening not run yet. Run screening on the job first.",
        })
    explanation = explain_ranking_with_shap(
        screening.matched_keywords,
        app.match_score or 0,
        app.job.title,
    )
    explanation["application_id"] = application_id
    explanation["applicant_id"] = app.applicant_id
    return response.Response(explanation)
