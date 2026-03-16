import math
from dataclasses import dataclass
from PIL import Image, ImageDraw
from tabfromtext.song.StrumStyle import StrumStyle
from tabfromtext.song.Segment import Segment
from tabfromtext.song.Song import Song
from tabfromtext.render.LayoutConfig import LayoutConfig
from tabfromtext.render.LayoutUtils import LayoutUtils, UNITS_PER_MEASURE, MEASURES_PER_LINE
from tabfromtext.util.TimeUtils import convertTimeToTicks, TIME_RESOLUTION

TICKS_SIXTEENTH     = TIME_RESOLUTION // 2
TICKS_DOTTED_EIGHTH = TICKS_SIXTEENTH * 3
TICKS_EIGHTH        = 1 * TIME_RESOLUTION
TICKS_HALF_NOTE     = 4 * TIME_RESOLUTION
TICKS_FULL_NOTE     = 8 * TIME_RESOLUTION

# Module-level rendering state — initialised once per render_tab / render_title_page call.
_utils:           LayoutUtils = None
_title_font       = None
_fret_font        = None
_small_font       = None
_string_name_font = None
_annotation_font  = None
_lyrics_font      = None
_lyrics_tab_font  = None


def _init_render(cfg: LayoutConfig) -> None:
    """Initialise module-level utils and fonts from the given config."""
    global _utils, _title_font, _fret_font, _small_font
    global _string_name_font, _annotation_font, _lyrics_font, _lyrics_tab_font
    _utils = LayoutUtils(cfg)
    (_title_font, _fret_font, _small_font,
     _string_name_font, _annotation_font,
     _lyrics_font, _lyrics_tab_font) = _utils.load_fonts()


def is_dotted(duration):
    if duration <= 0:
        return False
    doubled = duration * 2
    if doubled % 3 != 0:
        return False
    base = doubled // 3
    return base > 0 and (base & (base - 1)) == 0


# ---------------------------------------------------------------------------
# Contexts
# ---------------------------------------------------------------------------

@dataclass
class NoteContext:
    """Everything known about a note at the outer loop level."""
    note:           object   # the Note object
    idx:            int      # index in segment_notes
    segment_notes:  list
    tick:           int      # absolute tick of note start
    strings_y:      int      # y of 1st string in this note's system row
    x:              int      # left edge x of the note
    next_x:         int      # x after the note's full duration
    is_new_line:    bool
    # neighbours for beam decisions (resolved once per note, not per chunk)
    prev_real_note: object
    next_real_note: object
    # mutable palm-mute threading state
    last_style:     object
    last_pm_x:      object   # int | None
    last_pm_y:      object   # int | None


@dataclass
class ChunkContext:
    """Everything known about one chunk of a (possibly split) note."""
    acc:         int   # absolute tick of chunk start
    dur:         int   # duration of this chunk in ticks
    strings_y:   int   # y of 1st string in this chunk's system row
    stem_y:      int   # y where stems start (below 6th string)
    is_new_line: bool
    x:           int   # left edge x
    next_x:      int   # x after chunk duration
    stem_x:      int   # x of the stem
    is_first:    bool  # True for the first chunk of a note


# ---------------------------------------------------------------------------
# Row-level drawing — things that belong to a system of six string lines
# ---------------------------------------------------------------------------

def draw_row(draw_obj, y_top, start_measure_num):
    """Draw one complete system row: six string lines, opening barline,
    string names, and the measure number. y_top is the y of the 1st string."""
    cfg          = _utils.cfg
    string_names = ['e', 'B', 'G', 'D', 'A', 'E']
    font_h       = _utils.px(cfg.fonts.string_name_pt)
    mnum_y_off   = _utils.px(cfg.measures.num_y_offset_pt)

    for i, name in enumerate(string_names):
        y = y_top + i * _utils.line_sp_px
        draw_obj.text(
            (_utils.margin_left_px - _utils.px(cfg.row.string_name_x_pt) - font_h,
             y - font_h // 2),
            name, fill="black", font=_string_name_font,
        )
        draw_obj.line(
            [(_utils.margin_left_px, y),
             (_utils.margin_left_px + _utils.content_w_px, y)],
            fill=(200, 200, 200), width=_utils.lw(cfg.line_width.thin_pt),
        )

    draw_obj.line(
        [(_utils.margin_left_px, y_top),
         (_utils.margin_left_px, y_top + 5 * _utils.line_sp_px)],
        fill="black", width=_utils.lw(cfg.line_width.normal_pt),
    )
    draw_obj.text(
        (_utils.margin_left_px, y_top + mnum_y_off),
        str(start_measure_num), fill="gray", font=_small_font,
    )


def draw_barline(draw_obj, strings_y, bar_x, measure_num):
    """Draw a mid-row barline and its measure number label."""
    cfg = _utils.cfg
    draw_obj.line(
        [(bar_x, strings_y),
         (bar_x, strings_y + 5 * _utils.line_sp_px)],
        fill="black", width=_utils.lw(cfg.line_width.normal_pt),
    )
    draw_obj.text(
        (bar_x, strings_y + _utils.px(cfg.measures.num_y_offset_pt)),
        str(measure_num), fill="gray", font=_small_font,
    )


def draw_row_end_barline(draw_obj, strings_y):
    """Draw the closing barline at the right edge of a system row."""
    cfg = _utils.cfg
    draw_obj.line(
        [(_utils.margin_left_px + _utils.content_w_px, strings_y),
         (_utils.margin_left_px + _utils.content_w_px, strings_y + 5 * _utils.line_sp_px)],
        fill="black", width=_utils.lw(cfg.line_width.normal_pt),
    )


def draw_final_barline(draw_obj, final_x, final_y):
    """Draw the closing barline after the last note of a segment."""
    cfg = _utils.cfg
    draw_obj.line(
        [(final_x, final_y),
         (final_x, final_y + 5 * _utils.line_sp_px)],
        fill="black", width=_utils.lw(cfg.line_width.normal_pt),
    )


# ---------------------------------------------------------------------------
# Note-level drawing — everything that belongs to a single note event
# ---------------------------------------------------------------------------

def draw_note(draw_obj, note_ctx: NoteContext, chunk_ctx: ChunkContext,
              prev_stem_x, prev_stem_y_start):
    """Draw all visual elements for one note-chunk.
    Returns updated (last_pm_x, last_pm_y) for palm mute state threading.
    """
    last_pm_x = note_ctx.last_pm_x
    last_pm_y = note_ctx.last_pm_y

    if note_ctx.note.chord and note_ctx.note.style != StrumStyle.NO_HIT:
        last_pm_x, last_pm_y = _draw_fret_numbers(draw_obj, note_ctx, chunk_ctx)

    is_rest = (note_ctx.note.chord is None or note_ctx.note.style == StrumStyle.NO_HIT)
    _draw_stem(draw_obj, chunk_ctx, is_rest=is_rest)

    if chunk_ctx.is_first and is_dotted(note_ctx.note.duration):
        _draw_dot(draw_obj, chunk_ctx)

    if prev_stem_x is not None:
        draw_arc(draw_obj, prev_stem_x, chunk_ctx.stem_x,
                 min(prev_stem_y_start, chunk_ctx.stem_y))

    if chunk_ctx.dur in (TICKS_EIGHTH, TICKS_DOTTED_EIGHTH):
        _draw_beam(draw_obj, note_ctx, chunk_ctx)

    return last_pm_x, last_pm_y


def _draw_fret_numbers(draw_obj, note_ctx: NoteContext, chunk_ctx: ChunkContext):
    """Draw fret labels (or 'X') for each string, slide lines, and palm mute.
    Returns updated (last_pm_x, last_pm_y)."""
    note      = note_ctx.note
    strings   = [note.chord.string1, note.chord.string2, note.chord.string3,
                 note.chord.string4, note.chord.string5, note.chord.string6]
    last_pm_x = note_ctx.last_pm_x
    last_pm_y = note_ctx.last_pm_y

    for i, fret in enumerate(strings):
        if fret is not None and fret != -1:
            y     = chunk_ctx.strings_y + i * _utils.line_sp_px
            label = "X" if note.style == StrumStyle.MUTED else str(fret)

            text_w, text_h = draw_obj.textbbox((0, 0), label, font=_fret_font)[2:]
            draw_obj.rectangle(
                [chunk_ctx.x - 2,          y - text_h // 2,
                 chunk_ctx.x + text_w + 2, y + text_h // 2],
                fill="white",
            )
            draw_obj.text(
                (chunk_ctx.x, y - text_h // 2),
                label, fill="black", font=_fret_font,
            )

            if note.style == StrumStyle.SLIDE:
                _draw_slide(draw_obj, chunk_ctx, i, text_w)

    if note.style == StrumStyle.PALM_MUTED:
        last_pm_x, last_pm_y = _draw_palm_mute(draw_obj, note_ctx, chunk_ctx)

    return last_pm_x, last_pm_y


def _draw_slide(draw_obj, chunk_ctx: ChunkContext, string_index, text_w):
    """Draw the horizontal slide line and arc for one string."""
    cfg   = _utils.cfg
    nudge = _utils.px(cfg.arcs.slide_nudge_pt)
    y     = chunk_ctx.strings_y + string_index * _utils.line_sp_px
    draw_obj.line(
        [(chunk_ctx.x + text_w + nudge, y),
         (chunk_ctx.next_x - nudge, y)],
        fill="black", width=_utils.lw(cfg.line_width.thin_pt),
    )
    draw_arc(draw_obj,
             chunk_ctx.x + nudge, chunk_ctx.next_x - nudge,
             chunk_ctx.strings_y + string_index * _utils.line_sp_px)


def _draw_palm_mute(draw_obj, note_ctx: NoteContext, chunk_ctx: ChunkContext):
    """Draw P.M. label, dashed continuation line, and closing tick.
    Returns updated (last_pm_x, last_pm_y)."""
    cfg  = _utils.cfg
    pm_y = chunk_ctx.strings_y + _utils.px(cfg.palm_mute.y_offset_pt)

    is_first_pm_on_line = (note_ctx.last_style != StrumStyle.PALM_MUTED
                           or note_ctx.last_pm_x is None)
    is_last_pm = (note_ctx.next_real_note is None
                  or note_ctx.next_real_note.style != StrumStyle.PALM_MUTED)

    if is_first_pm_on_line:
        draw_obj.text(
            (chunk_ctx.x, pm_y - _utils.px(cfg.palm_mute.label_y_pt)),
            "P.M.", fill="black", font=_annotation_font,
        )
        last_pm_x = chunk_ctx.x + _utils.px(cfg.palm_mute.label_w_pt)
    else:
        _draw_dashed_segment(draw_obj, note_ctx.last_pm_x, chunk_ctx.x, pm_y)
        last_pm_x = chunk_ctx.x

    if is_last_pm and not is_first_pm_on_line:
        tick_h = _utils.px(cfg.palm_mute.tick_h_pt)
        draw_obj.line(
            [(chunk_ctx.x, pm_y - tick_h // 2),
             (chunk_ctx.x, pm_y + tick_h // 2)],
            fill="black", width=_utils.lw(cfg.line_width.thin_pt),
        )

    return last_pm_x, pm_y


def _draw_stem(draw_obj, chunk_ctx: ChunkContext, is_rest: bool = False):
    """Draw the stem below the note."""
    cfg = _utils.cfg
    if is_rest:
        full_h = _utils.px(cfg.stems.h_pt)
        rest_h = _utils.px(cfg.notes.rest_stem_pt)
        draw_obj.line(
            [(chunk_ctx.stem_x, chunk_ctx.stem_y + full_h - rest_h),
             (chunk_ctx.stem_x, chunk_ctx.stem_y + full_h)],
            fill="black", width=_utils.lw(cfg.line_width.normal_pt),
        )
        return
    if chunk_ctx.dur >= TICKS_FULL_NOTE:
        draw_obj.line(
            [(chunk_ctx.stem_x, chunk_ctx.stem_y),
             (chunk_ctx.stem_x, chunk_ctx.stem_y + _utils.px(cfg.stems.h_pt * 3.0))],
            fill="black", width=_utils.lw(cfg.line_width.normal_pt),
        )
    elif chunk_ctx.dur >= TICKS_HALF_NOTE:
        top_h = _utils.px(cfg.stems.h_pt * 0.5)
        gap   = _utils.px(cfg.stems.h_pt * 1.0)
        bot_h = _utils.px(cfg.stems.h_pt * 1.5)
        draw_obj.line(
            [(chunk_ctx.stem_x, chunk_ctx.stem_y),
             (chunk_ctx.stem_x, chunk_ctx.stem_y + top_h)],
            fill="black", width=_utils.lw(cfg.line_width.normal_pt),
        )
        draw_obj.line(
            [(chunk_ctx.stem_x, chunk_ctx.stem_y + top_h + gap),
             (chunk_ctx.stem_x, chunk_ctx.stem_y + top_h + gap + bot_h)],
            fill="black", width=_utils.lw(cfg.line_width.normal_pt),
        )
    else:
        draw_obj.line(
            [(chunk_ctx.stem_x, chunk_ctx.stem_y),
             (chunk_ctx.stem_x, chunk_ctx.stem_y + _utils.px(cfg.stems.h_pt))],
            fill="black", width=_utils.lw(cfg.line_width.normal_pt),
        )


def _draw_dot(draw_obj, chunk_ctx: ChunkContext):
    """Draw the dot for a dotted-rhythm note."""
    cfg        = _utils.cfg
    dot_offset = _utils.px(cfg.beams.dot_offset_pt)
    dot_r      = _utils.px(cfg.beams.dot_r_pt)
    draw_obj.ellipse(
        [chunk_ctx.stem_x + dot_offset - dot_r, chunk_ctx.stem_y + dot_offset - dot_r,
         chunk_ctx.stem_x + dot_offset + dot_r, chunk_ctx.stem_y + dot_offset + dot_r],
        fill="black",
    )


def _draw_beam(draw_obj, note_ctx: NoteContext, chunk_ctx: ChunkContext):
    """Draw a beam connecting to the next note, or a stub flag if unbeamed."""
    cfg            = _utils.cfg
    chunk_bottom_y = chunk_ctx.stem_y + _utils.px(cfg.stems.h_pt)
    note           = note_ctx.note

    is_at_measure_end = _utils.is_new_measure(chunk_ctx.acc + chunk_ctx.dur)
    can_beam_fwd = (not is_at_measure_end
                    and note_ctx.next_real_note is not None
                    and note_ctx.next_real_note.duration == note.duration
                    and note.chord is not None
                    and note_ctx.next_real_note.chord is not None)

    is_at_measure_start = _utils.is_new_measure(chunk_ctx.acc)
    is_beamed_back = (not is_at_measure_start
                      and note_ctx.prev_real_note is not None
                      and note_ctx.prev_real_note.duration == note.duration
                      and note.chord is not None
                      and note_ctx.prev_real_note.chord is not None)

    if can_beam_fwd:
        draw_obj.line(
            [(chunk_ctx.stem_x, chunk_bottom_y),
             (chunk_ctx.stem_x + _utils.beat_w_px * chunk_ctx.dur, chunk_bottom_y)],
            fill="black", width=_utils.lw(cfg.line_width.thick_pt),
        )
    elif not is_beamed_back:
        draw_obj.line(
            [(chunk_ctx.stem_x, chunk_bottom_y),
             (chunk_ctx.stem_x + _utils.px(cfg.beams.stub_pt), chunk_bottom_y)],
            fill="black", width=_utils.lw(cfg.line_width.normal_pt),
        )


# ---------------------------------------------------------------------------
# Shared primitives
# ---------------------------------------------------------------------------

def draw_arc(draw_obj, x_start, x_end, y_top):
    cfg     = _utils.cfg
    top_off = _utils.px(cfg.arcs.top_offset_pt)
    bot_off = _utils.px(cfg.arcs.bot_offset_pt)
    arc_box = [x_start, y_top - top_off, x_end, y_top - bot_off]
    draw_obj.arc(arc_box, start=180, end=0, fill="black",
                 width=_utils.lw(cfg.line_width.thin_pt))


def _draw_dashed_segment(draw_obj, x_start, x_end, y):
    dash_gap = _utils.px(_utils.cfg.palm_mute.dash_gap_pt)
    curr = x_start
    while curr < x_end:
        draw_obj.line(
            [(curr, y), (min(curr + dash_gap, x_end), y)],
            fill="black", width=_utils.lw(_utils.cfg.line_width.thin_pt),
        )
        curr += dash_gap * 2


# ---------------------------------------------------------------------------
# Segment rendering — drives the row/note layers
# ---------------------------------------------------------------------------

def render_tab(segments: list[Segment], instrument_name: str,
               output_base_path: str = "guitar_tab",
               cfg: LayoutConfig = None) -> list[tuple[str, object]]:
    _init_render(cfg or LayoutConfig())

    results = []
    global_measure_counter = 1

    for seg_idx, segment in enumerate(segments):
        img, draw, base_y = _create_segment_image(segment, instrument_name)
        draw.text((_utils.margin_left_px, _utils.px(_utils.cfg.page.title_padding_pt)),
                  segment.title, fill="black", font=_title_font)

        segment_notes   = segment.GetNotesFromSegment(instrument_name)
        acc_dur_segment = 0
        last_style      = None
        last_pm_x       = None
        last_pm_y       = None
        final_x         = _utils.margin_left_px
        final_y         = base_y

        for idx, note in enumerate(segment_notes):
            note_ctx = _build_note_context(
                note, idx, segment_notes, acc_dur_segment, base_y,
                last_style, last_pm_x, last_pm_y,
            )

            if note.duration is not None:
                final_y = note_ctx.strings_y
                final_x = note_ctx.next_x
                last_pm_x, last_pm_y = _render_note(
                    draw, note_ctx, base_y, global_measure_counter,
                )
                global_measure_counter = _advance_measure_counter(
                    note, acc_dur_segment, global_measure_counter,
                )

            if note.style is not None:
                last_style = note.style
            acc_dur_segment += note.duration if note.duration else 0

        if not _utils.is_new_system(acc_dur_segment):
            draw_final_barline(draw, final_x, final_y)

        if segment.lyrics is not None:
            _draw_lyrics(draw, segment, base_y)

        safe_title = "".join(
            c for c in segment.title if c.isalnum() or c in (' ', '_')
        ).strip().replace(' ', '_')
        results.append((f"{output_base_path}_{seg_idx + 1}_{safe_title}.png", img))

    return results


def _create_segment_image(segment, instrument_name):
    """Allocate the PIL image for one segment and return (img, draw, base_y)."""
    cfg           = _utils.cfg
    segment_notes = segment.GetNotesFromSegment(instrument_name)
    total_units   = sum((n.duration if n.duration else 0) for n in segment_notes)
    num_systems   = math.ceil(math.ceil(total_units / UNITS_PER_MEASURE) / MEASURES_PER_LINE)

    img_height_px = (
        _utils.px(cfg.page.title_padding_pt)
        + _utils.title_h_px
        + num_systems * _utils.system_h_px
        + _utils.below_str_px
    )
    img    = Image.new('RGB', (int(_utils.img_width_px), int(img_height_px)), color='white')
    draw   = ImageDraw.Draw(img)
    base_y = _utils.px(cfg.page.title_padding_pt) + _utils.title_h_px
    return img, draw, base_y


def _build_note_context(note, idx, segment_notes, tick, base_y,
                        last_style, last_pm_x, last_pm_y) -> NoteContext:
    """Compute all note-level values and resolve neighbours once."""
    x   = _utils.tick_to_x(tick)
    dur = note.duration or 0

    next_real_idx = next(
        (i for i in range(idx + 1, len(segment_notes))
         if segment_notes[i].duration is not None), None)
    prev_real_idx = next(
        (i for i in range(idx - 1, -1, -1)
         if segment_notes[i].duration is not None), None)

    return NoteContext(
        note=note,
        idx=idx,
        segment_notes=segment_notes,
        tick=tick,
        strings_y=_utils.tick_to_strings_y(tick, base_y),
        x=x,
        next_x=x + dur * _utils.beat_w_px,
        is_new_line=_utils.is_new_system(tick),
        prev_real_note=segment_notes[prev_real_idx] if prev_real_idx is not None else None,
        next_real_note=segment_notes[next_real_idx] if next_real_idx is not None else None,
        last_style=last_style,
        last_pm_x=last_pm_x,
        last_pm_y=last_pm_y,
    )


def _build_chunk_context(chunk_acc, chunk_dur, note_tick, base_y) -> ChunkContext:
    """Compute all chunk-level values."""
    x = _utils.tick_to_x(chunk_acc)
    return ChunkContext(
        acc=chunk_acc,
        dur=chunk_dur,
        strings_y=_utils.tick_to_strings_y(chunk_acc, base_y),
        stem_y=_utils.tick_to_stem_y(chunk_acc, base_y),
        is_new_line=_utils.is_new_system(chunk_acc),
        x=x,
        next_x=x + chunk_dur * _utils.beat_w_px,
        stem_x=x + _utils.px(_utils.cfg.stems.x_offset_pt),
        is_first=(chunk_acc == note_tick),
    )


def _render_note(draw, note_ctx: NoteContext, base_y, global_measure_counter):
    """Handle row/barline housekeeping and draw all chunks of one note.
    Returns updated (last_pm_x, last_pm_y)."""
    if note_ctx.is_new_line:
        draw_row(draw, note_ctx.strings_y, global_measure_counter)
        note_ctx.last_pm_x = None
        note_ctx.last_pm_y = None

    if (_utils.tick_to_unit_in_measure(note_ctx.tick) == 0
            and _utils.tick_to_measure_in_system(note_ctx.tick) > 0):
        draw_barline(draw, note_ctx.strings_y,
                     _utils.barline_x(note_ctx.tick), global_measure_counter)

    remaining_dur     = note_ctx.note.duration
    chunk_acc         = note_ctx.tick
    prev_stem_x       = None
    prev_stem_y_start = None

    while remaining_dur > 0:
        ticks_left = UNITS_PER_MEASURE - _utils.tick_to_unit_in_measure(chunk_acc)
        chunk_dur  = min(remaining_dur, ticks_left)
        chunk_ctx  = _build_chunk_context(chunk_acc, chunk_dur, note_ctx.tick, base_y)

        if chunk_ctx.is_new_line and not chunk_ctx.is_first:
            draw_row(draw, chunk_ctx.strings_y, global_measure_counter)
            note_ctx.last_pm_x = None
            note_ctx.last_pm_y = None

        if _utils.is_new_measure(chunk_acc) and not chunk_ctx.is_first:
            draw_barline(draw, chunk_ctx.strings_y,
                         _utils.barline_x(chunk_acc), global_measure_counter)

        note_ctx.last_pm_x, note_ctx.last_pm_y = draw_note(
            draw, note_ctx, chunk_ctx, prev_stem_x, prev_stem_y_start,
        )

        prev_stem_x       = chunk_ctx.stem_x
        prev_stem_y_start = chunk_ctx.stem_y
        chunk_acc         += chunk_dur
        remaining_dur     -= chunk_dur

        if _utils.is_new_system(chunk_acc):
            draw_row_end_barline(draw, _utils.tick_to_strings_y(chunk_acc - 1, base_y))

    return note_ctx.last_pm_x, note_ctx.last_pm_y


def _advance_measure_counter(note, acc_dur_segment, global_measure_counter):
    """Increment the measure counter for each measure boundary crossed by this note."""
    chunk_acc     = acc_dur_segment
    remaining_dur = note.duration
    while remaining_dur > 0:
        ticks_left = UNITS_PER_MEASURE - _utils.tick_to_unit_in_measure(chunk_acc)
        chunk_dur  = min(remaining_dur, ticks_left)
        chunk_acc     += chunk_dur
        remaining_dur -= chunk_dur
        if _utils.is_new_measure(chunk_acc):
            global_measure_counter += 1
    return global_measure_counter


# ---------------------------------------------------------------------------
# Lyrics
# ---------------------------------------------------------------------------

def _draw_lyrics(draw_obj, segment, base_y):
    """Draw syllable-aligned inline lyrics below the string lines."""
    from tabfromtext.util.SyllableUtils import split_syllables

    cfg             = _utils.cfg
    lyrics_y_off_px = _utils.px(cfg.lyrics.y_offset_pt)
    flat_syllables  = split_syllables(segment.lyrics.text)
    tick_list       = segment.lyrics.flatten_durations()
    offset_ticks    = convertTimeToTicks(segment.lyrics.offset)

    syllable_events: list[tuple[int, str]] = []
    syl_idx  = 0
    abs_tick = offset_ticks
    for entry in tick_list:
        if entry is not None and syl_idx < len(flat_syllables):
            syllable_events.append((abs_tick, flat_syllables[syl_idx]))
            syl_idx += 1
        abs_tick += 1

    for abs_tick, syl_text in syllable_events:
        syl_strings_y = _utils.tick_to_strings_y(abs_tick, base_y)
        syl_y         = syl_strings_y + 5 * _utils.line_sp_px + lyrics_y_off_px
        syl_x_left    = _utils.tick_to_x(abs_tick)
        text_w        = draw_obj.textbbox((0, 0), syl_text, font=_lyrics_tab_font)[2]
        draw_obj.text(
            (syl_x_left - text_w // 2, syl_y),
            syl_text, fill="black", font=_lyrics_tab_font,
        )


# ---------------------------------------------------------------------------
# Title page
# ---------------------------------------------------------------------------

def render_title_page(song: Song, cfg: LayoutConfig = None,
                      num_columns: int = 2) -> Image.Image | None:
    sections = [(seg.title, seg.lyrics.text if seg.lyrics is not None else None)
                for seg in song.segments]
    if not sections:
        return None

    _init_render(cfg or LayoutConfig())
    cfg = _utils.cfg

    from reportlab.lib.pagesizes import A4
    A4_WIDTH_PT, A4_HEIGHT_PT = A4

    img_w_px  = _utils.img_width_px
    page_h_pt = A4_HEIGHT_PT - cfg.page.top_margin_pt - cfg.page.bottom_margin_pt
    img_h_px  = _utils.px(page_h_pt)

    img  = Image.new('RGB', (img_w_px, img_h_px), color='white')
    draw = ImageDraw.Draw(img)

    margin_px     = _utils.margin_left_px
    title_line_h  = int(_utils.px(cfg.fonts.title_pt)  * 1.4)
    lyrics_line_h = int(_utils.px(cfg.fonts.lyrics_pt) * 1.4)
    section_gap   = lyrics_line_h
    top_pad_px    = _utils.px(cfg.page.top_margin_pt * 0.5)

    title_w = draw.textbbox((0, 0), song.title, font=_title_font)[2]
    draw.text(((img_w_px - title_w) // 2, top_pad_px), song.title,
              fill="black", font=_title_font)
    columns_top_y = top_pad_px + title_line_h * 2

    usable_w   = img_w_px - 2 * margin_px
    col_gap    = margin_px
    col_w      = (usable_w - col_gap * (num_columns - 1)) // num_columns
    col_starts = [margin_px + i * (col_w + col_gap) for i in range(num_columns)]
    col_height = img_h_px - columns_top_y

    def section_height(title, lyrics) -> int:
        h = title_line_h
        if lyrics:
            h += len(lyrics.splitlines()) * lyrics_line_h
        return h + section_gap

    columns: list[list] = [[] for _ in range(num_columns)]
    col_used = [0] * num_columns
    col_idx  = 0
    for title, lyrics in sections:
        sh = section_height(title, lyrics)
        if col_used[col_idx] + sh > col_height and col_idx < num_columns - 1:
            col_idx += 1
        columns[col_idx].append((title, lyrics))
        col_used[col_idx] += sh

    for c_idx, col_sections in enumerate(columns):
        x = col_starts[c_idx]
        y = columns_top_y
        for title, lyrics in col_sections:
            draw.text((x, y), title, fill="black", font=_title_font)
            y += title_line_h
            if lyrics:
                for line in lyrics.splitlines():
                    draw.text((x, y), line, fill="black", font=_lyrics_font)
                    y += lyrics_line_h
            y += section_gap

    return img