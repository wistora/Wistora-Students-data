# WIS Student Portal

Django student portal with student registration, authentication, published quizzes, scoring, results, history, and admin management.

## Local setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/` for the student portal and `/admin/` for quiz and student management.

To link from the main site later, point a menu item or button to `https://students.wistoraiq.com` once DNS and deployment are ready, or to `/student-portal` when the main site reverse-proxies that path to this Django service.

## Render admin setup

Add these environment variables in Render:

```text
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=your-email@example.com
DJANGO_SUPERUSER_PASSWORD=choose-a-strong-password
```

Use this build command so the admin account is created or updated automatically without Shell access:

```text
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate && python manage.py create_admin
```