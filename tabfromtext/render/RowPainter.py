"""Row-level drawing — things that belong to a system of six string lines,
including lyrics which span the full row."""
import math
import tabfromtext.render.LayoutUtils as lu
from tabfromtext.render.LayoutUtils import STRING_GAPS, STRING_COUNT
from tabfromtext.util.TimeUtils import convertTimeToTicks


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def lyrics_line_h_px() -> int:
    """Height of one lyrics-only row in pixels, mirroring system_h_px anatomy:
    above_strings_pt (top margin) + font height + below_strings_pt (bottom margin)."""
    return lu.px(lu.cfg.row.above_strings_pt + lu.cfg.fonts.lyrics_tab_pt + lu.cfg.row.below_strings_pt)


def _build_syllable_events(segment) -> list[tuple[int, str]]:
    """Return [(abs_tick, syllable_text), ...] for a segment's lyrics."""
    from tabfromtext.util.SyllableUtils import split_syllables

    flat_syllables = split_syllables(segment.lyrics.text)
    tick_list      = segment.lyrics.flatten_durations()
    offset_ticks   = convertTimeToTicks(segment.lyrics.offset)

    events   = []
    syl_idx  = 0
    abs_tick = offset_ticks
    for entry in tick_list:
        if entry is not None and syl_idx < len(flat_syllables):
            events.append((abs_tick, flat_syllables[syl_idx]))
            syl_idx += 1
        abs_tick += 1
    return events


# ---------------------------------------------------------------------------
# Segment title
# ---------------------------------------------------------------------------

def draw_segment_title(draw_obj, title: str):
    """Draw the segment title at the standard top-left position."""
    draw_obj.text(
        (lu.margin_left_px, lu.px(lu.cfg.page.title_padding_pt)),
        title, fill="black", font=lu.title_font,
    )


# ---------------------------------------------------------------------------
# Tab row primitives
# ---------------------------------------------------------------------------

def draw_row(draw_obj, y_top, start_measure_num):
    """Draw one complete system row: six string lines, opening barline,
    string names, and the measure number. y_top is the y of the 1st string."""
    cfg          = lu.cfg
    string_names = ['e', 'B', 'G', 'D', 'A', 'E']
    font_h       = lu.px(cfg.fonts.string_name_pt)
    mnum_y_off   = lu.px(cfg.measures.num_y_offset_pt)

    for i, name in enumerate(string_names):
        y = y_top + i * lu.line_sp_px
        draw_obj.text(
            (lu.margin_left_px - lu.px(cfg.row.string_name_x_pt) - font_h,
             y - font_h // 2),
            name, fill="black", font=lu.string_name_font,
        )
        draw_obj.line(
            [(lu.margin_left_px, y),
             (lu.margin_left_px + lu.content_w_px, y)],
            fill=(200, 200, 200), width=lu.lw(cfg.line_width.thin_pt),
        )

    draw_obj.line(
        [(lu.margin_left_px, y_top),
         (lu.margin_left_px, y_top + STRING_GAPS * lu.line_sp_px)],
        fill="black", width=lu.lw(cfg.line_width.normal_pt),
    )
    draw_obj.text(
        (lu.margin_left_px, y_top + mnum_y_off),
        str(start_measure_num), fill="gray", font=lu.small_font,
    )


def draw_barline(draw_obj, strings_y, bar_x, measure_num):
    """Draw a mid-row barline and its measure number label."""
    cfg = lu.cfg
    draw_obj.line(
        [(bar_x, strings_y),
         (bar_x, strings_y + STRING_GAPS * lu.line_sp_px)],
        fill="black", width=lu.lw(cfg.line_width.normal_pt),
    )
    draw_obj.text(
        (bar_x, strings_y + lu.px(cfg.measures.num_y_offset_pt)),
        str(measure_num), fill="gray", font=lu.small_font,
    )


def draw_row_end_barline(draw_obj, strings_y):
    """Draw the closing barline at the right edge of a system row."""
    cfg = lu.cfg
    draw_obj.line(
        [(lu.margin_left_px + lu.content_w_px, strings_y),
         (lu.margin_left_px + lu.content_w_px, strings_y + STRING_GAPS * lu.line_sp_px)],
        fill="black", width=lu.lw(cfg.line_width.normal_pt),
    )


def draw_final_barline(draw_obj, final_x, final_y):
    """Draw the closing barline after the last note of a segment."""
    cfg = lu.cfg
    draw_obj.line(
        [(final_x, final_y),
         (final_x, final_y + STRING_GAPS * lu.line_sp_px)],
        fill="black", width=lu.lw(cfg.line_width.normal_pt),
    )


# ---------------------------------------------------------------------------
# Lyrics drawing
# ---------------------------------------------------------------------------

def draw_lyrics(draw_obj, segment, base_y):
    """Draw all syllables of the segment's lyrics, aligned to their tick positions,
    below the tab strings."""
    lyrics_y_off_px = lu.px(lu.cfg.lyrics.y_offset_pt)

    for abs_tick, syl_text in _build_syllable_events(segment):
        syl_strings_y = lu.tick_to_strings_y(abs_tick, base_y)
        syl_y         = syl_strings_y + STRING_GAPS * lu.line_sp_px + lyrics_y_off_px
        syl_x         = lu.tick_to_x(abs_tick)
        text_w        = draw_obj.textbbox((0, 0), syl_text, font=lu.lyrics_tab_font)[2]
        draw_obj.text(
            (syl_x - text_w // 2, syl_y),
            syl_text, fill="black", font=lu.lyrics_tab_font,
        )


def draw_lyrics_only(draw_obj, segment, base_y):
    """Draw syllables for a lyrics-only segment (no tab strings).
    Rows are stacked vertically using lyrics_line_h_px() steps,
    with vertical barlines separating measures."""
    line_h       = lyrics_line_h_px()
    total_ticks  = segment.lyrics.total_ticks()
    num_measures = math.ceil(total_ticks / lu.UNITS_PER_MEASURE)
    measures_per_line = lu.MEASURES_PER_LINE
    font_h       = lu.px(lu.cfg.fonts.lyrics_tab_pt)
    above_px     = lu.above_str_px  # top margin within each row, same as tab rows

    def _bar(x, row):
        row_content_top = base_y + row * line_h + above_px
        draw_obj.line(
            [(x, row_content_top), (x, row_content_top + font_h)],
            fill="black", width=lu.lw(lu.cfg.line_width.normal_pt),
        )

    for measure_idx in range(num_measures):
        tick = measure_idx * lu.UNITS_PER_MEASURE
        row  = lu.tick_to_system(tick)

        # Opening barline of each measure (left edge of first measure = row open)
        _bar(lu.barline_x(tick), row)

        # If this is the last measure in a row, also draw the row-closing barline
        is_last_in_row     = (measure_idx + 1) % measures_per_line == 0
        is_last_measure    = measure_idx == num_measures - 1
        if is_last_in_row and not is_last_measure:
            _bar(lu.margin_left_px + lu.content_w_px, row)

    # Final closing barline at the actual end of the last measure
    last_tick   = total_ticks  # one past the last note
    last_row    = lu.tick_to_system(total_ticks - 1)
    measures_in_last_row = num_measures % measures_per_line or measures_per_line
    final_x = lu.margin_left_px + measures_in_last_row * lu.measure_w_px
    _bar(final_x, last_row)

    for abs_tick, syl_text in _build_syllable_events(segment):
        row    = lu.tick_to_system(abs_tick)
        syl_y  = base_y + row * line_h + above_px
        syl_x  = lu.tick_to_x(abs_tick)
        text_w = draw_obj.textbbox((0, 0), syl_text, font=lu.lyrics_tab_font)[2]
        draw_obj.text(
            (syl_x - text_w // 2, syl_y),
            syl_text, fill="black", font=lu.lyrics_tab_font,
        )