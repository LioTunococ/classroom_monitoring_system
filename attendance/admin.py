from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import (
    Student,
    SchoolYear,
    Section,
    Enrollment,
    AttendanceSessionRecord,
    NonSchoolDay,
    Notification,
    SectionAccess,
    FeatureAccess,
)


@admin.register(SchoolYear)
class SchoolYearAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date", "end_date", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "last_name", "first_name", "sex", "birthdate", "lrn",
        "guardian_name", "guardian_phone", "is_active", "history_button",
    )
    list_filter = ("sex", "is_active")
    search_fields = ("last_name", "first_name", "lrn", "guardian_name", "guardian_phone")

    def history_button(self, obj):
        try:
            url = reverse('attendance:student_history', args=[obj.id])
            return format_html('<a class="button" href="{}" target="_blank">History</a>', url)
        except Exception:
            return ''
    history_button.short_description = 'History'

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


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "created", "message", "is_read")
    list_filter = ("is_read", "user")
    search_fields = ("message", "user__username", "user__first_name", "user__last_name")
    date_hierarchy = "created"


@admin.register(SectionAccess)
class SectionAccessAdmin(admin.ModelAdmin):
    list_display = ("user", "section", "role")
    list_filter = ("role", "section__school_year")
    search_fields = ("user__username", "user__first_name", "user__last_name", "section__name")


@admin.register(FeatureAccess)
class FeatureAccessAdmin(admin.ModelAdmin):
    list_display = ("user", "feature", "allow")
    list_filter = ("feature", "allow")
    search_fields = ("user__username", "user__first_name", "user__last_name")
