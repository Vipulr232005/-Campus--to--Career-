"""
Resume Screener service: rank resumes against job description using NLP.
Uses TF-IDF or simple keyword overlap; can be replaced with NLTK/spaCy + ML.
"""
from django.db import transaction
from companies.models import Job, Application
from resume_builder.models import Resume
from .models import ScreeningResult


def _tokenize(text: str) -> list:
    """Simple tokenization (replace with NLTK if needed)."""
    if not text:
        return []
    return [t.lower().strip() for t in text.replace(",", " ").replace(".", " ").split() if len(t.strip()) > 1]


def score_resume_job(resume_text: str, job_description: str, job_requirements: str = "") -> tuple[float, list]:
    """
    Return (match_score 0-1, list of matched_keywords).
    Simple TF-style overlap; can swap in NLTK/spaCy + classifier.
    """
    job_tokens = set(_tokenize(job_description) + _tokenize(job_requirements))
    resume_tokens = set(_tokenize(resume_text))
    if not job_tokens:
        return 0.0, []
    overlap = job_tokens & resume_tokens
    score = len(overlap) / len(job_tokens)
    score = min(1.0, score * 2)  # scale so partial match is reasonable
    return round(score, 4), list(overlap)[:20]


def run_screening_for_job(job_id: int) -> int:
    """Score and rank all applications for a job; update Application.match_score and rank. Returns count updated."""
    job = Job.objects.prefetch_related("applications__applicant").get(id=job_id)
    job_text = f"{job.title} {job.description} {job.requirements}"
    applications = list(job.applications.select_related("applicant").all())
    scored = []
    for app in applications:
        try:
            resume = Resume.objects.get(student=app.applicant)
            text = resume.raw_text or f"{resume.summary} {' '.join(resume.skills)}"
        except Resume.DoesNotExist:
            text = ""
        score, keywords = score_resume_job(text, job.description, job.requirements)
        scored.append((app, score, keywords))
    scored.sort(key=lambda x: -x[1])
    with transaction.atomic():
        for rank, (app, score, keywords) in enumerate(scored, start=1):
            app.match_score = score
            app.rank = rank
            app.save(update_fields=["match_score", "rank"])
            ScreeningResult.objects.update_or_create(
                application=app,
                defaults={"match_score": score, "rank": rank, "matched_keywords": keywords},
            )
    return len(scored)
