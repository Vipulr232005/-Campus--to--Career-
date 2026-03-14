"""
HireSense AI — Student risk score calculation
"""


def calculate_risk_score(student_profile):
    """
    risk = 100 - ((attendance_pct * 0.4) + (grade_avg * 0.4) + (assignments_pct * 0.2))
    Returns (score 0-100, label 'Low'|'Medium'|'High')
    """
    from .models import AttendanceRecord, GradeRecord

    # Attendance %: distinct (subject, date) present / total
    att = AttendanceRecord.objects.filter(student=student_profile)
    total_classes = att.values('subject', 'date').distinct().count()
    present_count = att.filter(status='present').values('subject', 'date').distinct().count()
    attendance_pct = (present_count / total_classes * 100) if total_classes else 0

    # Grade average (scale 0-100 from total marks, assume max 100 per subject)
    grades = GradeRecord.objects.filter(student=student_profile)
    if grades.exists():
        grade_avg = sum(g.total for g in grades) / grades.count()
    else:
        grade_avg = 0

    # Assignments % (placeholder: no Assignment model; use 80 as default)
    assignments_pct = 80

    score = 100 - ((attendance_pct * 0.4) + (grade_avg * 0.4) + (assignments_pct * 0.2))
    score = max(0, min(100, round(score, 1)))

    if score <= 30:
        label = 'Low'
    elif score <= 60:
        label = 'Medium'
    else:
        label = 'High'

    return score, label
