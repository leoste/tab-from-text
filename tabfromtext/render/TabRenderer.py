import math
from PIL import Image, ImageDraw
from reportlab.lib.pagesizes import A4
from tabfromtext.song.Segment import Segment
from tabfromtext.song.Song import Song
from tabfromtext.render.RenderContexts import NoteContext, ChunkContext, SegmentRenderState
from tabfromtext.render.LayoutUtils import STRING_GAPS
from tabfromtext.render.RowPainter import (
    draw_row, draw_barline, draw_row_end_barline, draw_final_barline, draw_lyrics,
    draw_lyrics_only,
)
from tabfromtext.render.NotePainter import draw_note
import tabfromtext.render.LayoutUtils as lu

A4_WIDTH_PT, A4_HEIGHT_PT = A4


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
        render_state.last_pm_x = None
        render_state.last_pm_y = None

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
            render_state.last_pm_x = None
            render_state.last_pm_y = None

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
# Segment image allocation
# ---------------------------------------------------------------------------

def _total_ticks_from_lyrics(segment) -> int:
    """Derive total ticks from lyrics durations when parts is None."""
    from tabfromtext.util.TimeUtils import convertTimeToTicks
    return sum(
        convertTimeToTicks(d) for d in segment.lyrics.durations
        if d is not None
    )


def _create_segment_image(segment, instrument_name):
    """Allocate the PIL image for one segment and return (img, draw, base_y)."""
    segment_notes = segment.GetNotesFromSegment(instrument_name)
    total_units   = sum((n.duration if n.duration else 0) for n in segment_notes)
    num_systems   = math.ceil(math.ceil(total_units / lu.UNITS_PER_MEASURE) / lu.MEASURES_PER_LINE)

    img_height_px = (
        lu.px(lu.cfg.page.title_padding_pt)
        + lu.title_h_px
        + num_systems * lu.system_h_px
        + lu.below_str_px
    )
    img    = Image.new('RGB', (int(lu.img_width_px), int(img_height_px)), color='white')
    draw   = ImageDraw.Draw(img)
    base_y = lu.px(lu.cfg.page.title_padding_pt) + lu.title_h_px
    return img, draw, base_y


def _create_lyrics_only_image(segment):
    """Allocate a compact PIL image for a lyrics-only segment."""
    total_units = _total_ticks_from_lyrics(segment)
    num_systems = math.ceil(math.ceil(total_units / lu.UNITS_PER_MEASURE) / lu.MEASURES_PER_LINE)
    line_h_px   = lu.px(lu.cfg.fonts.lyrics_tab_pt) * 2

    img_height_px = (
        lu.px(lu.cfg.page.title_padding_pt)
        + lu.title_h_px
        + num_systems * line_h_px
        + line_h_px  # bottom padding
    )
    img    = Image.new('RGB', (int(lu.img_width_px), int(img_height_px)), color='white')
    draw   = ImageDraw.Draw(img)
    base_y = lu.px(lu.cfg.page.title_padding_pt) + lu.title_h_px
    return img, draw, base_y


# ---------------------------------------------------------------------------
# Public render entry points
# ---------------------------------------------------------------------------

def render_tab(segments: list[Segment], instrument_name: str) -> list[Image.Image]:
    results = []
    global_measure_counter = 1

    for segment in segments:
        is_lyrics_only = (
            segment.parts.get(instrument_name) is None
            and segment.lyrics is not None
        )
        is_empty = (
            segment.parts.get(instrument_name) is None
            and segment.lyrics is None
        )

        if is_empty:
            continue

        if is_lyrics_only:
            img, draw, base_y = _create_lyrics_only_image(segment)
            draw.text((lu.margin_left_px, lu.px(lu.cfg.page.title_padding_pt)),
                      segment.title, fill="black", font=lu.title_font)
            draw_lyrics_only(draw, segment, base_y)
            results.append(img)
            # advance measure counter based on lyrics duration
            total_ticks = _total_ticks_from_lyrics(segment)
            num_measures = math.ceil(total_ticks / lu.UNITS_PER_MEASURE)
            global_measure_counter += num_measures
            continue

        img, draw, base_y = _create_segment_image(segment, instrument_name)
        draw.text((lu.margin_left_px, lu.px(lu.cfg.page.title_padding_pt)),
                  segment.title, fill="black", font=lu.title_font)

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


def render_title_page(song: Song, num_columns: int = 2) -> Image.Image | None:
    sections = [(seg.title, seg.lyrics.text if seg.lyrics is not None else None)
                for seg in song.segments]
    if not sections:
        return None

    img_w_px  = lu.img_width_px
    page_h_pt = A4_HEIGHT_PT - lu.cfg.page.top_margin_pt - lu.cfg.page.bottom_margin_pt
    img_h_px  = lu.px(page_h_pt)

    img  = Image.new('RGB', (img_w_px, img_h_px), color='white')
    draw = ImageDraw.Draw(img)

    margin_px     = lu.margin_left_px
    title_line_h  = int(lu.px(lu.cfg.fonts.title_pt)  * 1.4)
    lyrics_line_h = int(lu.px(lu.cfg.fonts.lyrics_pt) * 1.4)
    section_gap   = lyrics_line_h
    top_pad_px    = lu.px(lu.cfg.page.top_margin_pt * 0.5)

    title_w = draw.textbbox((0, 0), song.title, font=lu.title_font)[2]
    draw.text(((img_w_px - title_w) // 2, top_pad_px), song.title,
              fill="black", font=lu.title_font)
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
            draw.text((x, y), title, fill="black", font=lu.title_font)
            y += title_line_h
            if lyrics:
                for line in lyrics.splitlines():
                    draw.text((x, y), line, fill="black", font=lu.lyrics_font)
                    y += lyrics_line_h
            y += section_gap

    return img