from dataclasses import dataclass
from PIL import ImageFont


# The original pixel constants were authored at this DPI.
# All _base pt values are derived as:  pt = original_px * 72 / ORIGINAL_DPI
ORIGINAL_DPI = 96


@dataclass
class LayoutConfig:
    # --- Rendering resolution ---
    dpi: int = 300

    # --- Base font sizes (pt) ---
    _fret_font_size_pt: float         = 26  * 72 / ORIGINAL_DPI   # 19.5
    _title_font_size_pt: float        = 46  * 72 / ORIGINAL_DPI   # 34.5
    _measure_num_font_size_pt: float  = 16  * 72 / ORIGINAL_DPI   # 12.0
    _string_name_font_size_pt: float  = 16  * 72 / ORIGINAL_DPI   # 12.0  (same as measure num)

    # --- Base staff geometry (pt) ---
    _line_spacing_pt: float   = 30   * 72 / ORIGINAL_DPI   # 22.5
    _beat_width_pt: float     = 27.5 * 72 / ORIGINAL_DPI   # 20.625  (55px / TIME_RESOLUTION=2)
    _bar_padding_pt: float    = 25   * 72 / ORIGINAL_DPI   # 18.75
    _margin_left_pt: float    = 80   * 72 / ORIGINAL_DPI   # 60.0
    _margin_right_pt: float   = 80   * 72 / ORIGINAL_DPI   # 60.0

    # --- Base section heights (pt) ---
    _title_height_pt: float   = 120  * 72 / ORIGINAL_DPI   # 90.0
    _system_height_pt: float  = 340  * 72 / ORIGINAL_DPI   # 255.0  (6*30 + 160 = 340px)

    # --- Base annotation geometry (pt) ---
    _pm_y_offset_pt: float          = -25 * 72 / ORIGINAL_DPI   # -18.75
    _dash_gap_pt: float             =   5 * 72 / ORIGINAL_DPI   #   3.75
    _tick_h_pt: float               =   8 * 72 / ORIGINAL_DPI   #   6.0
    _measure_num_y_offset_pt: float = -50 * 72 / ORIGINAL_DPI   # -37.5

    # --- Base stem height (pt) ---
    _stem_h_pt: float         = 30  * 72 / ORIGINAL_DPI    # 22.5

    # --- Base small layout offsets (pt) ---
    _top_padding_pt: float    = 40  * 72 / ORIGINAL_DPI    # 30.0
    _bottom_padding_pt: float = 60  * 72 / ORIGINAL_DPI    # 45.0
    _pm_label_y_pt: float     = 12  * 72 / ORIGINAL_DPI    #  9.0
    _pm_label_w_pt: float     = 35  * 72 / ORIGINAL_DPI    # 26.25
    _dot_offset_pt: float     =  8  * 72 / ORIGINAL_DPI    #  6.0
    _dot_r_pt: float          =  2  * 72 / ORIGINAL_DPI    #  1.5
    _beam_stub_pt: float      = 12  * 72 / ORIGINAL_DPI    #  9.0
    _string_name_x_pt: float  = 20  * 72 / ORIGINAL_DPI    # 15.0

    # --- Stem x offset from note x (pt) ---
    _stem_x_offset_pt: float  =  4  * 72 / ORIGINAL_DPI    #  3.0

    # --- Arc bounding box offsets above y_top anchor (pt) ---
    _arc_top_offset_pt: float = 20  * 72 / ORIGINAL_DPI    # 15.0
    _arc_bot_offset_pt: float =  5  * 72 / ORIGINAL_DPI    #  3.75

    # --- Slide decoration nudge (pt) ---
    _slide_nudge_pt: float    =  5  * 72 / ORIGINAL_DPI    #  3.75

    # --- Base line widths (pt) ---
    _line_width_thin_pt: float   = 1 * 72 / ORIGINAL_DPI   # 0.75
    _line_width_normal_pt: float = 2 * 72 / ORIGINAL_DPI   # 1.5
    _line_width_thick_pt: float  = 4 * 72 / ORIGINAL_DPI   # 3.0

    # --- Page printable width (pt) — set by TabPrinter; drives the scale factor ---
    printable_width_pt: float = 0.0

    # ------------------------------------------------------------------
    # Scale factor: ratio of printable width to the natural image width.
    # When printable_width_pt is 0 (not set), scale is 1.0 (no scaling).
    # ------------------------------------------------------------------
    @property
    def _natural_width_pt(self) -> float:
        UNITS_PER_MEASURE = 16   # 8 * TIME_RESOLUTION=2
        MEASURES_PER_LINE = 4
        content = MEASURES_PER_LINE * (UNITS_PER_MEASURE * self._beat_width_pt + self._bar_padding_pt)
        return content + self._margin_left_pt + self._margin_right_pt

    @property
    def scale(self) -> float:
        if self.printable_width_pt <= 0:
            return 1.0
        return self.printable_width_pt / self._natural_width_pt

    # ------------------------------------------------------------------
    # Public scaled geometry — these are what TabRenderer uses.
    # ------------------------------------------------------------------
    @property
    def fret_font_size_pt(self):          return self._fret_font_size_pt          * self.scale
    @property
    def title_font_size_pt(self):         return self._title_font_size_pt         * self.scale
    @property
    def measure_num_font_size_pt(self):   return self._measure_num_font_size_pt   * self.scale
    @property
    def string_name_font_size_pt(self):   return self._string_name_font_size_pt   * self.scale
    @property
    def line_spacing_pt(self):            return self._line_spacing_pt            * self.scale
    @property
    def beat_width_pt(self):              return self._beat_width_pt              * self.scale
    @property
    def bar_padding_pt(self):             return self._bar_padding_pt             * self.scale
    @property
    def margin_left_pt(self):             return self._margin_left_pt             * self.scale
    @property
    def margin_right_pt(self):            return self._margin_right_pt            * self.scale
    @property
    def title_height_pt(self):            return self._title_height_pt            * self.scale
    @property
    def system_height_pt(self):           return self._system_height_pt           * self.scale
    @property
    def pm_y_offset_pt(self):             return self._pm_y_offset_pt             * self.scale
    @property
    def dash_gap_pt(self):                return self._dash_gap_pt                * self.scale
    @property
    def tick_h_pt(self):                  return self._tick_h_pt                  * self.scale
    @property
    def measure_num_y_offset_pt(self):    return self._measure_num_y_offset_pt    * self.scale
    @property
    def stem_h_pt(self):                  return self._stem_h_pt                  * self.scale
    @property
    def top_padding_pt(self):             return self._top_padding_pt             * self.scale
    @property
    def bottom_padding_pt(self):          return self._bottom_padding_pt          * self.scale
    @property
    def pm_label_y_pt(self):              return self._pm_label_y_pt              * self.scale
    @property
    def pm_label_w_pt(self):              return self._pm_label_w_pt              * self.scale
    @property
    def dot_offset_pt(self):              return self._dot_offset_pt              * self.scale
    @property
    def dot_r_pt(self):                   return self._dot_r_pt                   * self.scale
    @property
    def beam_stub_pt(self):               return self._beam_stub_pt               * self.scale
    @property
    def string_name_x_pt(self):           return self._string_name_x_pt          * self.scale
    @property
    def stem_x_offset_pt(self):           return self._stem_x_offset_pt          * self.scale
    @property
    def arc_top_offset_pt(self):          return self._arc_top_offset_pt         * self.scale
    @property
    def arc_bot_offset_pt(self):          return self._arc_bot_offset_pt         * self.scale
    @property
    def slide_nudge_pt(self):             return self._slide_nudge_pt            * self.scale
    @property
    def line_width_thin_pt(self):         return self._line_width_thin_pt         * self.scale
    @property
    def line_width_normal_pt(self):       return self._line_width_normal_pt       * self.scale
    @property
    def line_width_thick_pt(self):        return self._line_width_thick_pt        * self.scale

    # --- Derived stem sub-heights ---
    @property
    def half_top_h_pt(self):    return self.stem_h_pt * 0.5
    @property
    def half_gap_pt(self):      return self.stem_h_pt * 1.0
    @property
    def half_bottom_h_pt(self): return self.stem_h_pt * 1.5
    @property
    def full_h_pt(self):        return self.stem_h_pt * 3.0

    def px(self, pt: float) -> int:
        """Convert pt to whole pixels at self.dpi."""
        return round(pt * self.dpi / 72)

    def lw(self, pt: float) -> int:
        """Convert a line-width pt value to pixels, minimum 1."""
        return max(1, self.px(pt))

    def load_fonts(self):
        """Load fonts at the configured (scaled) sizes.
        Returns (title_font, fret_font, small_font, string_name_font)."""
        try:
            title_font       = ImageFont.truetype("arialbd.ttf", self.px(self.title_font_size_pt))
            fret_font        = ImageFont.truetype("arial.ttf",   self.px(self.fret_font_size_pt))
            small_font       = ImageFont.truetype("arial.ttf",   self.px(self.measure_num_font_size_pt))
            string_name_font = ImageFont.truetype("arial.ttf",   self.px(self.string_name_font_size_pt))
        except Exception:
            default = ImageFont.load_default()
            title_font = fret_font = small_font = string_name_font = default
        return title_font, fret_font, small_font, string_name_font