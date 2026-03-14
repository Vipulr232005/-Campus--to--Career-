"""
HireSense AI — Students app models
"""
from django.db import models
from django.conf import settings


class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    roll_number = models.CharField(max_length=50, blank=True)
    branch = models.CharField(max_length=100, blank=True)
    year = models.IntegerField(default=1)
    semester = models.IntegerField(default=1)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.email


class Subject(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20)
    semester = models.IntegerField(default=1)
    faculty = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subjects_taught',
        limit_choices_to={'role': 'faculty'}
    )

    class Meta:
        ordering = ['semester', 'code']

    def __str__(self):
        return f'{self.code} — {self.name}'


class AttendanceRecord(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
    ]
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='attendance_records')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='present')

    class Meta:
        unique_together = ['student', 'subject', 'date']
        ordering = ['-date']

    def __str__(self):
        return f'{self.student} — {self.subject.code} — {self.date}'


class GradeRecord(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='grade_records')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='grade_records')
    semester = models.IntegerField()
    internal_marks = models.FloatField(default=0)
    external_marks = models.FloatField(default=0)

    @property
    def total(self):
        return self.internal_marks + self.external_marks

    @property
    def grade(self):
        t = self.total
        if t >= 90:
            return 'O'
        if t >= 80:
            return 'A+'
        if t >= 70:
            return 'A'
        if t >= 60:
            return 'B+'
        if t >= 50:
            return 'B'
        if t >= 40:
            return 'C'
        return 'F'

    class Meta:
        unique_together = ['student', 'subject', 'semester']
        ordering = ['semester', 'subject']

    def __str__(self):
        return f'{self.student} — {self.subject.code} — Sem {self.semester}'
