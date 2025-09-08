from django import template

register = template.Library()


def _normalize_digits(value: str) -> str:
    if not value:
        return ""
    # Keep digits and plus only
    out = []
    for ch in str(value).strip():
        if ch.isdigit() or ch == '+':
            out.append(ch)
    return ''.join(out)


def _to_ph_e164(value: str) -> str:
    s = _normalize_digits(value)
    if not s:
        return ""
    # Already +63...
    if s.startswith('+63'):
        return s
    # 63...
    if s.startswith('63'):
        return '+' + s
    # 09...
    if s.startswith('09') and len(s) >= 11:
        return '+63' + s[1:]
    # 9........ (common when users omit leading 0)
    if s.startswith('9') and len(s) >= 10:
        return '+63' + s
    return s  # Fallback: return as-is (might already be international)


@register.filter(name='phone_e164')
def phone_e164(value):
    """Return phone in E.164 for PH (+63...). Empty string if missing."""
    return _to_ph_e164(value)


@register.filter(name='phone_wa')
def phone_wa(value):
    """Return WhatsApp phone (no plus), e.g., 63XXXXXXXXXX."""
    e164 = _to_ph_e164(value)
    if e164.startswith('+'):
        return e164[1:]
    return e164


@register.filter(name='phone_no_plus')
def phone_no_plus(value):
    e164 = _to_ph_e164(value)
    return e164[1:] if e164.startswith('+') else e164


@register.filter(name='dict_get')
def dict_get(d, key):
    try:
        return d.get(key)
    except Exception:
        return None
