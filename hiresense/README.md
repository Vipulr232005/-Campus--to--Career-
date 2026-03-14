# HireSense AI — From Classroom to Career

Unified smart campus and hiring platform: students track academics and apply to jobs; faculty manage students and post updates; companies post jobs and screen AI-ranked resumes.

## Tech stack

- **Django 4.2** | **Python 3.11**
- **SQLite** (default, no extra setup)
- **Pillow** (images), **PyPDF2** (resume text), **python-docx** (optional)

## Setup

1. **Create and activate a virtual environment (recommended):**
   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
   # or: source venv/bin/activate   # Linux/macOS
   ```

2. **Install dependencies:**
   ```bash
   cd hiresense
   pip install -r requirements.txt
   ```

3. **Migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Seed demo data:**
   ```bash
   python manage.py seed_data
   ```

5. **Run the server:**
   ```bash
   python manage.py runserver
   ```
   Open **http://127.0.0.1:8000/**

## Demo login credentials

| Role    | Email             | Password |
|---------|-------------------|----------|
| Student | student1@demo.com | demo123  |
| Faculty | faculty@demo.com  | demo123  |
| Company | company@demo.com  | demo123  |

Additional students: `student2@demo.com` … `student5@demo.com` (same password).

## Project structure

```
hiresense/
├── manage.py
├── requirements.txt
├── hiresense/           # project config
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── accounts/            # CustomUser, login, register, profile
├── students/            # student dashboard, attendance, grades, risk, jobs
├── faculty/             # faculty dashboard, students, at-risk, results, announcements
├── companies/           # company dashboard, jobs, applications, AI ranker
├── landing/             # public landing page
├── templates/           # base, base_dashboard
├── static/
│   ├── css/main.css
│   └── js/waves.js, main.js
└── media/               # uploads (profiles, resumes, logos)
```

## Features

- **Role-based access:** Student / Faculty / Company; decorator `@role_required('student')` etc.
- **AI fit score:** On job application, resume text (PDF via PyPDF2) is compared to job description; score and matched/missing skills stored.
- **Risk score:** Computed from attendance %, grade average, and assignments (formula in `students/utils.py`).
- **Canvas wave background:** Cursor-reactive waves on all pages (`static/js/waves.js`).

## Commands

- `python manage.py seed_data` — Create demo users, subjects, attendance, grades, jobs, applications, announcements.
- `python manage.py createsuperuser` — Create an admin user for `/admin/`.
