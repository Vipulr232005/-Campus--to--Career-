"""
HireSense AI — Faculty app views
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from accounts.decorators import role_required
from .models import FacultyProfile, Announcement
from .forms import AnnouncementForm, PostResultsForm, ManageAttendanceForm
from .utils import get_at_risk_students
from students.models import StudentProfile, Subject, AttendanceRecord, GradeRecord
from students.utils import calculate_risk_score


@login_required
@role_required('faculty')
def dashboard(request):
    at_risk = get_at_risk_students(request.user)
    announcements_count = Announcement.objects.filter(posted_by=request.user).count()
    students = StudentProfile.objects.all()
    att_data = []
    for s in students:
        recs = AttendanceRecord.objects.filter(student=s)
        total = recs.values('subject', 'date').distinct().count()
        present = recs.filter(status='present').values('subject', 'date').distinct().count()
        pct = (present / total * 100) if total else 0
        att_data.append(pct)
    avg_att = round(sum(att_data) / len(att_data), 1) if att_data else 0
    return render(request, 'faculty/dashboard.html', {
        'total_students': students.count(),
        'at_risk_count': len(at_risk),
        'announcements_count': announcements_count,
        'avg_attendance': avg_att,
    })


@login_required
@role_required('faculty')
def students_list(request):
    qs = StudentProfile.objects.select_related('user').all().order_by('user__first_name')
    search = request.GET.get('q')
    if search:
        qs = qs.filter(
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(roll_number__icontains=search)
        )
    students_with_risk = []
    for s in qs:
        score, label = calculate_risk_score(s)
        recs = AttendanceRecord.objects.filter(student=s)
        total = recs.values('subject', 'date').distinct().count()
        present = recs.filter(status='present').values('subject', 'date').distinct().count()
        att_pct = round((present / total * 100), 1) if total else 0
        grades = GradeRecord.objects.filter(student=s)
        cgpa = round(sum(g.total for g in grades) / grades.count() / 10, 2) if grades.exists() else None
        students_with_risk.append((s, score, label, att_pct, cgpa))
    return render(request, 'faculty/students_list.html', {'students_with_risk': students_with_risk})


@login_required
@role_required('faculty')
def at_risk(request):
    at_risk_list = get_at_risk_students(request.user)
    return render(request, 'faculty/at_risk.html', {'at_risk_list': at_risk_list})


@login_required
@role_required('faculty')
def post_results(request):
    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        semester = request.POST.get('semester')
        subject = get_object_or_404(Subject, pk=subject_id)
        for key, val in request.POST.items():
            if key.startswith('internal_') and val != '':
                sid = key.replace('internal_', '')
                try:
                    student = StudentProfile.objects.get(pk=sid)
                    internal = float(val)
                    external = float(request.POST.get(f'external_{sid}', 0) or 0)
                    GradeRecord.objects.update_or_create(
                        student=student, subject=subject, semester=int(semester),
                        defaults={'internal_marks': internal, 'external_marks': external}
                    )
                except (ValueError, StudentProfile.DoesNotExist):
                    pass
        return redirect('faculty:post_results')
    form = PostResultsForm()
    students = StudentProfile.objects.select_related('user').all().order_by('user__first_name')
    return render(request, 'faculty/post_results.html', {'form': form, 'students': students})


@login_required
@role_required('faculty')
def post_announcement(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            ann = form.save(commit=False)
            ann.posted_by = request.user
            ann.save()
            return redirect('faculty:announcement_list')
    else:
        form = AnnouncementForm()
    return render(request, 'faculty/post_announcement.html', {'form': form})


@login_required
@role_required('faculty')
def announcement_list(request):
    announcements = Announcement.objects.filter(posted_by=request.user).order_by('-created_at')
    return render(request, 'faculty/announcement_list.html', {'announcements': announcements})


@login_required
@role_required('faculty')
def announcement_delete(request, pk):
    ann = get_object_or_404(Announcement, pk=pk, posted_by=request.user)
    ann.delete()
    return redirect('faculty:announcement_list')


@login_required
@role_required('faculty')
def manage_attendance(request):
    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        date_str = request.POST.get('date')
        subject = get_object_or_404(Subject, pk=subject_id)
        from datetime import datetime
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        for key, val in request.POST.items():
            if key.startswith('status_') and val in ('present', 'absent'):
                sid = key.replace('status_', '')
                try:
                    student = StudentProfile.objects.get(pk=sid)
                    AttendanceRecord.objects.update_or_create(
                        student=student, subject=subject, date=date,
                        defaults={'status': val}
                    )
                except StudentProfile.DoesNotExist:
                    pass
        return redirect('faculty:manage_attendance')
    form = ManageAttendanceForm()
    students = StudentProfile.objects.select_related('user').all().order_by('user__first_name')
    return render(request, 'faculty/manage_attendance.html', {'form': form, 'students': students})
