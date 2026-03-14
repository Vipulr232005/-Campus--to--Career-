"""
HireSense AI — Landing URL configuration
"""
from django.urls import path
from . import views

app_name = 'landing'

urlpatterns = [
    path('', views.index, name='index'),
]
