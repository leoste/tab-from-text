"""Note-level drawing — everything that belongs to a single note event."""
import math
from tabfromtext.song.StrumStyle import StrumStyle
from tabfromtext.render.NoteContext import NoteContext
from tabfromtext.render.ChunkContext import ChunkContext
from tabfromtext.render.SegmentRenderState import SegmentRenderState
from tabfromtext.util.TimeUtils import (
    TICKS_EIGHTH, TICKS_DOTTED_EIGHTH, TICKS_SIXTEENTH,
    TICKS_HALF_NOTE, TICKS_FULL_NOTE,
    is_dotted,
)
import tabfromtext.render.LayoutUtils as lu

# Styles that draw a spanning annotation above the strings
_SPANNING_STYLES = (StrumStyle.PALM_MUTED, StrumStyle.VIBRATO)


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def draw_note(draw_obj, note_ctx: NoteContext, chunk_ctx: ChunkContext,
              render_state: SegmentRenderState,
              prev_stem_x, prev_stem_y_start):
    """Draw all visual elements for one note-chunk.
    Updates render_state in place for spanning annotation continuity.
    """
    if note_ctx.note.chord and note_ctx.note.style != StrumStyle.NO_HIT:
        _draw_note_content(draw_obj, note_ctx, chunk_ctx, render_state)
    else:
        render_state.reset_annotation()

    is_rest = (note_ctx.note.chord is None or note_ctx.note.style == StrumStyle.NO_HIT)
    _draw_stem(draw_obj, chunk_ctx, is_rest=is_rest)

    if chunk_ctx.is_first and is_dotted(note_ctx.note.duration):
        _draw_dot(draw_obj, chunk_ctx)

    if prev_stem_x is not None:
        draw_arc(draw_obj, prev_stem_x, chunk_ctx.stem_x,
                 min(prev_stem_y_start, chunk_ctx.stem_y))

    if chunk_ctx.dur in (TICKS_SIXTEENTH, TICKS_EIGHTH, TICKS_DOTTED_EIGHTH):
        _draw_beam(draw_obj, note_ctx, chunk_ctx)


# ---------------------------------------------------------------------------
# Note content: fret numbers, slides, spanning annotations
# ---------------------------------------------------------------------------

def _draw_note_content(draw_obj, note_ctx: NoteContext, chunk_ctx: ChunkContext,
                       render_state: SegmentRenderState):
    """Draw fret labels (or 'X') for each string, slide lines, and spanning annotations."""
    note    = note_ctx.note
    strings = [note.chord.string1, note.chord.string2, note.chord.string3,
               note.chord.string4, note.chord.string5, note.chord.string6]

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

    if note.style in _SPANNING_STYLES:
        _draw_spanning_annotation(draw_obj, note_ctx, chunk_ctx, render_state)
    else:
        render_state.reset_annotation()


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


# ---------------------------------------------------------------------------
# Spanning annotations (palm mute, vibrato)
# ---------------------------------------------------------------------------

def _draw_spanning_annotation(draw_obj, note_ctx: NoteContext, chunk_ctx: ChunkContext,
                               render_state: SegmentRenderState):
    """Unified handler for annotations that span across consecutive notes above the strings.
    Dispatches to the style-specific drawing function, sharing continuity state."""
    style = note_ctx.note.style

    is_first = (render_state.last_annotation_style != style
                or render_state.last_annotation_x is None)
    is_last  = (note_ctx.next_real_note is None
                or note_ctx.next_real_note.style != style)

    if style == StrumStyle.PALM_MUTED:
        _draw_palm_mute(draw_obj, chunk_ctx, render_state, is_first, is_last)
    elif style == StrumStyle.VIBRATO:
        _draw_vibrato(draw_obj, chunk_ctx, render_state, is_first, is_last)


def _draw_palm_mute(draw_obj, chunk_ctx: ChunkContext,
                    render_state: SegmentRenderState,
                    is_first: bool, is_last: bool):
    """Draw P.M. label, dashed continuation line, and closing tick."""
    cfg  = lu.cfg
    pm_y = chunk_ctx.strings_y + lu.px(cfg.palm_mute.y_offset_pt)

    if is_first:
        draw_obj.text(
            (chunk_ctx.x, pm_y - lu.px(cfg.palm_mute.label_y_pt)),
            "P.M.", fill="black", font=lu.annotation_font,
        )
        render_state.last_annotation_x = chunk_ctx.x + lu.px(cfg.palm_mute.label_w_pt)
    else:
        # Draw dashed segment inline
        dash_gap = lu.px(cfg.palm_mute.dash_gap_pt)
        curr = render_state.last_annotation_x
        while curr < chunk_ctx.x:
            draw_obj.line(
                [(curr, pm_y), (min(curr + dash_gap, chunk_ctx.x), pm_y)],
                fill="black", width=lu.lw(cfg.line_width.thin_pt),
            )
            curr += dash_gap * 2
        render_state.last_annotation_x = chunk_ctx.x

    if is_last:
        tick_h = lu.px(cfg.palm_mute.tick_h_pt)
        draw_obj.line(
            [(chunk_ctx.next_x, pm_y - tick_h // 2),
             (chunk_ctx.next_x, pm_y + tick_h // 2)],
            fill="black", width=lu.lw(cfg.line_width.thin_pt),
        )

    render_state.last_annotation_y     = pm_y
    render_state.last_annotation_style = StrumStyle.PALM_MUTED


def _draw_vibrato(draw_obj, chunk_ctx: ChunkContext,
                  render_state: SegmentRenderState,
                  is_first: bool, is_last: bool):
    """Draw a wavy vibrato line spanning the note's duration."""
    cfg   = lu.cfg
    vib_y = chunk_ctx.strings_y + lu.px(cfg.vibrato.y_offset_pt)

    x_start = chunk_ctx.x if is_first else render_state.last_annotation_x
    x_end   = chunk_ctx.next_x

    _draw_wavy_segment(draw_obj, x_start, x_end, vib_y)

    if is_last:
        tick_h = lu.px(cfg.vibrato.tick_h_pt)
        draw_obj.line(
            [(x_end, vib_y - tick_h // 2),
             (x_end, vib_y + tick_h // 2)],
            fill="black", width=lu.lw(cfg.line_width.thin_pt),
        )

    render_state.last_annotation_x     = x_end
    render_state.last_annotation_y     = vib_y
    render_state.last_annotation_style = StrumStyle.VIBRATO


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
    """Draw beams below the note stem.

    Bottom beam (shared by eighths and sixteenths):
      - Connects forward to the next note if it is an eighth or sixteenth.
      - Falls back to a stub if not beamed in either direction.

    Top beam (sixteenths only):
      - Drawn above the bottom beam, separated by beam_gap_pt.
      - Connects forward only to an adjacent sixteenth.
      - Falls back to a stub if the next note is not a sixteenth.
    """
    cfg            = lu.cfg
    chunk_bottom_y = chunk_ctx.stem_y + lu.px(cfg.stems.h_pt)
    beam_gap_y     = lu.px(cfg.beams.beam_gap_pt)
    note           = note_ctx.note
    dur            = chunk_ctx.dur

    def _is_beamable(n):
        """True if note n can participate in the bottom beam (eighth or sixteenth)."""
        return (n is not None
                and n.duration in (TICKS_EIGHTH, TICKS_SIXTEENTH)
                and n.chord is not None)

    def _is_sixteenth(n):
        """True if note n is a sixteenth and has a chord."""
        return (n is not None
                and n.duration == TICKS_SIXTEENTH
                and n.chord is not None)

    is_at_measure_end   = lu.is_new_measure(chunk_ctx.acc + chunk_ctx.dur)
    is_at_measure_start = lu.is_new_measure(chunk_ctx.acc)

    # --- bottom beam ---
    can_beam_fwd_bot = (not is_at_measure_end
                        and _is_beamable(note_ctx.next_real_note)
                        and note.chord is not None)
    is_beamed_back_bot = (not is_at_measure_start
                          and _is_beamable(note_ctx.prev_real_note)
                          and note.chord is not None)

    if can_beam_fwd_bot:
        draw_obj.line(
            [(chunk_ctx.stem_x, chunk_bottom_y),
             (chunk_ctx.stem_x + lu.beat_w_px * dur, chunk_bottom_y)],
            fill="black", width=lu.lw(cfg.line_width.thick_pt),
        )
    elif not is_beamed_back_bot:
        draw_obj.line(
            [(chunk_ctx.stem_x, chunk_bottom_y),
             (chunk_ctx.stem_x + lu.px(cfg.beams.stub_pt), chunk_bottom_y)],
            fill="black", width=lu.lw(cfg.line_width.normal_pt),
        )

    # --- top beam (sixteenth only) ---
    if dur != TICKS_SIXTEENTH:
        return

    top_beam_y = chunk_bottom_y - beam_gap_y

    can_beam_fwd_top = (not is_at_measure_end
                        and _is_sixteenth(note_ctx.next_real_note)
                        and note.chord is not None)
    is_beamed_back_top = (not is_at_measure_start
                          and _is_sixteenth(note_ctx.prev_real_note)
                          and note.chord is not None)

    if can_beam_fwd_top:
        draw_obj.line(
            [(chunk_ctx.stem_x, top_beam_y),
             (chunk_ctx.stem_x + lu.beat_w_px * dur, top_beam_y)],
            fill="black", width=lu.lw(cfg.line_width.thick_pt),
        )
    elif not is_beamed_back_top:
        draw_obj.line(
            [(chunk_ctx.stem_x, top_beam_y),
             (chunk_ctx.stem_x + lu.px(cfg.beams.stub_pt), top_beam_y)],
            fill="black", width=lu.lw(cfg.line_width.normal_pt),
        )


# ---------------------------------------------------------------------------
# Shared primitives
# ---------------------------------------------------------------------------

def draw_arc(draw_obj, x_start, x_end, y_top):
    if x_end <= x_start:
        return
    cfg     = lu.cfg
    top_off = lu.px(cfg.arcs.top_offset_pt)
    bot_off = lu.px(cfg.arcs.bot_offset_pt)
    arc_box = [x_start, y_top - top_off, x_end, y_top - bot_off]
    draw_obj.arc(arc_box, start=180, end=0, fill="black",
                 width=lu.lw(cfg.line_width.thin_pt))


def _draw_wavy_segment(draw_obj, x_start, x_end, y_mid):
    """Draw a sine-wave wavy line from x_start to x_end centred on y_mid."""
    cfg    = lu.cfg
    wave_w = lu.px(cfg.vibrato.wave_w_pt)
    wave_h = lu.px(cfg.vibrato.wave_h_pt)
    lw     = lu.lw(cfg.line_width.thin_pt)

    if wave_w < 1:
        wave_w = 1
    total_w = x_end - x_start
    if total_w <= 0:
        return

    steps  = max(total_w, 4)
    points = []
    for s in range(steps + 1):
        t = s / steps
        x = x_start + t * total_w
        y = y_mid - wave_h * math.sin(math.pi * t * total_w / wave_w)
        points.append((x, y))

    for i in range(len(points) - 1):
        draw_obj.line([points[i], points[i + 1]], fill="black", width=lw)