from rest_framework import generics, permissions, response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import serializers
from students.models import StudentProfile
from students.serializers import StudentProfileSerializer
from .models import RiskPrediction
from .services import get_student_features, predict_risk


class AtRiskStudentSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)
    user_name = serializers.SerializerMethodField()
    latest_risk = serializers.FloatField(read_only=True)

    class Meta:
        model = StudentProfile
        fields = ("id", "user", "user_email", "user_name", "roll_number", "department", "year", "cgpa", "latest_risk")

    def get_user_name(self, obj):
        return obj.user.get_full_name() or obj.user.username


class IsFaculty(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "faculty"


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "student"


class MyRiskView(generics.GenericAPIView):
    """Student: get my own dropout risk and features."""
    permission_classes = [IsStudent]

    def get(self, request):
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        risk_score, risk_label, features = predict_risk(profile)
        RiskPrediction.objects.create(student=profile, risk_score=risk_score, risk_label=risk_label, features_json=features)
        return response.Response({
            "risk_score": risk_score,
            "risk_label": risk_label,
            "features": features,
        })


class AtRiskListView(generics.ListAPIView):
    """Faculty: list students with latest risk score (at-risk first)."""
    permission_classes = [IsFaculty]
    serializer_class = AtRiskStudentSerializer

    def get_queryset(self):
        from django.db.models import OuterRef, Subquery
        latest = RiskPrediction.objects.filter(student=OuterRef("pk")).order_by("-created_at")
        return StudentProfile.objects.annotate(
            latest_risk=Subquery(latest.values("risk_score")[:1])
        ).order_by("-latest_risk").select_related("user")


@api_view(["GET"])
@permission_classes([IsFaculty])
def risk_for_student(request, student_id):
    """Faculty: get risk and features for a specific student."""
    profile = StudentProfile.objects.filter(id=student_id).first()
    if not profile:
        return response.Response({"detail": "Not found."}, status=404)
    risk_score, risk_label, features = predict_risk(profile)
    return response.Response({
        "student_id": profile.id,
        "risk_score": risk_score,
        "risk_label": risk_label,
        "features": features,
    })
