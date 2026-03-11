from django.urls import path
from . import views

urlpatterns = [
    path("my-risk/", views.MyRiskView.as_view(), name="my-risk"),
    path("at-risk/", views.AtRiskListView.as_view(), name="at-risk-list"),
    path("student/<int:student_id>/", views.risk_for_student, name="risk-for-student"),
]
