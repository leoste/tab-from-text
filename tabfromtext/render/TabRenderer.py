import math
from PIL import Image, ImageDraw
from tabfromtext.song.Segment import Segment
from tabfromtext.render.RenderContexts import NoteContext, ChunkContext, SegmentRenderState
from tabfromtext.render.LayoutUtils import STRING_GAPS
from tabfromtext.render.RowPainter import (
    draw_row, draw_barline, draw_row_end_barline, draw_final_barline,
    draw_lyrics, draw_lyrics_only, draw_segment_title, lyrics_line_h_px,
)
from tabfromtext.render.NotePainter import draw_note
import tabfromtext.render.LayoutUtils as lu


# ---------------------------------------------------------------------------
# Context builders
# ---------------------------------------------------------------------------

def _build_note_context(note, idx, segment_notes, tick, base_y) -> NoteContext:
    x   = lu.tick_to_x(tick)
    dur = note.duration or 0

    next_real_idx = next(
        (i for i in range(idx + 1, len(segment_notes))
         if segment_notes[i].duration is not None), None)
    prev_real_idx = next(
        (i for i in range(idx - 1, -1, -1)
         if segment_notes[i].duration is not None), None)

    return NoteContext(
        note=note,
        tick=tick,
        strings_y=lu.tick_to_strings_y(tick, base_y),
        x=x,
        next_x=x + dur * lu.beat_w_px,
        is_new_line=lu.is_new_system(tick),
        prev_real_note=segment_notes[prev_real_idx] if prev_real_idx is not None else None,
        next_real_note=segment_notes[next_real_idx] if next_real_idx is not None else None,
    )


def _build_chunk_context(chunk_acc, chunk_dur, note_tick, base_y) -> ChunkContext:
    x = lu.tick_to_x(chunk_acc)
    return ChunkContext(
        acc=chunk_acc,
        dur=chunk_dur,
        strings_y=lu.tick_to_strings_y(chunk_acc, base_y),
        stem_y=lu.tick_to_stem_y(chunk_acc, base_y),
        is_new_line=lu.is_new_system(chunk_acc),
        x=x,
        next_x=x + chunk_dur * lu.beat_w_px,
        stem_x=x + lu.px(lu.cfg.stems.x_offset_pt),
        is_first=(chunk_acc == note_tick),
    )


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
        render_state.last_annotation_x     = None
        render_state.last_annotation_y     = None
        render_state.last_annotation_style = None

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
        chunk_ctx  = _build_chunk_context(chunk_acc, chunk_dur, note_ctx.tick, base_y)

        if chunk_ctx.is_new_line and not chunk_ctx.is_first:
            draw_row(draw, chunk_ctx.strings_y, global_measure_counter)
            render_state.last_annotation_x     = None
            render_state.last_annotation_y     = None
            render_state.last_annotation_style = None

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
# Image allocation helpers
# ---------------------------------------------------------------------------

def _new_image(height_px: int):
    """Allocate a white PIL image of the standard width and given height."""
    img  = Image.new('RGB', (int(lu.img_width_px), int(height_px)), color='white')
    draw = ImageDraw.Draw(img)
    return img, draw


def _title_top_px() -> int:
    return lu.px(lu.cfg.page.title_padding_pt)


def _base_y_px() -> int:
    return _title_top_px() + lu.title_h_px


def _create_tab_image(segment, instrument_name):
    """Allocate the PIL image for a normal tab segment."""
    segment_notes = segment.GetNotesFromSegment(instrument_name)
    total_units   = sum((n.duration if n.duration else 0) for n in segment_notes)
    num_systems   = math.ceil(math.ceil(total_units / lu.UNITS_PER_MEASURE) / lu.MEASURES_PER_LINE)
    height_px     = _base_y_px() + num_systems * lu.system_h_px
    return *_new_image(height_px), _base_y_px()


def _create_lyrics_only_image(segment):
    """Allocate a compact PIL image for a lyrics-only segment."""
    total_units = segment.lyrics.total_ticks()
    num_systems = math.ceil(math.ceil(total_units / lu.UNITS_PER_MEASURE) / lu.MEASURES_PER_LINE)
    line_h      = lyrics_line_h_px()
    height_px   = _base_y_px() + num_systems * line_h
    return *_new_image(height_px), _base_y_px()


def _create_title_only_image():
    """Allocate a minimal PIL image showing only the segment title."""
    height_px = _base_y_px() + lu.below_str_px
    return _new_image(height_px)


# ---------------------------------------------------------------------------
# Public render entry points
# ---------------------------------------------------------------------------

def render_tab(segments: list[Segment], instrument_name: str) -> list[Image.Image]:
    results = []
    global_measure_counter = 1

    for segment in segments:
        parts_for_instrument = segment.parts.get(instrument_name)

        if parts_for_instrument is None:
            # No notes for this instrument in this segment
            if segment.lyrics is not None:
                img, draw, base_y = _create_lyrics_only_image(segment)
                draw_segment_title(draw, segment.title)
                draw_lyrics_only(draw, segment, base_y)
                global_measure_counter += math.ceil(
                    segment.lyrics.total_ticks() / lu.UNITS_PER_MEASURE
                )
            else:
                img, draw = _create_title_only_image()
                draw_segment_title(draw, segment.title)
            results.append(img)
            continue

        img, draw, base_y = _create_tab_image(segment, instrument_name)
        draw_segment_title(draw, segment.title)

        segment_notes = segment.GetNotesFromSegment(instrument_name)
        acc_dur       = 0
        render_state  = SegmentRenderState()
        final_x       = lu.margin_left_px
        final_y       = base_y

        for idx, note in enumerate(segment_notes):
            note_ctx = _build_note_context(note, idx, segment_notes, acc_dur, base_y)

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

        results.append(img)

    return results