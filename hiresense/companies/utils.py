"""
HireSense AI — AI fit score: keyword match between resume and JD
"""
import re


def normalize_text(text):
    """Lowercase, alphanumeric + spaces, split into words."""
    if not text:
        return []
    s = re.sub(r'[^a-z0-9\s]', ' ', (text or '').lower())
    return [w for w in s.split() if len(w) > 1]


def calculate_fit_score(resume_text, jd_text):
    """
    Extract words from both; score = (matched / total_jd_keywords) * 100.
    Returns (score float, matched_skills list, missing_skills list).
    """
    resume_words = set(normalize_text(resume_text))
    jd_words = set(normalize_text(jd_text))

    # Filter to meaningful keywords (length > 2, not pure numbers)
    jd_keywords = {w for w in jd_words if len(w) > 2 and not w.isdigit()}
    resume_keywords = {w for w in resume_words if len(w) > 2 and not w.isdigit()}

    matched = list(jd_keywords & resume_keywords)
    missing = list(jd_keywords - resume_keywords)

    total_jd = len(jd_keywords) or 1
    score = round((len(matched) / total_jd) * 100, 1)
    score = min(100, max(0, score))

    return score, matched, missing
