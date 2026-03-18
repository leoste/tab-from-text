"""Row-level drawing — things that belong to a system of six string lines,
including lyrics which span the full row."""
import tabfromtext.render.LayoutUtils as lu
from tabfromtext.render.LayoutUtils import STRING_GAPS, STRING_COUNT
from tabfromtext.util.TimeUtils import convertTimeToTicks


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


def draw_lyrics_only(draw_obj, segment, base_y):
    """Draw syllables for a lyrics-only row, where base_y is the top of the
    lyrics area (no tab strings). Each syllable is placed at its tick-aligned
    x position. Multiple rows are stacked vertically when the lyrics span
    more than one system-width."""
    from tabfromtext.util.SyllableUtils import split_syllables

    flat_syllables = split_syllables(segment.lyrics.text)
    tick_list      = segment.lyrics.flatten_durations()
    offset_ticks   = convertTimeToTicks(segment.lyrics.offset)

    syllable_events = []
    syl_idx  = 0
    abs_tick = offset_ticks
    for entry in tick_list:
        if entry is not None and syl_idx < len(flat_syllables):
            syllable_events.append((abs_tick, flat_syllables[syl_idx]))
            syl_idx += 1
        abs_tick += 1

    line_h_px = lu.px(lu.cfg.fonts.lyrics_tab_pt) * 2

    for abs_tick, syl_text in syllable_events:
        row    = lu.tick_to_system(abs_tick)
        syl_y  = base_y + row * line_h_px
        syl_x  = lu.tick_to_x(abs_tick)
        text_w = draw_obj.textbbox((0, 0), syl_text, font=lu.lyrics_tab_font)[2]
        draw_obj.text(
            (syl_x - text_w // 2, syl_y),
            syl_text, fill="black", font=lu.lyrics_tab_font,
        )


def draw_lyrics(draw_obj, segment, base_y):
    """Draw all syllables of the segment's lyrics, aligned to their tick positions."""
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
        syl_y = syl_strings_y + STRING_GAPS * lu.line_sp_px + lyrics_y_off_px
        syl_x_left    = lu.tick_to_x(abs_tick)
        text_w        = draw_obj.textbbox((0, 0), syl_text, font=lu.lyrics_tab_font)[2]
        draw_obj.text(
            (syl_x_left - text_w // 2, syl_y),
            syl_text, fill="black", font=lu.lyrics_tab_font,
        )