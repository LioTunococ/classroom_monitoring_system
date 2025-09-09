from django.contrib.auth.models import Group
from .models import FeatureAccess


# Feature keys used to gate views and nav
FEATURES = {
    'dashboard',
    'take_attendance',
    'view_reports',
    'manage_schoolyears',
    'enroll_students',
    'manage_periods',
    'assign_section',
    'manage_students',
    'view_student_history',
    'manage_reports',
}


def _in_group(user, name: str) -> bool:
    try:
        return user.groups.filter(name=name).exists()
    except Exception:
        return False


def has_feature(user, feature: str) -> bool:
    if not getattr(user, 'is_authenticated', False):
        return False
    if getattr(user, 'is_superuser', False):
        return True
    # Per-user override takes precedence
    try:
        fa = FeatureAccess.objects.filter(user=user, feature=feature).first()
        if fa is not None:
            return bool(fa.allow)
    except Exception:
        pass
    # Map legacy staff to Admin-like access for backward compatibility
    if getattr(user, 'is_staff', False):
        admin_like = {
            'dashboard', 'take_attendance', 'view_reports', 'manage_schoolyears',
            'enroll_students', 'manage_periods', 'assign_section',
            'manage_students', 'view_student_history', 'manage_reports',
        }
        return feature in admin_like

    # Group-based roles
    is_admin = _in_group(user, 'Admin') or _in_group(user, 'SchoolAdmin')
    is_adviser = _in_group(user, 'Adviser')
    is_officer = _in_group(user, 'StudentOfficer')

    if is_admin:
        return True
    if is_adviser:
        adviser_feats = {
            'dashboard', 'take_attendance', 'view_reports', 'manage_schoolyears',
            'enroll_students', 'manage_periods', 'assign_section', 'view_student_history',
        }
        return feature in adviser_feats
    if is_officer:
        officer_feats = {'dashboard', 'take_attendance', 'view_student_history'}
        return feature in officer_feats

    # Default minimal
    return feature in {'dashboard'}


def caps_for(user):
    return {key: has_feature(user, key) for key in FEATURES}
