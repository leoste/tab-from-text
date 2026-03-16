import math
from PIL import Image, ImageDraw
from tabfromtext.song.Segment import Segment
from tabfromtext.song.Song import Song
from tabfromtext.render.LayoutConfig import LayoutConfig
from tabfromtext.render.RenderContexts import NoteContext, ChunkContext
from tabfromtext.render.RowPainter import (
    draw_row, draw_barline, draw_row_end_barline, draw_final_barline,
)
from tabfromtext.render.NotePainter import draw_note
from tabfromtext.util.TimeUtils import convertTimeToTicks
import tabfromtext.render.LayoutUtils as lu


# ---------------------------------------------------------------------------
# Context builders
# ---------------------------------------------------------------------------

def _build_note_context(note, idx, segment_notes, tick, base_y,
                        last_style, last_pm_x, last_pm_y) -> NoteContext:
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
        idx=idx,
        segment_notes=segment_notes,
        tick=tick,
        strings_y=lu.tick_to_strings_y(tick, base_y),
        x=x,
        next_x=x + dur * lu.beat_w_px,
        is_new_line=lu.is_new_system(tick),
        prev_real_note=segment_notes[prev_real_idx] if prev_real_idx is not None else None,
        next_real_note=segment_notes[next_real_idx] if next_real_idx is not None else None,
        last_style=last_style,
        last_pm_x=last_pm_x,
        last_pm_y=last_pm_y,
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

def _render_note(draw, note_ctx: NoteContext, base_y, global_measure_counter):
    """Handle row/barline housekeeping and draw all chunks of one note.
    Returns updated (last_pm_x, last_pm_y)."""
    if note_ctx.is_new_line:
        draw_row(draw, note_ctx.strings_y, global_measure_counter)
        note_ctx.last_pm_x = None
        note_ctx.last_pm_y = None

    if (lu.tick_to_unit_in_measure(note_ctx.tick) == 0
            and lu.tick_to_measure_in_system(note_ctx.tick) > 0):
        draw_barline(draw, note_ctx.strings_y,
                     lu.barline_x(note_ctx.tick), global_measure_counter)

    remaining_dur     = note_ctx.note.duration
    chunk_acc         = note_ctx.tick
    prev_stem_x       = None
    prev_stem_y_start = None

    while remaining_dur > 0:
        ticks_left = lu.UNITS_PER_MEASURE - lu.tick_to_unit_in_measure(chunk_acc)
        chunk_dur  = min(remaining_dur, ticks_left)
        chunk_ctx  = _build_chunk_context(chunk_acc, chunk_dur, note_ctx.tick, base_y)

        if chunk_ctx.is_new_line and not chunk_ctx.is_first:
            draw_row(draw, chunk_ctx.strings_y, global_measure_counter)
            note_ctx.last_pm_x = None
            note_ctx.last_pm_y = None

        if lu.is_new_measure(chunk_acc) and not chunk_ctx.is_first:
            draw_barline(draw, chunk_ctx.strings_y,
                         lu.barline_x(chunk_acc), global_measure_counter)

        note_ctx.last_pm_x, note_ctx.last_pm_y = draw_note(
            draw, note_ctx, chunk_ctx, prev_stem_x, prev_stem_y_start,
        )

        prev_stem_x       = chunk_ctx.stem_x
        prev_stem_y_start = chunk_ctx.stem_y
        chunk_acc         += chunk_dur
        remaining_dur     -= chunk_dur

        if lu.is_new_system(chunk_acc):
            draw_row_end_barline(draw, lu.tick_to_strings_y(chunk_acc - 1, base_y))

    return note_ctx.last_pm_x, note_ctx.last_pm_y


def _advance_measure_counter(note, acc_dur_segment, global_measure_counter):
    """Increment the measure counter for each measure boundary crossed by this note."""
    chunk_acc     = acc_dur_segment
    remaining_dur = note.duration
    while remaining_dur > 0:
        ticks_left = lu.UNITS_PER_MEASURE - lu.tick_to_unit_in_measure(chunk_acc)
        chunk_dur  = min(remaining_dur, ticks_left)
        chunk_acc     += chunk_dur
        remaining_dur -= chunk_dur
        if lu.is_new_measure(chunk_acc):
            global_measure_counter += 1
    return global_measure_counter


# ---------------------------------------------------------------------------
# Segment image allocation
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Lyrics
# ---------------------------------------------------------------------------

def _draw_lyrics(draw_obj, segment, base_y):
    """Draw syllable-aligned inline lyrics below the string lines."""
    from tabfromtext.util.SyllableUtils import split_syllables

    lyrics_y_off_px = lu.px(lu.cfg.lyrics.y_offset_pt)
    flat_syllables  = split_syllables(segment.lyrics.text)
    tick_list       = segment.lyrics.flatten_durations()
    offset_ticks    = convertTimeToTicks(segment.lyrics.offset)

    syllable_events = []
    syl_idx  = 0
    abs_tick = offset_ticks
    for entry in tick_list:
        if entry is not None and syl_idx < len(flat_syllables):
            syllable_events.append((abs_tick, flat_syllables[syl_idx]))
            syl_idx += 1
        abs_tick += 1

    for abs_tick, syl_text in syllable_events:
        syl_strings_y = lu.tick_to_strings_y(abs_tick, base_y)
        syl_y         = syl_strings_y + 5 * lu.line_sp_px + lyrics_y_off_px
        syl_x_left    = lu.tick_to_x(abs_tick)
        text_w        = draw_obj.textbbox((0, 0), syl_text, font=lu.lyrics_tab_font)[2]
        draw_obj.text(
            (syl_x_left - text_w // 2, syl_y),
            syl_text, fill="black", font=lu.lyrics_tab_font,
        )


# ---------------------------------------------------------------------------
# Public render entry points
# ---------------------------------------------------------------------------

def render_tab(segments: list[Segment], instrument_name: str,
               output_base_path: str = "guitar_tab",
               cfg: LayoutConfig = None) -> list[tuple[str, object]]:
    results = []
    global_measure_counter = 1

    for seg_idx, segment in enumerate(segments):
        img, draw, base_y = _create_segment_image(segment, instrument_name)
        draw.text((lu.margin_left_px, lu.px(lu.cfg.page.title_padding_pt)),
                  segment.title, fill="black", font=lu.title_font)

        segment_notes   = segment.GetNotesFromSegment(instrument_name)
        acc_dur_segment = 0
        last_style      = None
        last_pm_x       = None
        last_pm_y       = None
        final_x         = lu.margin_left_px
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

        if not lu.is_new_system(acc_dur_segment):
            draw_final_barline(draw, final_x, final_y)

        if segment.lyrics is not None:
            _draw_lyrics(draw, segment, base_y)

        safe_title = "".join(
            c for c in segment.title if c.isalnum() or c in (' ', '_')
        ).strip().replace(' ', '_')
        results.append((f"{output_base_path}_{seg_idx + 1}_{safe_title}.png", img))

    return results


def render_title_page(song: Song, cfg: LayoutConfig = None,
                      num_columns: int = 2) -> Image.Image | None:
    sections = [(seg.title, seg.lyrics.text if seg.lyrics is not None else None)
                for seg in song.segments]
    if not sections:
        return None

    from reportlab.lib.pagesizes import A4
    A4_WIDTH_PT, A4_HEIGHT_PT = A4

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