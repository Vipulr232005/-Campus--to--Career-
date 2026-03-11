# Campus to Career

**Final year project:** Student Performance Prediction + Early Warning + AI Resume Screener + Job Portal for Indian colleges and SMEs.

- **Students:** Dashboard (attendance, grades, assignments), ML dropout risk, resume builder, job applications.
- **Faculty:** At-risk students list (ML), alerts, explainability (why a student was flagged).
- **Companies:** Post jobs, receive applications, run AI resume screening, view ranked shortlists with explainability.

## Tech stack

| Layer        | Tech                    |
|-------------|--------------------------|
| Frontend    | React (Vite)             |
| Backend     | Django REST Framework    |
| Database    | PostgreSQL               |
| Auth        | JWT (Student / Faculty / Company) |
| ML risk     | scikit-learn             |
| Resume rank | NLP (TF/keywords; extend with NLTK/spaCy) |
| Explainability | SHAP (optional) / rule-based |

## Quick start

### Backend (Django)

```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r ../requirements.txt
# Create DB: createdb campus_to_career
copy .env.example .env  # edit .env with DB credentials
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Train dropout risk model (optional):

```bash
cd backend
python -m ml_risk_engine.train_stub
```

### Frontend (React)

```bash
cd frontend
npm install
npm run dev
```

- Backend: http://localhost:8000  
- Frontend: http://localhost:3000  
- API: http://localhost:8000/api/

## Project structure

```
Campus-to-Career/
├── backend/
│   ├── config/           # Django settings, urls
│   ├── users/            # JWT auth, 3 roles
│   ├── students/         # Profile, attendance, grades, assignments
│   ├── faculty/          # At-risk view, alerts
│   ├── companies/        # Jobs, applications
│   ├── resume_builder/   # ATS resume from profile
│   ├── ml_risk_engine/   # Dropout prediction (scikit-learn)
│   ├── resume_screener/  # Rank resumes vs job (NLP)
│   └── explainability/   # Why ranked/flagged (SHAP/rule-based)
├── frontend/             # React app
├── requirements.txt
└── README.md
```

## API overview

| Endpoint group      | Purpose                          |
|---------------------|----------------------------------|
| `api/auth/`         | Register, JWT token, profile     |
| `api/students/`     | Profile, attendance, grades, assignments |
| `api/faculty/`      | At-risk list, alerts             |
| `api/companies/`    | Jobs, applications               |
| `api/resume-builder/` | Resume CRUD                    |
| `api/risk/`         | My risk, at-risk list, per-student risk |
| `api/screener/`     | Run screening for a job          |
| `api/explain/`      | Explain risk, explain application rank |

## Next steps

1. **Data:** Import real attendance/grades or keep using admin to seed data.
2. **ML:** Replace `train_stub` with real dataset; tune features and model.
3. **NLP:** Add NLTK/spaCy + TF-IDF or sentence embeddings for better resume–job matching.
4. **SHAP:** Integrate SHAP explainer for risk model and (if applicable) screener.
5. **UI:** Add resume builder form, job apply flow, and explainability panels in React.

This scaffold gives you a running full-stack with 3 roles, two ML flows (risk + screener), and explainability hooks—ready to demo and extend.
