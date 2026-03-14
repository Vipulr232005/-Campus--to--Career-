"""
HireSense AI — Students app views
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import HttpResponse
from accounts.decorators import role_required
from .models import StudentProfile, Subject, AttendanceRecord, GradeRecord
from .utils import calculate_risk_score
from companies.models import JobPosting, JobApplication, CompanyProfile
from faculty.models import Announcement

try:
    import PyPDF2
    from io import BytesIO
except ImportError:
    PyPDF2 = None

from companies.utils import calculate_fit_score


def get_student_profile(user):
    return get_object_or_404(StudentProfile, user=user)


@login_required
@role_required('student')
def dashboard(request):
    profile = get_student_profile(request.user)
    score, label = calculate_risk_score(profile)
    apps = JobApplication.objects.filter(applicant=request.user)
    announcements = Announcement.objects.filter(is_active=True)[:5]

    # Attendance summary
    att = AttendanceRecord.objects.filter(student=profile)
    by_subject = att.values('subject').annotate(
        total=Count('id'),
        present=Count('id', filter=Q(status='present'))
    )
    total_held = sum(x['total'] for x in by_subject)
    total_att = sum(x['present'] for x in by_subject)
    attendance_pct = round((total_att / total_held * 100), 1) if total_held else 0

    # CGPA (average of grade totals / 100 * 10 scale simplified)
    grades = GradeRecord.objects.filter(student=profile)
    if grades.exists():
        cgpa = round(sum(g.total for g in grades) / grades.count() / 10, 2)
    else:
        cgpa = None

    return render(request, 'students/dashboard.html', {
        'profile': profile,
        'risk_score': score,
        'risk_label': label,
        'attendance_pct': attendance_pct,
        'cgpa': cgpa,
        'jobs_applied': apps.count(),
        'announcements': announcements,
    })


@login_required
@role_required('student')
def attendance(request):
    profile = get_student_profile(request.user)
    records = AttendanceRecord.objects.filter(student=profile).select_related('subject').order_by('subject__code', '-date')
    by_subject = {}
    for r in records:
        key = (r.subject_id, r.subject.code, r.subject.name)
        if key not in by_subject:
            by_subject[key] = {'held': 0, 'attended': 0}
        by_subject[key]['held'] += 1
        if r.status == 'present':
            by_subject[key]['attended'] += 1
    rows = []
    total_held = total_att = 0
    for (_, code, name), v in sorted(by_subject.items(), key=lambda x: x[0][1]):
        pct = round((v['attended'] / v['held'] * 100), 1) if v['held'] else 0
        total_held += v['held']
        total_att += v['attended']
        rows.append({'subject': name, 'code': code, 'held': v['held'], 'attended': v['attended'], 'pct': pct})
    overall = round((total_att / total_held * 100), 1) if total_held else 0
    return render(request, 'students/attendance.html', {'rows': rows, 'overall': overall})


@login_required
@role_required('student')
def grades(request):
    profile = get_student_profile(request.user)
    semester = request.GET.get('semester')
    qs = GradeRecord.objects.filter(student=profile).select_related('subject').order_by('semester', 'subject__code')
    if semester:
        qs = qs.filter(semester=int(semester))
    grades_list = list(qs)
    if grades_list:
        cgpa = round(sum(g.total for g in grades_list) / len(grades_list) / 10, 2)
    else:
        cgpa = None
    semesters = list(GradeRecord.objects.filter(student=profile).values_list('semester', flat=True).distinct().order_by('semester'))
    return render(request, 'students/grades.html', {'grades': grades_list, 'cgpa': cgpa, 'semesters': semesters, 'selected_semester': semester})


@login_required
@role_required('student')
def risk_score(request):
    profile = get_student_profile(request.user)
    score, label = calculate_risk_score(profile)
    return render(request, 'students/risk_score.html', {'profile': profile, 'risk_score': score, 'risk_label': label})


@login_required
@role_required('student')
def job_board(request):
    profile = get_student_profile(request.user)
    jobs = JobPosting.objects.filter(is_active=True).select_related('company').order_by('-created_at')
    role_filter = request.GET.get('role')
    skills_filter = request.GET.get('skills')
    if role_filter:
        jobs = jobs.filter(title__icontains=role_filter)
    if skills_filter:
        jobs = jobs.filter(skills_required__icontains=skills_filter)
    applied_ids = set(JobApplication.objects.filter(applicant=request.user).values_list('job_id', flat=True))
    return render(request, 'students/job_board.html', {'jobs': jobs, 'applied_ids': applied_ids})


@login_required
@role_required('student')
def apply_job(request, pk):
    job = get_object_or_404(JobPosting, pk=pk, is_active=True)
    profile = get_student_profile(request.user)
    if JobApplication.objects.filter(job=job, applicant=request.user).exists():
        return redirect('students:job_board')
    resume_text = ''
    if profile.resume and PyPDF2:
        try:
            with open(profile.resume.path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    resume_text += page.extract_text() or ''
        except Exception:
            resume_text = (profile.user.get_full_name() or '') + ' ' + (profile.branch or '')
    else:
        resume_text = (profile.user.get_full_name() or '') + ' ' + (profile.branch or '') + ' ' + (profile.roll_number or '')
    jd_text = job.description or '' + ' ' + (job.skills_required or '')
    score, matched, missing = calculate_fit_score(resume_text, jd_text)
    JobApplication.objects.create(
        job=job,
        applicant=request.user,
        ai_fit_score=score,
        matched_skills=', '.join(matched[:20]),
        missing_skills=', '.join(missing[:20]),
    )
    return redirect('students:job_board')


@login_required
@role_required('student')
def announcements(request):
    announcements_list = Announcement.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'students/announcements.html', {'announcements': announcements_list})
