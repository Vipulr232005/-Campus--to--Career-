from django.contrib import admin
from .models import StudentProfile, Course, AttendanceRecord, Grade, Assignment


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "roll_number", "department", "year", "cgpa")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "department")


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "date", "present")
    list_filter = ("course", "present")


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "semester", "marks", "grade_point")


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "title", "submitted", "marks_obtained", "deadline")
