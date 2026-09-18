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

## MySQL configuration

The application uses MySQL whenever `MYSQL_HOST` is set. Configure these environment variables before running migrations or starting the server:

```text
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DATABASE=student_portal
MYSQL_USER=your-mysql-user
MYSQL_PASSWORD=your-mysql-password
```

When `MYSQL_HOST` is not set, Django continues using the existing `db.sqlite3` file; it is not deleted or modified by this configuration change.

To link from the main site later, point a menu item or button to `https://students.wistoraiq.com` once DNS and deployment are ready, or to `/student-portal` when the main site reverse-proxies that path to this Django service.

## Render admin setup

Add these environment variables in Render. Use the connection details from your MySQL provider for the database values:

```text
DEBUG=False
SECRET_KEY=generate-a-long-random-secret
ALLOWED_HOSTS=students.wistoraiq.com,wistora-students-data.onrender.com
CSRF_TRUSTED_ORIGINS=https://students.wistoraiq.com,https://wistora-students-data.onrender.com
MYSQL_HOST=your-mysql-host
MYSQL_PORT=3306
MYSQL_DATABASE=student_portal
MYSQL_USER=your-mysql-user
MYSQL_PASSWORD=your-mysql-password
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=your-email@example.com
DJANGO_SUPERUSER_PASSWORD=choose-a-strong-password
```

Use this build command so the admin account is created or updated automatically without Shell access:

```text
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate && python manage.py create_admin
```