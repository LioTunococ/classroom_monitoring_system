from .models import SchoolYear, Notification


def active_sy(request):
    """Expose the active school year to all templates for navbar links."""
    try:
        sy = SchoolYear.objects.filter(is_active=True).first()
    except Exception:
        sy = None
    # Unread notifications for the navbar badge
    unread = 0
    try:
        if getattr(request, 'user', None) and request.user.is_authenticated:
            unread = Notification.objects.filter(user=request.user, is_read=False).count()
    except Exception:
        unread = 0
    return {"active_sy": sy, "notif_unread": unread}
