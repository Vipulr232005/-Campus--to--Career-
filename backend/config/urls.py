"""
Campus-to-Career — Root URL config
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

def root_view(request):
    return HttpResponse(
        "<h1>Campus-to-Career API</h1>"
        "<p>This backend is <strong>API-only</strong>. There is no web UI here.</p>"
        "<ul>"
        "<li><a href='/admin/'>Django Admin</a></li>"
        "<li>API: <code>/api/auth/</code>, <code>/api/students/</code>, <code>/api/companies/</code>, etc.</li>"
        "</ul>"
        "<p>To use the app: run the <strong>frontend</strong> (e.g. <code>cd frontend && npm run dev</code>) "
        "and open the URL it shows (e.g. http://localhost:5173).</p>"
        "<p>Or use the <strong>HireSense</strong> full-site Django project: <code>cd hiresense && python manage.py runserver</code> "
        "then open <a href='http://127.0.0.1:8000/'>http://127.0.0.1:8000/</a></p>",
        content_type="text/html",
    )

urlpatterns = [
    path("", root_view),
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
