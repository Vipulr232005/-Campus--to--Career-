from rest_framework import serializers
from .models import StudentProfile, Course, AttendanceRecord, Grade, Assignment


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class StudentProfileSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = StudentProfile
        fields = ("id", "user", "user_email", "user_name", "roll_number", "department", "year", "cgpa", "created_at", "updated_at")

    def get_user_name(self, obj):
        return obj.user.get_full_name() or obj.user.username


class AttendanceRecordSerializer(serializers.ModelSerializer):
    course_code = serializers.CharField(source="course.code", read_only=True)

    class Meta:
        model = AttendanceRecord
        fields = ("id", "student", "course", "course_code", "date", "present", "created_at")


class GradeSerializer(serializers.ModelSerializer):
    course_code = serializers.CharField(source="course.code", read_only=True)

    class Meta:
        model = Grade
        fields = ("id", "student", "course", "course_code", "semester", "marks", "grade_point", "created_at")


class AssignmentSerializer(serializers.ModelSerializer):
    course_code = serializers.CharField(source="course.code", read_only=True)

    class Meta:
        model = Assignment
        fields = "__all__"
