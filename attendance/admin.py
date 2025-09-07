from django.contrib import admin
from .models import (
    Student,
    SchoolYear,
    Section,
    Enrollment,
    AttendanceSessionRecord,
    NonSchoolDay,
)


@admin.register(SchoolYear)
class SchoolYearAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date", "end_date", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "sex", "birthdate", "lrn", "is_active")
    list_filter = ("sex", "is_active")
    search_fields = ("last_name", "first_name", "lrn")

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("name", "school_year", "adviser")
    list_filter = ("school_year",)
    search_fields = ("name", "adviser__username", "adviser__first_name", "adviser__last_name")


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "school_year", "section", "active", "date_enrolled")
    list_filter = ("school_year", "section", "active")
    search_fields = ("student__last_name", "student__first_name")

@admin.register(AttendanceSessionRecord)
class AttendanceSessionRecordAdmin(admin.ModelAdmin):
    list_display = ("enrollment", "date", "session", "status", "remarks")
    list_filter = ("date", "session", "status", "enrollment__school_year", "enrollment__section")
    search_fields = (
        "enrollment__student__last_name",
        "enrollment__student__first_name",
        "remarks",
    )
    date_hierarchy = "date"


@admin.register(NonSchoolDay)
class NonSchoolDayAdmin(admin.ModelAdmin):
    list_display = ("date", "school_year", "kind", "title")
    list_filter = ("school_year", "kind")
    search_fields = ("title", "notes")
    date_hierarchy = "date"
