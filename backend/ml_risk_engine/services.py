"""
ML Risk Engine service: build features from student data, run dropout prediction.
Uses scikit-learn (model trained separately; this loads and predicts).
"""
import os
import json
from django.conf import settings
from students.models import StudentProfile, AttendanceRecord, Grade, Assignment


def get_student_features(profile: StudentProfile) -> dict:
    """Build feature dict for one student (attendance, grades, assignment patterns)."""
    from django.db.models import Avg, Count, Q

    # Attendance: fraction of present days (recent)
    att = AttendanceRecord.objects.filter(student=profile)
    total_days = att.count()
    present_days = att.filter(present=True).count()
    attendance_pct = (present_days / total_days * 100) if total_days else 0

    # Grades: average grade point
    grades = Grade.objects.filter(student=profile).aggregate(avg=Avg("grade_point"))
    avg_grade = float(grades["avg"] or 0)

    # Assignments: submission rate and average score
    assignments = Assignment.objects.filter(student=profile)
    total_assign = assignments.count()
    submitted = assignments.filter(submitted=True).count()
    submission_rate = (submitted / total_assign * 100) if total_assign else 0
    assign_avg = assignments.aggregate(avg=Avg("marks_obtained"))
    avg_assign_marks = float(assign_avg["avg"] or 0)

    return {
        "attendance_pct": round(attendance_pct, 2),
        "avg_grade_point": round(avg_grade, 2),
        "assignment_submission_rate": round(submission_rate, 2),
        "avg_assignment_marks": round(avg_assign_marks, 2),
        "cgpa": float(profile.cgpa or 0),
    }


def predict_risk(profile: StudentProfile) -> tuple[float, str, dict]:
    """
    Return (risk_score 0-1, risk_label, features_dict).
    If no trained model, use a simple heuristic.
    """
    features = get_student_features(profile)
    model_path = getattr(settings, "ML_RISK_MODEL_PATH", None)

    if model_path and os.path.isfile(model_path):
        try:
            import joblib
            model = joblib.load(model_path)
            # Expect model to have predict_proba or a single risk score
            X = [[
                features["attendance_pct"],
                features["avg_grade_point"],
                features["assignment_submission_rate"],
                features["avg_assignment_marks"],
                features["cgpa"],
            ]]
            if hasattr(model, "predict_proba"):
                proba = model.predict_proba(X)[0]
                risk_score = float(proba[1] if proba.shape[0] > 1 else proba[0])
            else:
                risk_score = float(model.predict(X)[0])
            risk_score = max(0, min(1, risk_score))
        except Exception:
            risk_score = _heuristic_risk(features)
    else:
        risk_score = _heuristic_risk(features)

    if risk_score >= 0.7:
        risk_label = "high"
    elif risk_score >= 0.4:
        risk_label = "medium"
    else:
        risk_label = "low"

    return risk_score, risk_label, features


def _heuristic_risk(features: dict) -> float:
    """Simple rule-based risk when no ML model is loaded."""
    # Higher risk if low attendance, low grades, low submission
    att = features.get("attendance_pct", 100) / 100
    grade = features.get("avg_grade_point", 0) / 10
    sub = features.get("assignment_submission_rate", 100) / 100
    # Inverse so low values -> high risk
    risk = (1 - att) * 0.4 + (1 - grade) * 0.4 + (1 - sub) * 0.2
    return max(0, min(1, risk))
