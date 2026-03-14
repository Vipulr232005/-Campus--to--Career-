"""
HireSense AI — Companies URL configuration
"""
from django.urls import path
from . import views

app_name = 'companies'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('post-job/', views.post_job, name='post_job'),
    path('listings/', views.listings, name='listings'),
    path('applications/', views.applications, name='applications'),
    path('applications/<int:pk>/shortlist/', views.shortlist, name='shortlist'),
    path('applications/<int:pk>/reject/', views.reject, name='reject'),
    path('ai-ranker/', views.ai_ranker, name='ai_ranker'),
]
