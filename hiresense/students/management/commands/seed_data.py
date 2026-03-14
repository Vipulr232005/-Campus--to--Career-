"""
HireSense AI — Seed demo data
Run: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from accounts.models import CustomUser
from students.models import StudentProfile, Subject, AttendanceRecord, GradeRecord
from faculty.models import FacultyProfile, Announcement
from companies.models import CompanyProfile, JobPosting, JobApplication


class Command(BaseCommand):
    help = 'Create demo users, subjects, attendance, grades, jobs, applications, announcements'

    def handle(self, *args, **options):
        # Users
        students_data = [
            ('student1@demo.com', 'Student', 'One'),
            ('student2@demo.com', 'Student', 'Two'),
            ('student3@demo.com', 'Student', 'Three'),
            ('student4@demo.com', 'Student', 'Four'),
            ('student5@demo.com', 'Student', 'Five'),
        ]
        student_users = []
        for email, first, last in students_data:
            u, _ = CustomUser.objects.get_or_create(
                email=email,
                defaults={'username': email, 'first_name': first, 'last_name': last, 'role': 'student'}
            )
            u.set_password('demo123')
            u.save()
            student_users.append(u)

        faculty_user, _ = CustomUser.objects.get_or_create(
            email='faculty@demo.com',
            defaults={'username': 'faculty@demo.com', 'first_name': 'Demo', 'last_name': 'Faculty', 'role': 'faculty'}
        )
        faculty_user.set_password('demo123')
        faculty_user.save()

        company_user, _ = CustomUser.objects.get_or_create(
            email='company@demo.com',
            defaults={'username': 'company@demo.com', 'first_name': 'Demo', 'last_name': 'Company', 'role': 'company'}
        )
        company_user.set_password('demo123')
        company_user.save()

        # Profiles
        for i, u in enumerate(student_users, 1):
            StudentProfile.objects.get_or_create(
                user=u,
                defaults={'roll_number': f'R{i}001', 'branch': 'CSE', 'year': 2, 'semester': 3}
            )
        FacultyProfile.objects.get_or_create(user=faculty_user, defaults={'department': 'CSE', 'employee_id': 'F001'})
        comp_prof, _ = CompanyProfile.objects.get_or_create(
            user=company_user,
            defaults={'company_name': 'Demo Company', 'industry': 'Tech', 'location': 'Bangalore', 'website': 'https://demo.com', 'about': 'We hire.'}
        )

        # Subjects
        subj_data = [('DSA', 'CS201', 3), ('DBMS', 'CS202', 3), ('OS', 'CS203', 3), ('CN', 'CS204', 3), ('ML', 'CS205', 3)]
        subjects = []
        for name, code, sem in subj_data:
            s, _ = Subject.objects.get_or_create(code=code, defaults={'name': name, 'semester': sem, 'faculty': faculty_user})
            subjects.append(s)

        # Attendance (varied 55-90%)
        for i, prof in enumerate(StudentProfile.objects.all()):
            for subj in subjects:
                for d in range(1, 16):
                    dt = date.today() - timedelta(days=d * 2)
                    present = (i * 3 + d) % 10 < (6 + i)  # vary by student
                    AttendanceRecord.objects.get_or_create(
                        student=prof, subject=subj, date=dt,
                        defaults={'status': 'present' if present else 'absent'}
                    )

        # Grades (2 semesters)
        for prof in StudentProfile.objects.all():
            for subj in subjects:
                for sem in [1, 2]:
                    GradeRecord.objects.get_or_create(
                        student=prof, subject=subj, semester=sem,
                        defaults={'internal_marks': 15 + (prof.id % 10), 'external_marks': 50 + (prof.id % 30)}
                    )

        # Jobs
        job1, _ = JobPosting.objects.get_or_create(
            company=comp_prof, title='Software Intern',
            defaults={'department': 'Engineering', 'skills_required': 'Python, React', 'experience_level': 'fresher',
                      'salary_min': 20000, 'salary_max': 30000, 'description': 'Backend and frontend.', 'deadline': date.today() + timedelta(days=60)}
        )
        job2, _ = JobPosting.objects.get_or_create(
            company=comp_prof, title='Data Analyst',
            defaults={'department': 'Data', 'skills_required': 'SQL, Python', 'experience_level': 'junior',
                      'salary_min': 35000, 'salary_max': 50000, 'description': 'Analyze data.', 'deadline': date.today() + timedelta(days=45)}
        )

        # Applications (2 with AI scores)
        for i, u in enumerate(student_users[:2]):
            JobApplication.objects.get_or_create(
                job=job1, applicant=u,
                defaults={'ai_fit_score': 70 + i * 15, 'matched_skills': 'Python', 'missing_skills': 'Docker', 'status': 'pending'}
            )

        # Announcements
        Announcement.objects.get_or_create(
            title='Mid-sem exam schedule', posted_by=faculty_user,
            defaults={'description': 'Exams from next week.', 'category': 'exam'}
        )
        Announcement.objects.get_or_create(
            title='Placement drive', posted_by=faculty_user,
            defaults={'description': 'TechCorp visiting on 20th.', 'category': 'event'}
        )
        Announcement.objects.get_or_create(
            title='Assignment deadline', posted_by=faculty_user,
            defaults={'description': 'Submit by Friday.', 'category': 'general'}
        )

        self.stdout.write(self.style.SUCCESS('Seed data created. Login: student1@demo.com / faculty@demo.com / company@demo.com — password: demo123'))
