from PIL import ImageFont

from tabfromtext.render.LayoutConfig import LayoutConfig
from tabfromtext.util.TimeUtils import TIME_RESOLUTION

MEASURES_PER_LINE = 4
UNITS_PER_MEASURE = 8 * TIME_RESOLUTION


class LayoutUtils:
    """Converts LayoutConfig pt values to pixels and provides all coordinate
    calculations used during rendering. A single LayoutUtils instance is
    created once per render pass and shared across all painters.

    Pixel conversion
    ────────────────
    All pt → px conversions go through px() so the DPI/scale factor is
    applied in exactly one place. lw() is the same but clamps to ≥ 1 so
    line widths are always visible.

    Tick → coordinate helpers
    ─────────────────────────
    A "tick" is the smallest time unit (TIME_RESOLUTION ticks per eighth note).
    Every horizontal and vertical position in the tab is derived from a tick
    value plus a base_y (top of the segment's first system row).
    """

    def __init__(self, cfg: LayoutConfig) -> None:
        self.cfg = cfg

        # --- Derived pt values (computed once) ---
        self._measure_width_pt      = (UNITS_PER_MEASURE * cfg.notes.eighth_note_width_pt) + cfg.notes.bar_padding_pt
        self._line_content_width_pt = MEASURES_PER_LINE * self._measure_width_pt
        self._natural_width_pt      = (self._line_content_width_pt
                                       + cfg.page.margin_left_pt + cfg.page.margin_right_pt)

        # --- Scale: maps natural pt layout to actual printable width ---
        self.scale: float = (cfg.printable_width_pt / self._natural_width_pt
                             if cfg.printable_width_pt > 0 else 1.0)

        # --- Frequently used px values (computed once) ---
        self.margin_left_px   = self.px(cfg.page.margin_left_pt)
        self.margin_right_px  = self.px(cfg.page.margin_right_pt)
        self.line_sp_px       = self.px(cfg.row.line_spacing_pt)
        self.beat_w_px        = self.px(cfg.notes.eighth_note_width_pt)
        self.bar_pad_px       = self.px(cfg.notes.bar_padding_pt)
        self.measure_w_px     = self.px(self._measure_width_pt)
        self.content_w_px     = self.px(self._line_content_width_pt)
        self.img_width_px     = self.content_w_px + self.margin_left_px + self.margin_right_px
        self.title_h_px       = self.px(cfg.fonts.title_pt + cfg.page.title_padding_pt)
        self.system_h_px      = self.px(cfg.row.above_strings_pt
                                        + 5 * cfg.row.line_spacing_pt
                                        + cfg.row.below_strings_pt)
        self.above_str_px     = self.px(cfg.row.above_strings_pt)
        self.below_str_px     = self.px(cfg.row.below_strings_pt)
        self.string_block_px  = self.px(5 * cfg.row.line_spacing_pt)

    # ------------------------------------------------------------------
    # Basic unit converters
    # ------------------------------------------------------------------

    def px(self, pt: float) -> int:
        """Convert a pt value to pixels using DPI and scale."""
        return round(pt * self.scale * self.cfg.dpi / 72)

    def lw(self, pt: float) -> int:
        """Convert a pt line-width to pixels, clamped to minimum 1."""
        return max(1, self.px(pt))

    # ------------------------------------------------------------------
    # Tick → position helpers
    # ------------------------------------------------------------------

    def tick_to_system(self, tick: int) -> int:
        """Which system row (0-based) does this tick fall in?"""
        return int(tick // (UNITS_PER_MEASURE * MEASURES_PER_LINE))

    def tick_to_measure_in_system(self, tick: int) -> int:
        """Which measure within the system (0-based) does this tick fall in?"""
        total_measures = tick // UNITS_PER_MEASURE
        return int(total_measures % MEASURES_PER_LINE)

    def tick_to_unit_in_measure(self, tick: int) -> int:
        """How many ticks into the current measure is this tick?"""
        return tick % UNITS_PER_MEASURE

    def is_new_system(self, tick: int) -> bool:
        """True if this tick is the first tick of a new system row."""
        return tick % (UNITS_PER_MEASURE * MEASURES_PER_LINE) == 0

    def is_new_measure(self, tick: int) -> bool:
        """True if this tick is the first tick of a new measure."""
        return tick % UNITS_PER_MEASURE == 0

    def tick_to_x(self, tick: int) -> int:
        """Pixel x coordinate for a given tick (left edge of the note)."""
        measure = self.tick_to_measure_in_system(tick)
        unit    = self.tick_to_unit_in_measure(tick)
        return (self.margin_left_px
                + measure * self.measure_w_px
                + unit    * self.beat_w_px
                + self.bar_pad_px)

    def tick_to_strings_y(self, tick: int, base_y: int) -> int:
        """Pixel y coordinate of the 1st string line for the system that
        contains *tick*. base_y is the top of the segment's first system."""
        system = self.tick_to_system(tick)
        return base_y + system * self.system_h_px + self.above_str_px

    def tick_to_stem_y(self, tick: int, base_y: int) -> int:
        """Pixel y coordinate where stems start (just below the 6th string)."""
        return self.tick_to_strings_y(tick, base_y) + 6 * self.line_sp_px

    def barline_x(self, tick: int) -> int:
        """Pixel x of the barline at the start of the measure containing tick."""
        measure = self.tick_to_measure_in_system(tick)
        return self.margin_left_px + measure * self.measure_w_px

    # ------------------------------------------------------------------
    # Font loading
    # ------------------------------------------------------------------

    def load_fonts(self):
        """Load and return all fonts used during rendering.

        Returns (title_font, fret_font, small_font, string_name_font,
                 annotation_font, lyrics_font, lyrics_tab_font).
        Falls back to PIL's default bitmap font if TrueType files are
        unavailable.
        """
        try:
            title_font       = ImageFont.truetype("arialbd.ttf", self.px(self.cfg.fonts.title_pt))
            fret_font        = ImageFont.truetype("arial.ttf",   self.px(self.cfg.fonts.fret_pt))
            small_font       = ImageFont.truetype("arial.ttf",   self.px(self.cfg.fonts.measure_num_pt))
            string_name_font = ImageFont.truetype("arial.ttf",   self.px(self.cfg.fonts.string_name_pt))
            annotation_font  = ImageFont.truetype("arial.ttf",   self.px(self.cfg.fonts.annotation_pt))
            lyrics_font      = ImageFont.truetype("arial.ttf",   self.px(self.cfg.fonts.lyrics_pt))
            lyrics_tab_font  = ImageFont.truetype("arial.ttf",   self.px(self.cfg.fonts.lyrics_tab_pt))
        except Exception:
            default = ImageFont.load_default()
            title_font = fret_font = small_font = string_name_font = \
                annotation_font = lyrics_font = lyrics_tab_font = default
        return (title_font, fret_font, small_font, string_name_font,
                annotation_font, lyrics_font, lyrics_tab_font)