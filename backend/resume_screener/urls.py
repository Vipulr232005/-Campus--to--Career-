from django.urls import path
from . import views

urlpatterns = [
    path("job/<int:job_id>/run/", views.RunScreeningView.as_view(), name="run-screening"),
]
