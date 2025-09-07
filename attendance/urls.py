from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('students/', views.student_list, name='student_list'),
    path('students/new/', views.student_create, name='student_create'),
    path('students/<int:pk>/edit/', views.student_edit, name='student_edit'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),
    path('students/<int:pk>/archive/', views.student_archive, name='student_archive'),
    path('students/<int:pk>/restore/', views.student_restore, name='student_restore'),
    path('school-years/', views.schoolyear_list, name='schoolyear_list'),
    path('school-years/new/', views.schoolyear_create, name='schoolyear_create'),
    path('school-years/<int:pk>/edit/', views.schoolyear_edit, name='schoolyear_edit'),
    path('enroll/<int:schoolyear_id>/', views.enroll_students, name='enroll_students'),
    path('attendance/<int:schoolyear_id>/', views.take_attendance, name='take_attendance'),
    path('sections/<int:schoolyear_id>/assign/', views.bulk_assign_section, name='bulk_assign_section'),
    path('reports/monthly/', views.report_form, name='report_form'),
    path('reports/monthly/export/', views.export_monthly_report, name='export_monthly_report'),
    path('reports/monthly/preview/', views.report_preview, name='report_preview'),
    path('non-school-days/import/', views.non_school_days_import, name='non_school_days_import'),
]
