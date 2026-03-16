"""Note-level drawing — everything that belongs to a single note event."""
from tabfromtext.song.StrumStyle import StrumStyle
from tabfromtext.render.RenderContexts import NoteContext, ChunkContext
from tabfromtext.util.TimeUtils import TIME_RESOLUTION
import tabfromtext.render.LayoutUtils as lu

TICKS_SIXTEENTH     = TIME_RESOLUTION // 2
TICKS_DOTTED_EIGHTH = TICKS_SIXTEENTH * 3
TICKS_EIGHTH        = 1 * TIME_RESOLUTION
TICKS_HALF_NOTE     = 4 * TIME_RESOLUTION
TICKS_FULL_NOTE     = 8 * TIME_RESOLUTION


def is_dotted(duration):
    if duration <= 0:
        return False
    doubled = duration * 2
    if doubled % 3 != 0:
        return False
    base = doubled // 3
    return base > 0 and (base & (base - 1)) == 0


# ---------------------------------------------------------------------------
# Public entry point
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


# ---------------------------------------------------------------------------
# Fret numbers, slides, palm mute
# ---------------------------------------------------------------------------

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
            y     = chunk_ctx.strings_y + i * lu.line_sp_px
            label = "X" if note.style == StrumStyle.MUTED else str(fret)

            text_w, text_h = draw_obj.textbbox((0, 0), label, font=lu.fret_font)[2:]
            draw_obj.rectangle(
                [chunk_ctx.x - 2,          y - text_h // 2,
                 chunk_ctx.x + text_w + 2, y + text_h // 2],
                fill="white",
            )
            draw_obj.text(
                (chunk_ctx.x, y - text_h // 2),
                label, fill="black", font=lu.fret_font,
            )

            if note.style == StrumStyle.SLIDE:
                _draw_slide(draw_obj, chunk_ctx, i, text_w)

    if note.style == StrumStyle.PALM_MUTED:
        last_pm_x, last_pm_y = _draw_palm_mute(draw_obj, note_ctx, chunk_ctx)

    return last_pm_x, last_pm_y


def _draw_slide(draw_obj, chunk_ctx: ChunkContext, string_index, text_w):
    """Draw the horizontal slide line and arc for one string."""
    cfg   = lu.cfg
    nudge = lu.px(cfg.arcs.slide_nudge_pt)
    y     = chunk_ctx.strings_y + string_index * lu.line_sp_px
    draw_obj.line(
        [(chunk_ctx.x + text_w + nudge, y),
         (chunk_ctx.next_x - nudge, y)],
        fill="black", width=lu.lw(cfg.line_width.thin_pt),
    )
    draw_arc(draw_obj,
             chunk_ctx.x + nudge, chunk_ctx.next_x - nudge,
             chunk_ctx.strings_y + string_index * lu.line_sp_px)


def _draw_palm_mute(draw_obj, note_ctx: NoteContext, chunk_ctx: ChunkContext):
    """Draw P.M. label, dashed continuation line, and closing tick.
    Returns updated (last_pm_x, last_pm_y)."""
    cfg  = lu.cfg
    pm_y = chunk_ctx.strings_y + lu.px(cfg.palm_mute.y_offset_pt)

    is_first_pm_on_line = (note_ctx.last_style != StrumStyle.PALM_MUTED
                           or note_ctx.last_pm_x is None)
    is_last_pm = (note_ctx.next_real_note is None
                  or note_ctx.next_real_note.style != StrumStyle.PALM_MUTED)

    if is_first_pm_on_line:
        draw_obj.text(
            (chunk_ctx.x, pm_y - lu.px(cfg.palm_mute.label_y_pt)),
            "P.M.", fill="black", font=lu.annotation_font,
        )
        last_pm_x = chunk_ctx.x + lu.px(cfg.palm_mute.label_w_pt)
    else:
        _draw_dashed_segment(draw_obj, note_ctx.last_pm_x, chunk_ctx.x, pm_y)
        last_pm_x = chunk_ctx.x

    if is_last_pm and not is_first_pm_on_line:
        tick_h = lu.px(cfg.palm_mute.tick_h_pt)
        draw_obj.line(
            [(chunk_ctx.x, pm_y - tick_h // 2),
             (chunk_ctx.x, pm_y + tick_h // 2)],
            fill="black", width=lu.lw(cfg.line_width.thin_pt),
        )

    return last_pm_x, pm_y


# ---------------------------------------------------------------------------
# Stem, dot, beam
# ---------------------------------------------------------------------------

def _draw_stem(draw_obj, chunk_ctx: ChunkContext, is_rest: bool = False):
    """Draw the stem below the note."""
    cfg = lu.cfg
    if is_rest:
        full_h = lu.px(cfg.stems.h_pt)
        rest_h = lu.px(cfg.notes.rest_stem_pt)
        draw_obj.line(
            [(chunk_ctx.stem_x, chunk_ctx.stem_y + full_h - rest_h),
             (chunk_ctx.stem_x, chunk_ctx.stem_y + full_h)],
            fill="black", width=lu.lw(cfg.line_width.normal_pt),
        )
        return
    if chunk_ctx.dur >= TICKS_FULL_NOTE:
        draw_obj.line(
            [(chunk_ctx.stem_x, chunk_ctx.stem_y),
             (chunk_ctx.stem_x, chunk_ctx.stem_y + lu.px(cfg.stems.h_pt * 3.0))],
            fill="black", width=lu.lw(cfg.line_width.normal_pt),
        )
    elif chunk_ctx.dur >= TICKS_HALF_NOTE:
        top_h = lu.px(cfg.stems.h_pt * 0.5)
        gap   = lu.px(cfg.stems.h_pt * 1.0)
        bot_h = lu.px(cfg.stems.h_pt * 1.5)
        draw_obj.line(
            [(chunk_ctx.stem_x, chunk_ctx.stem_y),
             (chunk_ctx.stem_x, chunk_ctx.stem_y + top_h)],
            fill="black", width=lu.lw(cfg.line_width.normal_pt),
        )
        draw_obj.line(
            [(chunk_ctx.stem_x, chunk_ctx.stem_y + top_h + gap),
             (chunk_ctx.stem_x, chunk_ctx.stem_y + top_h + gap + bot_h)],
            fill="black", width=lu.lw(cfg.line_width.normal_pt),
        )
    else:
        draw_obj.line(
            [(chunk_ctx.stem_x, chunk_ctx.stem_y),
             (chunk_ctx.stem_x, chunk_ctx.stem_y + lu.px(cfg.stems.h_pt))],
            fill="black", width=lu.lw(cfg.line_width.normal_pt),
        )


def _draw_dot(draw_obj, chunk_ctx: ChunkContext):
    """Draw the dot for a dotted-rhythm note."""
    cfg        = lu.cfg
    dot_offset = lu.px(cfg.beams.dot_offset_pt)
    dot_r      = lu.px(cfg.beams.dot_r_pt)
    draw_obj.ellipse(
        [chunk_ctx.stem_x + dot_offset - dot_r, chunk_ctx.stem_y + dot_offset - dot_r,
         chunk_ctx.stem_x + dot_offset + dot_r, chunk_ctx.stem_y + dot_offset + dot_r],
        fill="black",
    )


def _draw_beam(draw_obj, note_ctx: NoteContext, chunk_ctx: ChunkContext):
    """Draw a beam connecting to the next note, or a stub flag if unbeamed."""
    cfg            = lu.cfg
    chunk_bottom_y = chunk_ctx.stem_y + lu.px(cfg.stems.h_pt)
    note           = note_ctx.note

    is_at_measure_end = lu.is_new_measure(chunk_ctx.acc + chunk_ctx.dur)
    can_beam_fwd = (not is_at_measure_end
                    and note_ctx.next_real_note is not None
                    and note_ctx.next_real_note.duration == note.duration
                    and note.chord is not None
                    and note_ctx.next_real_note.chord is not None)

    is_at_measure_start = lu.is_new_measure(chunk_ctx.acc)
    is_beamed_back = (not is_at_measure_start
                      and note_ctx.prev_real_note is not None
                      and note_ctx.prev_real_note.duration == note.duration
                      and note.chord is not None
                      and note_ctx.prev_real_note.chord is not None)

    if can_beam_fwd:
        draw_obj.line(
            [(chunk_ctx.stem_x, chunk_bottom_y),
             (chunk_ctx.stem_x + lu.beat_w_px * chunk_ctx.dur, chunk_bottom_y)],
            fill="black", width=lu.lw(cfg.line_width.thick_pt),
        )
    elif not is_beamed_back:
        draw_obj.line(
            [(chunk_ctx.stem_x, chunk_bottom_y),
             (chunk_ctx.stem_x + lu.px(cfg.beams.stub_pt), chunk_bottom_y)],
            fill="black", width=lu.lw(cfg.line_width.normal_pt),
        )


# ---------------------------------------------------------------------------
# Shared primitives
# ---------------------------------------------------------------------------

def draw_arc(draw_obj, x_start, x_end, y_top):
    cfg     = lu.cfg
    top_off = lu.px(cfg.arcs.top_offset_pt)
    bot_off = lu.px(cfg.arcs.bot_offset_pt)
    arc_box = [x_start, y_top - top_off, x_end, y_top - bot_off]
    draw_obj.arc(arc_box, start=180, end=0, fill="black",
                 width=lu.lw(cfg.line_width.thin_pt))


def _draw_dashed_segment(draw_obj, x_start, x_end, y):
    dash_gap = lu.px(lu.cfg.palm_mute.dash_gap_pt)
    curr = x_start
    while curr < x_end:
        draw_obj.line(
            [(curr, y), (min(curr + dash_gap, x_end), y)],
            fill="black", width=lu.lw(lu.cfg.line_width.thin_pt),
        )
        curr += dash_gap * 2