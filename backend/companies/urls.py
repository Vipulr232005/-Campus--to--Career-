from django.urls import path
from . import views

urlpatterns = [
    path("jobs/", views.JobListCreate.as_view(), name="job-list"),
    path("jobs/<int:pk>/", views.JobDetail.as_view(), name="job-detail"),
    path("jobs/<int:job_id>/applications/", views.ApplicationList.as_view(), name="application-list"),
    path("applications/", views.ApplicationCreate.as_view(), name="application-create"),
]
