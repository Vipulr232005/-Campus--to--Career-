from django.urls import path
from . import views

urlpatterns = [
    path("", views.ResumeDetail.as_view(), name="resume-detail"),
]
