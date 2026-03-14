"""
HireSense AI — Companies forms
"""
from django import forms
from .models import JobPosting, CompanyProfile


class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = (
            'title', 'department', 'skills_required', 'experience_level',
            'salary_min', 'salary_max', 'description', 'deadline'
        )
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Job Title'}),
            'department': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Department'}),
            'skills_required': forms.Textarea(attrs={'class': 'form-input', 'rows': 2, 'placeholder': 'Skills (comma-separated)'}),
            'experience_level': forms.Select(attrs={'class': 'form-input'}),
            'salary_min': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Min salary'}),
            'salary_max': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Max salary'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Job description'}),
            'deadline': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
        }


class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ('company_name', 'industry', 'location', 'website', 'about', 'logo')
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-input'}),
            'industry': forms.TextInput(attrs={'class': 'form-input'}),
            'location': forms.TextInput(attrs={'class': 'form-input'}),
            'website': forms.URLInput(attrs={'class': 'form-input'}),
            'about': forms.Textarea(attrs={'class': 'form-input', 'rows': 4}),
        }
