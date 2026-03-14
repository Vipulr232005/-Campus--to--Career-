"""
HireSense AI — Faculty utils: at-risk students
"""
from students.models import StudentProfile
from students.utils import calculate_risk_score


def get_at_risk_students(faculty_user, threshold=60):
    """Return student profiles with risk score > threshold."""
    at_risk = []
    for profile in StudentProfile.objects.select_related('user').all():
        score, _ = calculate_risk_score(profile)
        if score > threshold:
            at_risk.append((profile, score))
    at_risk.sort(key=lambda x: -x[1])
    return at_risk
