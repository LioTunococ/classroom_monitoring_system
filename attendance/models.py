from django.db import models
from django.conf import settings
from django.utils import timezone
from django.conf import settings as dj_settings

# Shared status choices for attendance
STATUS_CHOICES = (
    ("P", "Present"),
    ("A", "Absent"),
    ("L", "Late"),
    ("E", "Excused"),
)


class SchoolYear(models.Model):
    name = models.CharField(max_length=32, unique=True, help_text="e.g., 2024-2025")
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(max_length=100)
    school_year = models.ForeignKey(SchoolYear, on_delete=models.CASCADE, related_name="sections")
    adviser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sections")

    class Meta:
        unique_together = ("name", "school_year")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} - {self.school_year}"


class Student(models.Model):
    SEX_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
    )

    lrn = models.CharField(max_length=20, blank=True, null=True, help_text="Learner Reference Number (optional)")
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    birthdate = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    guardian_name = models.CharField(max_length=150, blank=True)
    guardian_phone = models.CharField(max_length=30, blank=True, help_text="Parent/guardian mobile (e.g., 09171234567 or +639171234567)")

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="enrollments")
    school_year = models.ForeignKey(SchoolYear, on_delete=models.CASCADE, related_name="enrollments")
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True, related_name="enrollments")
    date_enrolled = models.DateField(default=timezone.now)
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("student", "school_year")
        ordering = ["student__last_name", "student__first_name"]

    def __str__(self):
        return f"{self.student} - {self.school_year}"


class AttendanceSessionRecord(models.Model):
    SESSION_CHOICES = (
        ("AM", "AM"),
        ("PM", "PM"),
    )

    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name="attendance_sessions")
    date = models.DateField()
    session = models.CharField(max_length=2, choices=SESSION_CHOICES)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="P")
    remarks = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ("enrollment", "date", "session")
        ordering = ["-date", "session", "enrollment__student__last_name"]

    def __str__(self):
        return f"{self.enrollment} - {self.date} {self.session}: {self.get_status_display()}"


class NonSchoolDay(models.Model):
    TYPE_CHOICES = (
        ("HOL", "Holiday"),
        ("SUS", "Class Suspension"),
    )

    school_year = models.ForeignKey(SchoolYear, on_delete=models.CASCADE, related_name="non_school_days")
    date = models.DateField()
    kind = models.CharField(max_length=3, choices=TYPE_CHOICES, default="HOL")
    title = models.CharField(max_length=150)
    notes = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ("school_year", "date")
        ordering = ["-date"]
        indexes = [
            models.Index(fields=["school_year", "date"], name="idx_nsd_sy_date"),
            models.Index(fields=["date"], name="idx_nsd_date"),
        ]

    def __str__(self):
        return f"{self.get_kind_display()} - {self.title} ({self.date})"


class Notification(models.Model):
    user = models.ForeignKey(dj_settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    created = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=255)
    url = models.CharField(max_length=255, blank=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["user", "is_read", "-created"], name="idx_notif_user_read_created"),
        ]

    def __str__(self):
        return f"{self.user}: {self.message}"


class Period(models.Model):
    HALF_CHOICES = (
        ("AM", "AM"),
        ("PM", "PM"),
    )
    school_year = models.ForeignKey(SchoolYear, on_delete=models.CASCADE, related_name="periods")
    name = models.CharField(max_length=50)
    order = models.PositiveIntegerField(default=1)
    half = models.CharField(max_length=2, choices=HALF_CHOICES, default="AM")
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        unique_together = ("school_year", "name")

    def __str__(self):
        return f"{self.school_year} - {self.name} ({self.half})"


class AttendancePeriodRecord(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name="period_attendance")
    date = models.DateField()
    period = models.ForeignKey(Period, on_delete=models.CASCADE, related_name="attendance_records")
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="P")
    time_in = models.TimeField(blank=True, null=True)
    remarks = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ("enrollment", "date", "period")
        ordering = ["-date", "period__order", "enrollment__student__last_name"]

    def __str__(self):
        return f"{self.enrollment} - {self.date} {self.period.name}: {self.get_status_display()}"


class SectionAccess(models.Model):
    """Grants a user access to a specific Section (e.g., Student Officer)."""
    ROLE_CHOICES = (
        ("OFFICER", "Student Officer"),
        ("ASSISTANT", "Assistant"),
    )
    user = models.ForeignKey(dj_settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="section_access")
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="user_access")
    role = models.CharField(max_length=16, choices=ROLE_CHOICES, default="OFFICER")

    class Meta:
        unique_together = ("user", "section")
        indexes = [
            models.Index(fields=["user", "section"], name="idx_secaccess_user_section"),
        ]

    def __str__(self):
        return f"{self.user} -> {self.section} ({self.role})"


class FeatureAccess(models.Model):
    """Per-user feature overrides (allow or deny) to customize access without changing groups."""
    FEATURE_CHOICES = (
        ('dashboard', 'Dashboard'),
        ('take_attendance', 'Take Attendance'),
        ('view_reports', 'View Reports'),
        ('manage_schoolyears', 'Manage School Years'),
        ('enroll_students', 'Enroll Students'),
        ('manage_periods', 'Manage Periods'),
        ('assign_section', 'Assign Section'),
        ('manage_students', 'Manage Students'),
        ('view_student_history', 'View Student History'),
        ('manage_reports', 'Manage Reports/NSDs'),
    )
    user = models.ForeignKey(dj_settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feature_access')
    feature = models.CharField(max_length=64, choices=FEATURE_CHOICES)
    allow = models.BooleanField(default=True, help_text="Allow if checked, deny if unchecked")

    class Meta:
        unique_together = ("user", "feature")
        indexes = [
            models.Index(fields=["user", "feature"], name="idx_feataccess_user_feature"),
        ]

    def __str__(self):
        state = 'allow' if self.allow else 'deny'
        return f"{self.user} {state} {self.feature}"
