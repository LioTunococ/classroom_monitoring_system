from datetime import date, timedelta

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from attendance.models import (
    SchoolYear,
    Student,
    Enrollment,
    AttendanceSessionRecord,
    NonSchoolDay,
)
from attendance.views import _compute_sf2_summary


@pytest.mark.django_db
def test_sf2_summary_half_day_absences_and_holiday_exclusion():
    # Create school year covering a full month
    sy = SchoolYear.objects.create(
        name="2025-2026",
        start_date=date(2025, 6, 1),
        end_date=date(2025, 6, 30),
        is_active=True,
    )

    # One male student
    s = Student.objects.create(last_name="Test", first_name="Tom", sex="M")
    e = Enrollment.objects.create(student=s, school_year=sy)

    # Build a list of month days within SY
    days = [date(2025, 6, 1) + timedelta(n) for n in range(30)]

    # Determine first 12 school days (Mon-Fri) within June
    school_days = [d for d in days if sy.start_date <= d <= sy.end_date and d.weekday() < 5]
    assert len(school_days) >= 12

    # Mark the 6th school day as a Non-School Day (holiday)
    nsd_day = school_days[5]
    NonSchoolDay.objects.create(school_year=sy, date=nsd_day, kind="HOL", title="Holiday")

    # Create half-day absences for the first 12 school days (AM Absent, PM Present)
    # Excluding non-school day automatically as no records created there
    created = 0
    for d in school_days[:12]:
        if d == nsd_day:
            continue
        AttendanceSessionRecord.objects.create(enrollment=e, date=d, session="AM", status="A")
        AttendanceSessionRecord.objects.create(enrollment=e, date=d, session="PM", status="P")
        created += 1
    assert created >= 11  # With 1 excluded day, we have at least 11 half-day absences

    # Build by_key mapping for summary
    recs = AttendanceSessionRecord.objects.filter(enrollment=e, date__gte=sy.start_date, date__lte=sy.end_date)
    by_key = {(r.enrollment_id, r.date, r.session): r for r in recs}

    # Compute summary for June
    summary = _compute_sf2_summary(sy, 2025, 6, [d for d in days if sy.start_date <= d <= sy.end_date], [e], by_key)

    # School days exclude the declared holiday
    assert summary['school_days'] == len([d for d in school_days if d != nsd_day])

    # With 11 half-day absences (0.5 each), the consecutive absence streak >= 5.0 day-equivalents
    assert summary['by']['M']['absent5'] == 1
    assert summary['by']['T']['absent5'] == 1

