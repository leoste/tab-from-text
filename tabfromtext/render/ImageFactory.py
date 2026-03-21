"""PIL image allocation helpers shared across renderers.

All functions return (img, draw) or (img, draw, base_y) tuples
so callers can immediately start painting onto them.
"""
import math
from PIL import Image, ImageDraw

import tabfromtext.render.LayoutUtils as lu
from tabfromtext.render.RowPainter import lyrics_line_h_px


def new_image(height_px: int) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    """Allocate a white PIL image of the standard tab width and given height."""
    img  = Image.new('RGB', (int(lu.img_width_px), int(height_px)), color='white')
    draw = ImageDraw.Draw(img)
    return img, draw


def _title_top_px() -> int:
    return lu.px(lu.cfg.page.title_padding_top_pt)


def _base_y_px() -> int:
    return _title_top_px() + lu.title_h_px


def new_tab_image(segment, instrument_name) -> tuple[Image.Image, ImageDraw.ImageDraw, int]:
    """Allocate the PIL image for a normal tab segment.
    Returns (img, draw, base_y)."""
    segment_notes = segment.GetNotesFromSegment(instrument_name)
    total_units   = sum((n.duration if n.duration else 0) for n in segment_notes)
    num_systems   = math.ceil(math.ceil(total_units / lu.UNITS_PER_MEASURE) / lu.MEASURES_PER_LINE)
    height_px     = _base_y_px() + num_systems * lu.system_h_px
    img, draw     = new_image(height_px)
    return img, draw, _base_y_px()


def new_lyrics_only_image(segment) -> tuple[Image.Image, ImageDraw.ImageDraw, int]:
    """Allocate a compact PIL image for a lyrics-only segment.
    Returns (img, draw, base_y)."""
    total_units = segment.lyrics.total_ticks()
    num_systems = math.ceil(math.ceil(total_units / lu.UNITS_PER_MEASURE) / lu.MEASURES_PER_LINE)
    line_h      = lyrics_line_h_px()
    height_px   = _base_y_px() + num_systems * line_h
    img, draw   = new_image(height_px)
    return img, draw, _base_y_px()


def new_title_only_image() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    """Allocate a minimal PIL image showing only the segment title."""
    height_px = _base_y_px() + lu.below_str_px
    return new_image(height_px)


def new_title_page_image() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    """Allocate a full-page PIL image for the song title page."""
    from reportlab.lib.pagesizes import A4
    A4_HEIGHT_PT = A4[1]
    page_h_pt = A4_HEIGHT_PT - lu.cfg.page.top_margin_pt - lu.cfg.page.bottom_margin_pt
    return new_image(lu.px(page_h_pt))