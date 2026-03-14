"""
HireSense AI — Students URL configuration
"""
from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('attendance/', views.attendance, name='attendance'),
    path('grades/', views.grades, name='grades'),
    path('risk-score/', views.risk_score, name='risk_score'),
    path('jobs/', views.job_board, name='job_board'),
    path('jobs/<int:pk>/apply/', views.apply_job, name='apply_job'),
    path('announcements/', views.announcements, name='announcements'),
]
