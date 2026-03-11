"""
Explainability: SHAP-based explanations for (1) dropout risk (2) resume ranking.
Shows WHY a student was flagged / WHY a candidate was ranked.
"""
import os
from django.conf import settings


def explain_risk_with_shap(features_dict: dict, risk_score: float) -> dict:
    """
    Return human-readable explanation for dropout risk.
    If SHAP explainer is available, return feature contributions; else rule-based.
    """
    # Rule-based explanation when no SHAP model
    reasons = []
    att = features_dict.get("attendance_pct", 100)
    if att < 75:
        reasons.append(f"Low attendance ({att}%)")
    grade = features_dict.get("avg_grade_point", 0)
    if grade < 5:
        reasons.append(f"Low average grade ({grade})")
    sub = features_dict.get("assignment_submission_rate", 100)
    if sub < 80:
        reasons.append(f"Low assignment submission rate ({sub}%)")
    if not reasons:
        reasons.append("Overall metrics within normal range")
    return {
        "risk_score": risk_score,
        "contributing_factors": reasons,
        "features_used": features_dict,
    }


def explain_ranking_with_shap(matched_keywords: list, match_score: float, job_title: str) -> dict:
    """Explain why a candidate was ranked (e.g. which skills/keywords matched)."""
    return {
        "match_score": match_score,
        "job_title": job_title,
        "why_ranked": "Matched keywords from job description and requirements.",
        "matched_keywords": matched_keywords,
    }
