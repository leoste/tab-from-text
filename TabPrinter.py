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

CM_TO_PT = 28.3465

# Page margins (these become part of step 6 cleanup, but live here for now)
PAGE_MARGIN_CM          = 2.0
PAGE_VERTICAL_MARGIN_CM = 1.8
PAGE_MARGIN_PT          = PAGE_MARGIN_CM * CM_TO_PT
PAGE_VERTICAL_MARGIN_PT = PAGE_VERTICAL_MARGIN_CM * CM_TO_PT

A4_WIDTH_PT, A4_HEIGHT_PT = A4
PRINTABLE_WIDTH_PT  = A4_WIDTH_PT  - 2 * PAGE_MARGIN_PT
PRINTABLE_HEIGHT_PT = A4_HEIGHT_PT - 2 * PAGE_VERTICAL_MARGIN_PT


def _make_layout_config() -> LayoutConfig:
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
    return 72.0 / (cfg.dpi * cfg.scale)


def _image_dimensions_pt(img: Image.Image, cfg: LayoutConfig) -> tuple[float, float]:
    ppp = _pt_per_px(cfg)
    return img.size[0] * ppp, img.size[1] * ppp


def _print_instrument(
    c: canvas.Canvas,
    images_with_names: list[tuple[str, Image.Image]],
    cfg: LayoutConfig,
    title: str = "",
    instrument_name: str = "",
) -> None:
    """Lay out all segment images for one instrument onto the canvas.

    Segment images are stacked vertically with cfg.block_gap_pt between them.
    Images that don't fit on the current page trigger a page break.
    """
    block_gap_pt = cfg.block_gap_pt
    footer_font_size = cfg.footer_font_size_pt

    entries: list[tuple[Image.Image, float, float]] = []
    for _filename, img in images_with_names:
        w_pt, h_pt = _image_dimensions_pt(img, cfg)
        entries.append((img, w_pt, h_pt))

    page_num   = 1
    page_entries: list[tuple[Image.Image, float, float]] = []
    page_used_h_pt = 0.0

    def flush_page() -> None:
        nonlocal page_num
        y_cursor_pt = A4_HEIGHT_PT - PAGE_VERTICAL_MARGIN_PT
        for i, (im, w, h) in enumerate(page_entries):
            if i > 0:
                y_cursor_pt -= block_gap_pt
            c.drawImage(
                _image_to_reader(im),
                PAGE_MARGIN_PT,
                y_cursor_pt - h,
                width=w,
                height=h,
            )
            y_cursor_pt -= h
        c.setFont("Helvetica", footer_font_size)
        c.drawCentredString(A4_WIDTH_PT / 2, PAGE_VERTICAL_MARGIN_PT / 2, str(page_num))
        if title:
            c.drawString(PAGE_MARGIN_PT, PAGE_VERTICAL_MARGIN_PT / 2, title)
        if instrument_name:
            c.drawRightString(A4_WIDTH_PT - PAGE_MARGIN_PT,
                              PAGE_VERTICAL_MARGIN_PT / 2, instrument_name)
        c.showPage()
        page_num += 1

    for img, w_pt, h_pt in entries:
        # Gap is only added between blocks, not before the first one on a page
        gap = block_gap_pt if page_entries else 0.0
        fits = (page_used_h_pt + gap + h_pt) <= PRINTABLE_HEIGHT_PT

        if not fits and page_entries:
            flush_page()
            page_entries   = []
            page_used_h_pt = 0.0
            gap            = 0.0

        page_entries.append((img, w_pt, h_pt))
        page_used_h_pt += gap + h_pt

    if page_entries:
        flush_page()


def print_song(song: Song, output_dir: str) -> None:
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
        _print_instrument(c, images_with_names, cfg,
                          title=song.title, instrument_name=instrument.name)
        c.save()
        print(f"PDF salvestatud: {pdf_path}")