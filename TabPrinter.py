import io
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from object.Song import Song
from TabRenderer import render_song

# --- Constants ---
PAGE_MARGIN_CM = 2.0
IMAGE_DPI = 96  # the DPI at which TabRenderer produces its images

# Derived
CM_TO_PT = 28.3465
PAGE_MARGIN_PT = PAGE_MARGIN_CM * CM_TO_PT

A4_WIDTH_PT, A4_HEIGHT_PT = A4  # 595.27 x 841.89 pt
PRINTABLE_WIDTH_PT = A4_WIDTH_PT - 2 * PAGE_MARGIN_PT
PRINTABLE_HEIGHT_PT = A4_HEIGHT_PT - 2 * PAGE_MARGIN_PT


def _px_to_pt(px: float) -> float:
    """Convert pixels (at IMAGE_DPI) to PDF points."""
    return px / IMAGE_DPI * 72


def _image_dimensions_pt(img: Image.Image) -> tuple[float, float]:
    """Return the natural (width, height) of the image in PDF points."""
    w_pt = _px_to_pt(img.size[0])
    h_pt = _px_to_pt(img.size[1])
    return w_pt, h_pt


def _fit_to_printable_width(w_pt: float, h_pt: float) -> tuple[float, float]:
    """Scale down to fit printable width if necessary, preserving aspect ratio."""
    if w_pt <= PRINTABLE_WIDTH_PT:
        return w_pt, h_pt
    scale = PRINTABLE_WIDTH_PT / w_pt
    return PRINTABLE_WIDTH_PT, h_pt * scale


def _image_to_reader(img: Image.Image) -> ImageReader:
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return ImageReader(buf)


def print_song(song: Song, output_path: str) -> None:
    images_with_names = render_song(song)

    # Pre-compute fitted pt dimensions for each image (no pixel resampling)
    entries: list[tuple[Image.Image, float, float]] = []
    for _filename, img in images_with_names:
        w_pt, h_pt = _image_dimensions_pt(img)
        w_pt, h_pt = _fit_to_printable_width(w_pt, h_pt)
        entries.append((img, w_pt, h_pt))

    c = canvas.Canvas(output_path, pagesize=A4)

    page_entries: list[tuple[Image.Image, float, float]] = []
    page_used_h_pt = 0.0

    def flush_page() -> None:
        y_cursor_pt = A4_HEIGHT_PT - PAGE_MARGIN_PT  # top of printable area
        for im, w, h in page_entries:
            c.drawImage(
                _image_to_reader(im),
                PAGE_MARGIN_PT,
                y_cursor_pt - h,
                width=w,
                height=h,
            )
            y_cursor_pt -= h
        c.showPage()

    for img, w_pt, h_pt in entries:
        fits = (page_used_h_pt + h_pt) <= PRINTABLE_HEIGHT_PT

        if not fits and page_entries:
            flush_page()
            page_entries = []
            page_used_h_pt = 0.0

        page_entries.append((img, w_pt, h_pt))
        page_used_h_pt += h_pt

    if page_entries:
        flush_page()

    c.save()
    print(f"PDF salvestatud: {output_path}")