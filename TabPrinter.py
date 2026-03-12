import io
import os
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfdoc import PDFDictionary, PDFName

from object.Song import Song
from TabRenderer import render_tab
from LayoutConfig import LayoutConfig

# --- Page margin constants (pt) ---
PAGE_MARGIN_CM          = 2.0
PAGE_VERTICAL_MARGIN_CM = 1.8
PAGE_NUMBER_FONT_SIZE   = 10

CM_TO_PT = 28.3465
PAGE_MARGIN_PT          = PAGE_MARGIN_CM * CM_TO_PT
PAGE_VERTICAL_MARGIN_PT = PAGE_VERTICAL_MARGIN_CM * CM_TO_PT

A4_WIDTH_PT, A4_HEIGHT_PT = A4  # 595.27 x 841.89 pt
PRINTABLE_WIDTH_PT  = A4_WIDTH_PT  - 2 * PAGE_MARGIN_PT
PRINTABLE_HEIGHT_PT = A4_HEIGHT_PT - 2 * PAGE_VERTICAL_MARGIN_PT


def _make_layout_config() -> LayoutConfig:
    """Construct a LayoutConfig sized to the printable area of the page."""
    cfg = LayoutConfig()
    cfg.printable_width_pt = PRINTABLE_WIDTH_PT
    return cfg


def _image_to_reader(img: Image.Image) -> ImageReader:
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return ImageReader(buf)


def _pt_per_px(cfg: LayoutConfig) -> float:
    """How many PDF points correspond to one rendered pixel."""
    return 72.0 / cfg.dpi


def _image_dimensions_pt(img: Image.Image, cfg: LayoutConfig) -> tuple[float, float]:
    """Return the exact (width_pt, height_pt) of the image given the render DPI."""
    ppp = _pt_per_px(cfg)
    return img.size[0] * ppp, img.size[1] * ppp


def _print_instrument(
    c: canvas.Canvas,
    images_with_names: list[tuple[str, Image.Image]],
    cfg: LayoutConfig,
    title: str = "",
    instrument_name: str = "",
) -> None:
    """Lay out all segment images for one instrument onto the canvas, with page numbers.

    Images are rendered at exactly the printable width — no scaling needed.
    Images that don't fit on the current page trigger a page break.
    """
    ppp = _pt_per_px(cfg)
    entries: list[tuple[Image.Image, float, float]] = []
    for _filename, img in images_with_names:
        w_pt, h_pt = _image_dimensions_pt(img, cfg)
        entries.append((img, w_pt, h_pt))

    page_num = 1
    page_entries: list[tuple[Image.Image, float, float]] = []
    page_used_h_pt = 0.0

    def flush_page() -> None:
        nonlocal page_num
        y_cursor_pt = A4_HEIGHT_PT - PAGE_VERTICAL_MARGIN_PT
        for im, w, h in page_entries:
            c.drawImage(
                _image_to_reader(im),
                PAGE_MARGIN_PT,
                y_cursor_pt - h,
                width=w,
                height=h,
            )
            y_cursor_pt -= h
        c.setFont("Helvetica", PAGE_NUMBER_FONT_SIZE)
        c.drawCentredString(A4_WIDTH_PT / 2, PAGE_VERTICAL_MARGIN_PT / 2, str(page_num))
        if title:
            c.drawString(PAGE_MARGIN_PT, PAGE_VERTICAL_MARGIN_PT / 2, title)
        if instrument_name:
            c.drawRightString(A4_WIDTH_PT - PAGE_MARGIN_PT, PAGE_VERTICAL_MARGIN_PT / 2, instrument_name)
        c.showPage()
        page_num += 1

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


def print_song(song: Song, output_dir: str) -> None:
    """Render each instrument of a song to its own PDF in output_dir."""
    os.makedirs(output_dir, exist_ok=True)
    safe_song_title = song.title.lower().replace(' ', '_')

    cfg = _make_layout_config()

    for instrument in song.instruments:
        safe_instrument_name = instrument.name.lower().replace(' ', '_')
        output_base_path = f"tabs/{safe_song_title}/{safe_instrument_name}/tab"
        images_with_names = render_tab(instrument.segments, output_base_path, cfg)

        pdf_path = os.path.join(output_dir, f"{safe_song_title}_{safe_instrument_name}.pdf")
        c = canvas.Canvas(pdf_path, pagesize=A4)
        c._doc.Catalog.ViewerPreferences = PDFDictionary({"PrintScaling": PDFName("None")})
        _print_instrument(c, images_with_names, cfg, title=song.title, instrument_name=instrument.name)
        c.save()
        print(f"PDF salvestatud: {pdf_path}")