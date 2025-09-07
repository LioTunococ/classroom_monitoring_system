# Classroom Monitoring System (Django)

A simple classroom monitoring system to track daily attendance per school year, export a monthly report in Excel (DepEd School Form 2 style), and show birthday reminders.

## Features

- School year management (set active SY, start/end dates)
- Student master list (LRN, sex, birthdate)
- Enrollment per school year
- Daily attendance with statuses: Present, Absent, Late, Excused
- Monthly report export to Excel (.xlsx) with daily columns and totals (SF2-like)
- Dashboard with upcoming birthdays (next 14 days) within the active school year
- Django Admin for full CRUD

## Quick Start

1. Create a virtual environment and install dependencies:

   - Windows PowerShell
     
     python -m venv .venv
     .\\.venv\\Scripts\\Activate.ps1
     pip install -r requirements.txt
     

2. Initialize the database:
   
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   

3. Run the development server:
   
   python manage.py runserver
   

4. In the browser:
   - Visit http://127.0.0.1:8000/admin/ to manage data or use the simple UI at http://127.0.0.1:8000/.
   - Create a School Year and mark it Active.
   - Add Students, then enroll them to the School Year.
   - Take daily attendance (Dashboard → Take Attendance).
   - Export monthly report (Reports → Monthly Report → Download Excel).

## Notes

- Time zone is set to Asia/Manila.
- Excel export uses openpyxl. If missing, install dependencies with `pip install -r requirements.txt`.
- The Excel layout follows a simplified SF2 style: columns for LRN, Learner's Name, Sex, Birthdate, days in the month (1–31 as applicable), and counts of Present/Absent/Late/Excused.
- Each school year has its own enrollment, so the same student can be enrolled across multiple school years.

## Project Structure

- manage.py — Django management entrypoint
- cms/ — Django project (settings, urls)
- attendance/ — Main app (models, views, forms, admin, urls)
- templates/attendance/ — Basic HTML templates

## Next Improvements (optional)

- Sections/classes and advisors
- Import/export students via CSV
- Attendance reasons and analytics
- Email/SMS notifications for birthdays or absences

