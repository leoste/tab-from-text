from dataclasses import dataclass
from PIL import ImageFont


@dataclass
class LayoutConfig:
    """All values are pt as they appear on the final printed page (1pt = 1/72 inch).
    Pixels are only used at the px() / lw() call site. The scale factor
    (printable_width / natural_image_width) is applied there and nowhere else.

    TAB ROW ANATOMY
    ───────────────
        ┌─ above_strings_pt ─┐  ← measure numbers, P.M., annotations
        │  1st string line   │
        │  ...               │  5 × line_spacing_pt
        │  6th string line   │
        └─ below_strings_pt ─┘  ← stems, beams, dots
    system_height_pt  = above_strings_pt + 5×line_spacing_pt + below_strings_pt
    title_height_pt   = title_font_size_pt + title_padding_pt
    """

    dpi: int = 300

    # --- Fonts ---
    title_font_size_pt:        float = 12
    fret_font_size_pt:         float = 6
    annotation_font_size_pt:   float = 4   # P.M. and other staff annotations
    measure_num_font_size_pt:  float = 4
    string_name_font_size_pt:  float = 4
    footer_font_size_pt:       float = 10   # page number, song title, instrument name
    lyrics_font_size_pt:       float = 12   # lyrics on the title page

    # --- Inline tab lyrics ---
    # lyrics_y_offset_pt: vertical distance from the 6th string line downward
    # to the baseline of the inline lyric text.
    lyrics_y_offset_pt:        float = 18.0
    lyrics_tab_font_size_pt:   float = 6.0

    # --- String lines ---
    line_spacing_pt:    float = 6    # gap between adjacent string lines
    above_strings_pt:   float = 12   # space above 1st string (annotations live here)
    below_strings_pt:   float = 22   # space below 6th string (stems live here) use 36 for text

    # --- Title block ---
    title_padding_pt:   float = 8.0    # gap between title baseline and first system

    # --- Horizontal layout ---
    eighth_note_width_pt: float = 6.0  # per tick; one eighth note = 2 ticks = 2 × this
    bar_padding_pt:       float = 8.0  # gap at start of each measure before first note
    margin_left_pt:       float = 64   # includes former 2cm page margin (56.7pt) + 18pt content indent
    margin_right_pt:      float = 64

    # --- Page layout ---
    block_gap_pt:            float = 0.0    # vertical gap between stacked segment images
    page_top_margin_pt:      float = 34.0
    page_bottom_margin_pt:   float = 64.0
    footer_margin_pt:        float = 64.0   # horizontal indent for footer text (keep in sync with margin_left_pt)

    # --- Stems ---
    stem_h_pt:          float = 8
    stem_x_offset_pt:   float = 1.0   # how far right of note x the stem is drawn

    # --- Beams & dots ---
    beam_stub_pt:       float = 2    # flag stub on an unbeamed eighth note
    dot_offset_pt:      float = 2
    dot_r_pt:           float = 0.5

    # --- Arcs (ties / slides) ---
    arc_top_offset_pt:  float = 6   # how far above y_top the arc peaks
    arc_bot_offset_pt:  float = 2   # how close to y_top the arc base sits
    slide_nudge_pt:     float = 2   # gap between fret number and slide line/arc

    # --- P.M. annotation ---
    pm_y_offset_pt:     float = -6.0  # offset from 1st string line upward
    pm_label_y_pt:      float = 2   # label baseline offset above pm_y
    pm_label_w_pt:      float = 8   # width of "P.M." text (where dashed line starts)
    dash_gap_pt:        float = 2   # dash length (inter-dash gap is also this value)
    tick_h_pt:          float = 2   # half-height of the P.M. end tick

    # --- Measure numbers ---
    measure_num_y_offset_pt: float = -12.0  # offset from top of system upward

    # --- String names ---
    string_name_x_pt:   float = 4   # gap between string name letter and the left barline

    # --- Line widths ---
    line_width_thin_pt:   float = 0.25
    line_width_normal_pt: float = 0.5
    line_width_thick_pt:  float = 1

    # --- Page geometry (set by TabPrinter) ---
    printable_width_pt: float = 0.0



    @property
    def string_block_pt(self) -> float: return 5 * self.line_spacing_pt
    @property
    def system_height_pt(self) -> float: return self.above_strings_pt + self.string_block_pt + self.below_strings_pt

    @property
    def title_height_pt(self) -> float: return self.title_font_size_pt + self.title_padding_pt

    @property
    def half_top_h_pt(self):    return self.stem_h_pt * 0.5
    @property
    def half_gap_pt(self):      return self.stem_h_pt * 1.0
    @property
    def half_bottom_h_pt(self): return self.stem_h_pt * 1.5
    @property
    def full_h_pt(self):        return self.stem_h_pt * 3.0

    @property
    def _natural_width_pt(self) -> float:
        UNITS_PER_MEASURE = 16   # 8 beats × TIME_RESOLUTION=2
        MEASURES_PER_LINE = 4
        content = MEASURES_PER_LINE * (UNITS_PER_MEASURE * self.eighth_note_width_pt + self.bar_padding_pt)
        return content + self.margin_left_pt + self.margin_right_pt

    @property
    def scale(self) -> float:
        if self.printable_width_pt <= 0:
            return 1.0
        return self.printable_width_pt / self._natural_width_pt

    def px(self, pt: float) -> int:
        return round(pt * self.scale * self.dpi / 72)

    def lw(self, pt: float) -> int:
        return max(1, self.px(pt))

    def load_fonts(self):
        try:
            title_font       = ImageFont.truetype("arialbd.ttf", self.px(self.title_font_size_pt))
            fret_font        = ImageFont.truetype("arial.ttf",   self.px(self.fret_font_size_pt))
            small_font       = ImageFont.truetype("arial.ttf",   self.px(self.measure_num_font_size_pt))
            string_name_font = ImageFont.truetype("arial.ttf",   self.px(self.string_name_font_size_pt))
            annotation_font  = ImageFont.truetype("arial.ttf",   self.px(self.annotation_font_size_pt))
            lyrics_font      = ImageFont.truetype("arial.ttf",   self.px(self.lyrics_font_size_pt))
            lyrics_tab_font  = ImageFont.truetype("arial.ttf",   self.px(self.lyrics_tab_font_size_pt))
        except Exception:
            default = ImageFont.load_default()
            title_font = fret_font = small_font = string_name_font = annotation_font = lyrics_font = default
            lyrics_tab_font = default
        return title_font, fret_font, small_font, string_name_font, annotation_font, lyrics_font, lyrics_tab_font