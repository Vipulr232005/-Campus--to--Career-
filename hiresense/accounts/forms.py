"""
HireSense AI — Accounts forms
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email'}))
    first_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First name'}))
    last_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Last name'}))
    phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone'}))
    college = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'College'}))

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'phone', 'college', 'role', 'password1', 'password2')
        widgets = {
            'password1': forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Confirm password'}),
        }

    def __init__(self, *args, role='student', **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'] = forms.ChoiceField(
            choices=CustomUser.ROLE_CHOICES,
            initial=role,
            widget=forms.HiddenInput()
        )
        self.initial['role'] = role
        self.fields['email'].label = ''
        self.fields['first_name'].label = ''
        self.fields['last_name'].label = ''
        self.fields['phone'].label = ''
        self.fields['college'].label = ''
        self.fields['password1'].label = ''
        self.fields['password2'].label = ''

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email
        user.role = self.cleaned_data.get('role', 'student')
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Password'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = ''
        self.fields['password'].label = ''


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone', 'college', 'profile_photo')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
            'college': forms.TextInput(attrs={'class': 'form-input'}),
        }
