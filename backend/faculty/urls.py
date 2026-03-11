from django.urls import path
from . import views

urlpatterns = [
    path("at-risk/", views.AtRiskStudentsList.as_view(), name="at-risk-students"),
    path("alerts/", views.AlertListCreate.as_view(), name="alerts"),
]
