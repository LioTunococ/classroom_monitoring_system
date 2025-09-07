from io import BytesIO
from typing import Optional

from django.http import HttpResponse

try:
    from PIL import Image, ImageDraw
except Exception:  # pragma: no cover
    Image = None
    ImageDraw = None


BLUE = (13, 110, 253, 255)  # Bootstrap primary
WHITE = (255, 255, 255, 255)


def _rounded_rect(draw: "ImageDraw.ImageDraw", xy, radius: int, fill):
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill)


def _draw_c_letter(draw: "ImageDraw.ImageDraw", size: int):
    # Draw a thick white "C" using an arc
    margin = int(size * 0.22)
    bbox = (margin, margin, size - margin, size - margin)
    width = max(4, int(size * 0.18))
    # angles in degrees, starting at 3 o'clock going counter-clockwise
    # We want a C shape open on the right side
    draw.arc(bbox, start=120, end=240, fill=WHITE, width=width)
    draw.arc(bbox, start=-60, end=60, fill=WHITE, width=width)


def pwa_icon(request, size: str, variant: Optional[str] = None):
    if Image is None:
        return HttpResponse(status=501)

    n = int(size)
    img = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background rounded square
    radius = max(8, int(n * 0.12))
    _rounded_rect(draw, (0, 0, n, n), radius, BLUE)

    # Foreground mark
    _draw_c_letter(draw, n)

    out = BytesIO()
    img.save(out, format="PNG")
    data = out.getvalue()
    resp = HttpResponse(data, content_type="image/png")
    resp["Cache-Control"] = "public, max-age=604800, immutable"  # 7 days
    return resp

