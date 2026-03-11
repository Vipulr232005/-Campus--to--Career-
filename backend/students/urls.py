from django.urls import path
from . import views

urlpatterns = [
    path("profile/", views.StudentProfileDetail.as_view(), name="student-profile"),
    path("courses/", views.CourseList.as_view(), name="course-list"),
    path("attendance/", views.MyAttendanceList.as_view(), name="my-attendance"),
    path("grades/", views.MyGradesList.as_view(), name="my-grades"),
    path("assignments/", views.MyAssignmentsList.as_view(), name="my-assignments"),
]
