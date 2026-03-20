import math
from PIL import Image
from tabfromtext.song.Segment import Segment
from tabfromtext.render.NoteContext import NoteContext
from tabfromtext.render.ChunkContext import ChunkContext
from tabfromtext.render.SegmentRenderState import SegmentRenderState
from tabfromtext.render.LayoutUtils import STRING_GAPS
from tabfromtext.render.RowPainter import (
    draw_row, draw_barline, draw_row_end_barline, draw_final_barline,
    draw_lyrics, draw_lyrics_only, draw_segment_title,
)
from tabfromtext.render.NotePainter import draw_note
from tabfromtext.render.ImageFactory import (
    new_tab_image, new_lyrics_only_image, new_title_only_image,
)
import tabfromtext.render.LayoutUtils as lu


# ---------------------------------------------------------------------------
# Note rendering — chunk loop + row housekeeping
# ---------------------------------------------------------------------------

def _render_note(draw, note_ctx: NoteContext, base_y,
                 render_state: SegmentRenderState,
                 global_measure_counter) -> tuple[int, int, int]:
    """Handle row/barline housekeeping and draw all chunks of one note.
    Returns (global_measure_counter, final_x, final_y)."""
    if note_ctx.is_new_line:
        draw_row(draw, note_ctx.strings_y, global_measure_counter)
        render_state.reset_annotation()

    if (lu.tick_to_unit_in_measure(note_ctx.tick) == 0
            and lu.tick_to_measure_in_system(note_ctx.tick) > 0):
        draw_barline(draw, note_ctx.strings_y,
                     lu.barline_x(note_ctx.tick), global_measure_counter)

    remaining_dur     = note_ctx.note.duration
    chunk_acc         = note_ctx.tick
    prev_stem_x       = None
    prev_stem_y_start = None
    final_x           = note_ctx.next_x
    final_y           = note_ctx.strings_y

    while remaining_dur > 0:
        ticks_left = lu.UNITS_PER_MEASURE - lu.tick_to_unit_in_measure(chunk_acc)
        chunk_dur  = min(remaining_dur, ticks_left)
        chunk_ctx  = ChunkContext.build(chunk_acc, chunk_dur, note_ctx.tick, base_y)

        if chunk_ctx.is_new_line and not chunk_ctx.is_first:
            draw_row(draw, chunk_ctx.strings_y, global_measure_counter)
            render_state.reset_annotation()

        if lu.is_new_measure(chunk_acc) and not chunk_ctx.is_first:
            draw_barline(draw, chunk_ctx.strings_y,
                         lu.barline_x(chunk_acc), global_measure_counter)

        draw_note(draw, note_ctx, chunk_ctx, render_state, prev_stem_x, prev_stem_y_start)

        prev_stem_x       = chunk_ctx.stem_x
        prev_stem_y_start = chunk_ctx.stem_y
        chunk_acc         += chunk_dur
        remaining_dur     -= chunk_dur

        if lu.is_new_measure(chunk_acc):
            global_measure_counter += 1

        if lu.is_new_system(chunk_acc):
            draw_row_end_barline(draw, lu.tick_to_strings_y(chunk_acc - 1, base_y))

    return global_measure_counter, final_x, final_y


# ---------------------------------------------------------------------------
# Per-segment renderers
# ---------------------------------------------------------------------------

def _render_empty_segment(segment) -> Image.Image:
    """Render a segment that has no notes and no lyrics — title only."""
    img, draw = new_title_only_image()
    draw_segment_title(draw, segment.title)
    return img


def _render_lyrics_only_segment(segment) -> tuple[Image.Image, int]:
    """Render a segment that has lyrics but no tab notes for this instrument.
    Returns (image, measures_consumed)."""
    img, draw, base_y = new_lyrics_only_image(segment)
    draw_segment_title(draw, segment.title)
    draw_lyrics_only(draw, segment, base_y)
    measures_consumed = math.ceil(segment.lyrics.total_ticks() / lu.UNITS_PER_MEASURE)
    return img, measures_consumed


def _render_tab_segment(segment, instrument_name,
                        global_measure_counter) -> tuple[Image.Image, int]:
    """Render a full tab segment with notes (and optional lyrics).
    Returns (image, updated_global_measure_counter)."""
    img, draw, base_y = new_tab_image(segment, instrument_name)
    draw_segment_title(draw, segment.title)

    segment_notes = segment.GetNotesFromSegment(instrument_name)
    acc_dur       = 0
    render_state  = SegmentRenderState()
    final_x       = lu.margin_left_px
    final_y       = base_y

    for idx, note in enumerate(segment_notes):
        note_ctx = NoteContext.build(note, idx, segment_notes, acc_dur, base_y)

        if note.duration is not None:
            global_measure_counter, final_x, final_y = _render_note(
                draw, note_ctx, base_y, render_state, global_measure_counter,
            )

        if note.style is not None:
            render_state.last_style = note.style
        acc_dur += note.duration if note.duration else 0

    if not lu.is_new_system(acc_dur):
        draw_final_barline(draw, final_x, final_y)

    if segment.lyrics is not None:
        draw_lyrics(draw, segment, base_y)

    return img, global_measure_counter


# ---------------------------------------------------------------------------
# Public render entry point
# ---------------------------------------------------------------------------

def render_tab(segments: list[Segment], instrument_name: str) -> list[Image.Image]:
    results = []
    global_measure_counter = 1

    for segment in segments:
        has_notes  = segment.parts.get(instrument_name) is not None
        has_lyrics = segment.lyrics is not None

        if has_notes:
            img, global_measure_counter = _render_tab_segment(
                segment, instrument_name, global_measure_counter,
            )
        elif has_lyrics:
            img, measures_consumed = _render_lyrics_only_segment(segment)
            global_measure_counter += measures_consumed
        else:
            img = _render_empty_segment(segment)

        results.append(img)

    return results