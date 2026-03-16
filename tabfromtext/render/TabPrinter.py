import io
import os
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfdoc import PDFDictionary, PDFName

from tabfromtext.song.Song import Song
from tabfromtext.render.TabRenderer import render_tab, render_title_page
import tabfromtext.render.LayoutUtils as lu

A4_WIDTH_PT, A4_HEIGHT_PT = A4


def _image_to_reader(img: Image.Image) -> ImageReader:
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return ImageReader(buf)


def _image_dimensions_pt(img: Image.Image) -> tuple[float, float]:
    ppp = 72.0 / (lu.cfg.dpi * lu.scale)
    return img.size[0] * ppp, img.size[1] * ppp


def _print_instrument(
    c: canvas.Canvas,
    images_with_names: list[tuple[str, Image.Image]],
    title: str = "",
    instrument_name: str = "",
) -> None:
    cfg          = lu.cfg
    v_margin_top = cfg.page.top_margin_pt
    v_margin_bot = cfg.page.bottom_margin_pt
    f_margin     = cfg.page.footer_margin_pt
    block_gap    = cfg.page.block_gap_pt
    footer_font  = cfg.fonts.footer_pt
    printable_h  = A4_HEIGHT_PT - v_margin_top - v_margin_bot

    entries: list[tuple[Image.Image, float, float]] = []
    for _filename, img in images_with_names:
        w_pt, h_pt = _image_dimensions_pt(img)
        entries.append((img, w_pt, h_pt))

    page_num       = 1
    page_entries: list[tuple[Image.Image, float, float]] = []
    page_used_h_pt = 0.0

    def flush_page() -> None:
        nonlocal page_num
        y_cursor_pt = A4_HEIGHT_PT - v_margin_top
        for i, (im, w, h) in enumerate(page_entries):
            if i > 0:
                y_cursor_pt -= block_gap
            c.drawImage(_image_to_reader(im), 0, y_cursor_pt - h, width=w, height=h)
            y_cursor_pt -= h
        c.setFont("Helvetica", footer_font)
        c.drawCentredString(A4_WIDTH_PT / 2, v_margin_bot / 2, str(page_num))
        if title:
            c.drawString(f_margin, v_margin_bot / 2, title)
        if instrument_name:
            c.drawRightString(A4_WIDTH_PT - f_margin, v_margin_bot / 2, instrument_name)
        c.showPage()
        page_num += 1

    for img, w_pt, h_pt in entries:
        gap  = block_gap if page_entries else 0.0
        fits = (page_used_h_pt + gap + h_pt) <= printable_h

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

    for instrument in song.instruments:
        safe_instrument_name = instrument.name.lower().replace(' ', '_')
        output_base_path = f"demo/build/{safe_song_title}/{safe_instrument_name}/tab"
        images_with_names = render_tab(instrument.segments, instrument.name,
                                       output_base_path)

        pdf_path = os.path.join(output_dir, f"{safe_song_title}_{safe_instrument_name}.pdf")
        c = canvas.Canvas(pdf_path, pagesize=A4)
        c._doc.Catalog.ViewerPreferences = PDFDictionary({"PrintScaling": PDFName("None")})

        title_page_img = render_title_page(song, num_columns=2)
        if title_page_img is not None:
            w_pt, h_pt = _image_dimensions_pt(title_page_img)
            c.drawImage(_image_to_reader(title_page_img), 0,
                        A4_HEIGHT_PT - lu.cfg.page.top_margin_pt - h_pt,
                        width=w_pt, height=h_pt)
            c.showPage()

        _print_instrument(c, images_with_names,
                          title=song.title, instrument_name=instrument.name)
        c.save()
        print(f"PDF salvestatud: {pdf_path}")