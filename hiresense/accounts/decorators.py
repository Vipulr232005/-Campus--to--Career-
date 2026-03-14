"""
HireSense AI — Role-based access decorators
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth import REDIRECT_FIELD_NAME


def role_required(role):
    """Require user to be authenticated and have the given role."""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                from django.conf import settings
                from django.contrib.auth.views import redirect_to_login
                return redirect_to_login(request.get_full_path(), settings.LOGIN_URL, REDIRECT_FIELD_NAME)
            if request.user.role != role:
                return redirect(request.user.get_dashboard_url())
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
