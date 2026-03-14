"""
HireSense AI — Accounts views: login, register, logout, profile
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import CustomUser
from .forms import RegisterForm, LoginForm, ProfileForm
from students.models import StudentProfile
from faculty.models import FacultyProfile
from companies.models import CompanyProfile


@require_http_methods(['GET', 'POST'])
def login_view(request):
    if request.user.is_authenticated:
        return redirect(request.user.get_dashboard_url())
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(user.get_dashboard_url())
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


@require_http_methods(['GET', 'POST'])
def register_view(request):
    if request.user.is_authenticated:
        return redirect(request.user.get_dashboard_url())
    role = request.GET.get('role', 'student')
    if request.method == 'POST':
        role = request.POST.get('role', role)
        form = RegisterForm(request.POST, role=role)
        if form.is_valid():
            user = form.save()
            if user.role == 'student':
                StudentProfile.objects.get_or_create(user=user, defaults={'roll_number': '', 'branch': '', 'year': 1, 'semester': 1})
            elif user.role == 'faculty':
                FacultyProfile.objects.get_or_create(user=user, defaults={'department': '', 'employee_id': ''})
            elif user.role == 'company':
                CompanyProfile.objects.get_or_create(user=user, defaults={'company_name': user.get_full_name() or user.email, 'industry': '', 'location': '', 'website': '', 'about': ''})
            login(request, user)
            return redirect(user.get_dashboard_url())
    else:
        form = RegisterForm(role=role)
    return render(request, 'accounts/register.html', {'form': form, 'role': role})


@require_http_methods(['GET', 'POST'])
def logout_view(request):
    logout(request)
    return redirect('landing:index')


@login_required
@require_http_methods(['GET', 'POST'])
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})
