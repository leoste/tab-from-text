"""Row-level drawing — things that belong to a system of six string lines."""
import tabfromtext.render.LayoutUtils as lu


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
         (lu.margin_left_px, y_top + 5 * lu.line_sp_px)],
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
         (bar_x, strings_y + 5 * lu.line_sp_px)],
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
         (lu.margin_left_px + lu.content_w_px, strings_y + 5 * lu.line_sp_px)],
        fill="black", width=lu.lw(cfg.line_width.normal_pt),
    )


def draw_final_barline(draw_obj, final_x, final_y):
    """Draw the closing barline after the last note of a segment."""
    cfg = lu.cfg
    draw_obj.line(
        [(final_x, final_y),
         (final_x, final_y + 5 * lu.line_sp_px)],
        fill="black", width=lu.lw(cfg.line_width.normal_pt),
    )