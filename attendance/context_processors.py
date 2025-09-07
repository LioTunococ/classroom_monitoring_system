from .models import SchoolYear


def active_sy(request):
    """Expose the active school year to all templates for navbar links."""
    try:
        sy = SchoolYear.objects.filter(is_active=True).first()
    except Exception:
        sy = None
    return {"active_sy": sy}

