"""
HireSense AI — Faculty forms
"""
from django import forms
from .models import Announcement
from students.models import Subject, StudentProfile, GradeRecord, AttendanceRecord


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ('title', 'description', 'category')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Title'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Description'}),
            'category': forms.Select(attrs={'class': 'form-input'}),
        }


class PostResultsForm(forms.Form):
    subject = forms.ModelChoiceField(queryset=Subject.objects.none(), widget=forms.Select(attrs={'class': 'form-input'}))
    semester = forms.IntegerField(min_value=1, max_value=10, widget=forms.NumberInput(attrs={'class': 'form-input'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].queryset = Subject.objects.all().order_by('code')


class GradeEntryForm(forms.Form):
    """One row: student, internal, external."""
    student_id = forms.IntegerField(widget=forms.HiddenInput())
    internal_marks = forms.FloatField(min_value=0, max_value=100, required=False, widget=forms.NumberInput(attrs={'class': 'form-input', 'step': '0.5'}))
    external_marks = forms.FloatField(min_value=0, max_value=100, required=False, widget=forms.NumberInput(attrs={'class': 'form-input', 'step': '0.5'}))


class ManageAttendanceForm(forms.Form):
    subject = forms.ModelChoiceField(queryset=Subject.objects.none(), widget=forms.Select(attrs={'class': 'form-input'}))
    date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].queryset = Subject.objects.all().order_by('code')
