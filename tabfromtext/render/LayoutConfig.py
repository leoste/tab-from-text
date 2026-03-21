from dataclasses import dataclass, field
from reportlab.lib.pagesizes import A4

A4_WIDTH_PT = A4[0]


@dataclass
class FontConfig:
    title_pt:        float = 12
    fret_pt:         float = 6
    annotation_pt:   float = 4   # P.M. and other staff annotations
    measure_num_pt:  float = 4
    string_name_pt:  float = 4
    footer_pt:       float = 10  # page number, song title, instrument name
    lyrics_pt:       float = 12  # lyrics on the title page
    lyrics_tab_pt:   float = 6.0


@dataclass
class RowConfig:
    """A row is one system of six string lines.

    ROW ANATOMY
    ───────────
        ┌─ above_strings_pt ─┐  ← measure numbers, P.M., annotations
        │  1st string line   │
        │  ...               │  5 × line_spacing_pt
        │  6th string line   │
        └─ below_strings_pt ─┘  ← stems, beams, dots
    row_height = above_strings_pt + 5×line_spacing_pt + below_strings_pt
    """
    line_spacing_pt:    float = 6
    above_strings_pt:   float = 6    # space above 1st string (annotations live here)
    below_strings_pt:   float = 28   # space below 6th string (stems and lyrics live here)
    string_name_x_pt:   float = 4    # gap between string name letter and the left barline


@dataclass
class NoteConfig:
    eighth_note_width_pt: float = 6.0  # per tick; one eighth note = 2 ticks = 2 × this
    bar_padding_pt:       float = 8.0  # gap at start of each measure before first note
    rest_stem_pt:         float = 2.0  # height of the stem drawn for silent notes


@dataclass
class StemConfig:
    h_pt:        float = 8
    x_offset_pt: float = 1.0   # how far right of note x the stem is drawn


@dataclass
class BeamConfig:
    stub_pt:       float = 2    # flag stub on an unbeamed eighth note
    dot_offset_pt: float = 2
    dot_r_pt:      float = 0.5
    beam_gap_pt:   float = 2  # vertical gap between bottom and top beam (sixteenth)


@dataclass
class ArcConfig:
    """Ties and slides."""
    top_offset_pt:  float = 6   # how far above y_top the arc peaks
    bot_offset_pt:  float = 2   # how close to y_top the arc base sits
    slide_nudge_pt: float = 2   # gap between fret number and slide line/arc


@dataclass
class PalmMuteConfig:
    y_offset_pt:  float = -6.0  # offset from 1st string line upward
    label_y_pt:   float = 2     # label baseline offset above pm_y
    label_w_pt:   float = 8     # width of "P.M." text (where dashed line starts)
    dash_gap_pt:  float = 2     # dash length (inter-dash gap is also this value)
    tick_h_pt:    float = 2     # half-height of the P.M. end tick


@dataclass
class VibratoConfig:
    y_offset_pt:   float = -4.0  # offset from 1st string line upward (sits above P.M. line)
    wave_w_pt:     float = 3.0   # width of one half-wave cycle
    wave_h_pt:     float = 1.5   # amplitude (peak-to-trough half-height)
    tick_h_pt:     float = 2     # half-height of the closing end tick


@dataclass
class MeasureConfig:
    num_y_offset_pt: float = -12.0  # offset from top of system upward


@dataclass
class LyricsConfig:
    y_offset_pt: float = 18.0   # vertical distance from the 6th string line downward to lyric baseline


@dataclass
class LineWidthConfig:
    thin_pt:   float = 0.25
    normal_pt: float = 0.5
    thick_pt:  float = 1.0


@dataclass
class PageConfig:
    top_margin_pt:    float = 34.0
    bottom_margin_pt: float = 64.0
    footer_margin_pt: float = 64.0   # horizontal indent for footer text
    margin_left_pt:   float = 64     # includes former 2cm page margin (56.7pt) + 18pt content indent
    margin_right_pt:  float = 64
    block_gap_pt:     float = 0.0    # vertical gap between stacked segment images
    title_padding_top_pt: float = 8.0   # gap above the title text
    title_padding_bot_pt: float = 12.0  # gap between title baseline and first system
    printable_width_pt: float = A4_WIDTH_PT


@dataclass
class LayoutConfig:
    dpi: int = 300

    fonts:      FontConfig      = field(default_factory=FontConfig)
    row:        RowConfig       = field(default_factory=RowConfig)
    notes:      NoteConfig      = field(default_factory=NoteConfig)
    stems:      StemConfig      = field(default_factory=StemConfig)
    beams:      BeamConfig      = field(default_factory=BeamConfig)
    arcs:       ArcConfig       = field(default_factory=ArcConfig)
    palm_mute:  PalmMuteConfig  = field(default_factory=PalmMuteConfig)
    vibrato:    VibratoConfig   = field(default_factory=VibratoConfig)
    measures:   MeasureConfig   = field(default_factory=MeasureConfig)
    lyrics:     LyricsConfig    = field(default_factory=LyricsConfig)
    line_width: LineWidthConfig = field(default_factory=LineWidthConfig)
    page:       PageConfig      = field(default_factory=PageConfig)