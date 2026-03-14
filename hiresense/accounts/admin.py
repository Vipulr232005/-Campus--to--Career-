from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role',)
    ordering = ('email',)
    fieldsets = BaseUserAdmin.fieldsets + (('HireSense', {'fields': ('role', 'phone', 'college', 'profile_photo', 'is_profile_complete')}),)
