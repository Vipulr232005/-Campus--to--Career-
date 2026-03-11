from django.urls import path
from . import views

urlpatterns = [
    path("risk/", views.explain_risk, name="explain-my-risk"),
    path("risk/<int:student_id>/", views.explain_risk, name="explain-risk"),
    path("application/<int:application_id>/", views.explain_application_rank, name="explain-application-rank"),
]
