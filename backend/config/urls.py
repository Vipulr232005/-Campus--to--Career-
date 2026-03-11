"""
Campus-to-Career — Root URL config
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("users.urls")),
    path("api/students/", include("students.urls")),
    path("api/faculty/", include("faculty.urls")),
    path("api/companies/", include("companies.urls")),
    path("api/resume-builder/", include("resume_builder.urls")),
    path("api/risk/", include("ml_risk_engine.urls")),
    path("api/screener/", include("resume_screener.urls")),
    path("api/explain/", include("explainability.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
