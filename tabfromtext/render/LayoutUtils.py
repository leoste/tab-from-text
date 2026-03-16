"""Layout calculations and pixel conversion for tab rendering.

All values are derived once from LayoutConfig at import time.
Consumers import individual functions or constants directly:

    from tabfromtext.render.LayoutUtils import px, tick_to_x, margin_left_px
"""
from PIL import ImageFont
from tabfromtext.render.LayoutConfig import LayoutConfig
from tabfromtext.util.TimeUtils import TIME_RESOLUTION

# ---------------------------------------------------------------------------
# Config and derived constants
# ---------------------------------------------------------------------------

_cfg = LayoutConfig()

MEASURES_PER_LINE = 4
UNITS_PER_MEASURE = 8 * TIME_RESOLUTION

_measure_width_pt      = (UNITS_PER_MEASURE * _cfg.notes.eighth_note_width_pt) + _cfg.notes.bar_padding_pt
_line_content_width_pt = MEASURES_PER_LINE * _measure_width_pt
_natural_width_pt      = _line_content_width_pt + _cfg.page.margin_left_pt + _cfg.page.margin_right_pt

scale: float = (_cfg.page.printable_width_pt / _natural_width_pt
                if _cfg.page.printable_width_pt > 0 else 1.0)

# ---------------------------------------------------------------------------
# Pixel conversion
# ---------------------------------------------------------------------------

def px(pt: float) -> int:
    """Convert a pt value to pixels using DPI and scale."""
    return round(pt * scale * _cfg.dpi / 72)


def lw(pt: float) -> int:
    """Convert a pt line-width to pixels, clamped to minimum 1."""
    return max(1, px(pt))


# ---------------------------------------------------------------------------
# Frequently used px constants (computed once)
# ---------------------------------------------------------------------------

cfg             = _cfg   # exposed for consumers that need raw config values
margin_left_px  = px(_cfg.page.margin_left_pt)
margin_right_px = px(_cfg.page.margin_right_pt)
line_sp_px      = px(_cfg.row.line_spacing_pt)
beat_w_px       = px(_cfg.notes.eighth_note_width_pt)
bar_pad_px      = px(_cfg.notes.bar_padding_pt)
measure_w_px    = px(_measure_width_pt)
content_w_px    = px(_line_content_width_pt)
img_width_px    = content_w_px + margin_left_px + margin_right_px
title_h_px      = px(_cfg.fonts.title_pt + _cfg.page.title_padding_pt)
system_h_px     = px(_cfg.row.above_strings_pt + 5 * _cfg.row.line_spacing_pt + _cfg.row.below_strings_pt)
above_str_px    = px(_cfg.row.above_strings_pt)
below_str_px    = px(_cfg.row.below_strings_pt)
string_block_px = px(5 * _cfg.row.line_spacing_pt)

# ---------------------------------------------------------------------------
# Fonts (loaded once)
# ---------------------------------------------------------------------------

try:
    title_font       = ImageFont.truetype("arialbd.ttf", px(_cfg.fonts.title_pt))
    fret_font        = ImageFont.truetype("arial.ttf",   px(_cfg.fonts.fret_pt))
    small_font       = ImageFont.truetype("arial.ttf",   px(_cfg.fonts.measure_num_pt))
    string_name_font = ImageFont.truetype("arial.ttf",   px(_cfg.fonts.string_name_pt))
    annotation_font  = ImageFont.truetype("arial.ttf",   px(_cfg.fonts.annotation_pt))
    lyrics_font      = ImageFont.truetype("arial.ttf",   px(_cfg.fonts.lyrics_pt))
    lyrics_tab_font  = ImageFont.truetype("arial.ttf",   px(_cfg.fonts.lyrics_tab_pt))
except Exception:
    _default = ImageFont.load_default()
    title_font = fret_font = small_font = string_name_font = \
        annotation_font = lyrics_font = lyrics_tab_font = _default

# ---------------------------------------------------------------------------
# Tick → position helpers
# ---------------------------------------------------------------------------

def tick_to_system(tick: int) -> int:
    """Which system row (0-based) does this tick fall in?"""
    return int(tick // (UNITS_PER_MEASURE * MEASURES_PER_LINE))


def tick_to_measure_in_system(tick: int) -> int:
    """Which measure within the system (0-based) does this tick fall in?"""
    return int((tick // UNITS_PER_MEASURE) % MEASURES_PER_LINE)


def tick_to_unit_in_measure(tick: int) -> int:
    """How many ticks into the current measure is this tick?"""
    return tick % UNITS_PER_MEASURE


def is_new_system(tick: int) -> bool:
    """True if this tick is the first tick of a new system row."""
    return tick % (UNITS_PER_MEASURE * MEASURES_PER_LINE) == 0


def is_new_measure(tick: int) -> bool:
    """True if this tick is the first tick of a new measure."""
    return tick % UNITS_PER_MEASURE == 0


def tick_to_x(tick: int) -> int:
    """Pixel x coordinate for a given tick (left edge of the note)."""
    measure = tick_to_measure_in_system(tick)
    unit    = tick_to_unit_in_measure(tick)
    return margin_left_px + measure * measure_w_px + unit * beat_w_px + bar_pad_px


def tick_to_strings_y(tick: int, base_y: int) -> int:
    """Pixel y of the 1st string line for the system containing tick."""
    return base_y + tick_to_system(tick) * system_h_px + above_str_px


def tick_to_stem_y(tick: int, base_y: int) -> int:
    """Pixel y where stems start (just below the 6th string)."""
    return tick_to_strings_y(tick, base_y) + 6 * line_sp_px


def barline_x(tick: int) -> int:
    """Pixel x of the barline at the start of the measure containing tick."""
    return margin_left_px + tick_to_measure_in_system(tick) * measure_w_px