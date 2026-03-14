"""
HireSense AI — Faculty URL configuration
"""
from django.urls import path
from . import views

app_name = 'faculty'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('students/', views.students_list, name='students_list'),
    path('at-risk/', views.at_risk, name='at_risk'),
    path('post-results/', views.post_results, name='post_results'),
    path('announcement/post/', views.post_announcement, name='post_announcement'),
    path('announcement/list/', views.announcement_list, name='announcement_list'),
    path('announcement/<int:pk>/delete/', views.announcement_delete, name='announcement_delete'),
    path('attendance/', views.manage_attendance, name='manage_attendance'),
]
