"""
HireSense AI — Companies app models
"""
from django.db import models
from django.conf import settings


class CompanyProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='company_profile')
    company_name = models.CharField(max_length=200)
    industry = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=200, blank=True)
    website = models.URLField(blank=True)
    about = models.TextField(blank=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)

    def __str__(self):
        return self.company_name


class JobPosting(models.Model):
    EXPERIENCE_CHOICES = [
        ('fresher', 'Fresher'),
        ('junior', 'Junior'),
        ('mid', 'Mid'),
        ('senior', 'Senior'),
    ]
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='job_postings')
    title = models.CharField(max_length=200)
    department = models.CharField(max_length=100, blank=True)
    skills_required = models.TextField(help_text='Comma-separated skills')
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='fresher')
    salary_min = models.IntegerField(null=True, blank=True)
    salary_max = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    deadline = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.company.company_name} — {self.title}'


class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
    ]
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='job_applications')
    applied_at = models.DateTimeField(auto_now_add=True)
    resume_snapshot = models.FileField(upload_to='application_resumes/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    ai_fit_score = models.FloatField(default=0)
    matched_skills = models.TextField(blank=True)
    missing_skills = models.TextField(blank=True)

    class Meta:
        unique_together = ['job', 'applicant']
        ordering = ['-applied_at']

    def __str__(self):
        return f'{self.applicant.email} → {self.job.title}'
