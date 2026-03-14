"""
HireSense AI — Companies app views
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from .models import CompanyProfile, JobPosting, JobApplication
from .forms import JobPostingForm


def get_company(request):
    return get_object_or_404(CompanyProfile, user=request.user)


@login_required
@role_required('company')
def dashboard(request):
    company = get_company(request)
    jobs = JobPosting.objects.filter(company=company)
    apps = JobApplication.objects.filter(job__company=company)
    shortlisted = apps.filter(status='shortlisted').count()
    pending = apps.filter(status='pending').count()
    return render(request, 'companies/dashboard.html', {
        'company': company,
        'jobs_count': jobs.count(),
        'applications_count': apps.count(),
        'shortlisted': shortlisted,
        'pending': pending,
    })


@login_required
@role_required('company')
def post_job(request):
    company = get_company(request)
    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = company
            job.save()
            return redirect('companies:listings')
    else:
        form = JobPostingForm()
    return render(request, 'companies/post_job.html', {'form': form})


@login_required
@role_required('company')
def listings(request):
    company = get_company(request)
    jobs = JobPosting.objects.filter(company=company).order_by('-created_at')
    return render(request, 'companies/job_listings.html', {'jobs': jobs})


@login_required
@role_required('company')
def applications(request):
    company = get_company(request)
    job_id = request.GET.get('job')
    jobs = JobPosting.objects.filter(company=company).order_by('-created_at')
    applications_list = []
    selected_job = None
    if job_id:
        selected_job = get_object_or_404(JobPosting, pk=job_id, company=company)
        applications_list = JobApplication.objects.filter(job=selected_job).select_related('applicant').order_by('-ai_fit_score')
    return render(request, 'companies/applications.html', {
        'jobs': jobs,
        'applications': applications_list,
        'selected_job': selected_job,
    })


@login_required
@role_required('company')
def shortlist(request, pk):
    if request.method != 'POST':
        return redirect('companies:applications')
    app = get_object_or_404(JobApplication, pk=pk, job__company=get_company(request))
    app.status = 'shortlisted'
    app.save()
    return redirect(reverse('companies:applications') + '?job=' + str(app.job_id))


@login_required
@role_required('company')
def reject(request, pk):
    if request.method != 'POST':
        return redirect('companies:applications')
    app = get_object_or_404(JobApplication, pk=pk, job__company=get_company(request))
    app.status = 'rejected'
    app.save()
    return redirect(reverse('companies:applications') + '?job=' + str(app.job_id))


@login_required
@role_required('company')
def ai_ranker(request):
    company = get_company(request)
    job_id = request.GET.get('job')
    jobs = JobPosting.objects.filter(company=company).order_by('-created_at')
    applications_list = []
    selected_job = None
    if job_id:
        selected_job = get_object_or_404(JobPosting, pk=job_id, company=company)
        applications_list = JobApplication.objects.filter(job=selected_job).select_related('applicant').order_by('-ai_fit_score')
    return render(request, 'companies/ai_ranker.html', {
        'jobs': jobs,
        'applications': applications_list,
        'selected_job': selected_job,
    })
