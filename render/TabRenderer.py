import math
from PIL import Image, ImageDraw
from song.object.StrumStyle import StrumStyle
from song.object.Segment import Segment
from object.TimeUtils import TIME_RESOLUTION, convertTimeToTicks
from song.object.Song import Song
from render.LayoutConfig import LayoutConfig

MEASURES_PER_LINE = 4
UNITS_PER_MEASURE = 8 * TIME_RESOLUTION

# Tick thresholds (unit counts, not pixels)
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


def draw_arc(draw_obj, cfg: LayoutConfig, x_start, x_end, y_top):
    top_off = cfg.px(cfg.arc_top_offset_pt)
    bot_off = cfg.px(cfg.arc_bot_offset_pt)
    arc_box = [x_start, y_top - top_off, x_end, y_top - bot_off]
    draw_obj.arc(arc_box, start=180, end=0, fill="black", width=cfg.lw(cfg.line_width_thin_pt))


def draw_stem(draw_obj, cfg: LayoutConfig, stem_x, stem_y_start, duration, is_rest: bool = False):
    if is_rest:
        full_h = cfg.px(cfg.stem_h_pt)
        rest_h = cfg.px(cfg.rest_stem_pt)
        draw_obj.line([(stem_x, stem_y_start + full_h - rest_h),
                       (stem_x, stem_y_start + full_h)],
                      fill="black", width=cfg.lw(cfg.line_width_normal_pt))
        return
    if duration >= TICKS_FULL_NOTE:
        draw_obj.line([(stem_x, stem_y_start),
                       (stem_x, stem_y_start + cfg.px(cfg.full_h_pt))],
                      fill="black", width=cfg.lw(cfg.line_width_normal_pt))
    elif duration >= TICKS_HALF_NOTE:
        top_h = cfg.px(cfg.half_top_h_pt)
        gap   = cfg.px(cfg.half_gap_pt)
        bot_h = cfg.px(cfg.half_bottom_h_pt)
        draw_obj.line([(stem_x, stem_y_start),
                       (stem_x, stem_y_start + top_h)],
                      fill="black", width=cfg.lw(cfg.line_width_normal_pt))
        draw_obj.line([(stem_x, stem_y_start + top_h + gap),
                       (stem_x, stem_y_start + top_h + gap + bot_h)],
                      fill="black", width=cfg.lw(cfg.line_width_normal_pt))
    else:
        draw_obj.line([(stem_x, stem_y_start),
                       (stem_x, stem_y_start + cfg.px(cfg.stem_h_pt))],
                      fill="black", width=cfg.lw(cfg.line_width_normal_pt))


def draw_staff_elements(draw_obj, cfg: LayoutConfig, fret_font, small_font, string_name_font,
                        y_top, start_measure_num):
    """Draw the six string lines, left barline, string names, and measure number
    for one system.  y_top is the y coordinate of the 1st string line."""
    string_names = ['e', 'B', 'G', 'D', 'A', 'E']
    line_sp      = cfg.px(cfg.line_spacing_pt)
    margin_left  = cfg.px(cfg.margin_left_pt)
    content_w    = cfg.px(_line_content_width_pt(cfg))
    mnum_y_off   = cfg.px(cfg.measure_num_y_offset_pt)
    font_h       = cfg.px(cfg.string_name_font_size_pt)

    for i, name in enumerate(string_names):
        y = y_top + (i * line_sp)
        draw_obj.text((margin_left - cfg.px(cfg.string_name_x_pt) - font_h, y - (font_h // 2)),
                      name, fill="black", font=string_name_font)
        draw_obj.line([(margin_left, y), (margin_left + content_w, y)],
                      fill=(200, 200, 200), width=cfg.lw(cfg.line_width_thin_pt))

    draw_obj.line([(margin_left, y_top), (margin_left, y_top + 5 * line_sp)],
                  fill="black", width=cfg.lw(cfg.line_width_normal_pt))
    draw_obj.text((margin_left, y_top + mnum_y_off),
                  str(start_measure_num), fill="gray", font=small_font)


def draw_dashed_segment(draw_obj, cfg: LayoutConfig, x_start, x_end, y):
    dash_gap = cfg.px(cfg.dash_gap_pt)
    curr = x_start
    while curr < x_end:
        draw_obj.line([(curr, y), (min(curr + dash_gap, x_end), y)],
                      fill="black", width=cfg.lw(cfg.line_width_thin_pt))
        curr += dash_gap * 2


def _line_content_width_pt(cfg: LayoutConfig) -> float:
    measure_width_pt = (UNITS_PER_MEASURE * cfg.eighth_note_width_pt) + cfg.bar_padding_pt
    return MEASURES_PER_LINE * measure_width_pt


def render_tab(segments: list[Segment], instrument_name: str,
               output_base_path: str = "guitar_tab",
               cfg: LayoutConfig = None) -> list[tuple[str, object]]:
    if cfg is None:
        cfg = LayoutConfig()

    title_font, fret_font, small_font, string_name_font, annotation_font, _lyrics_font, lyrics_tab_font = cfg.load_fonts()

    line_content_width_pt = _line_content_width_pt(cfg)
    measure_width_pt      = (UNITS_PER_MEASURE * cfg.eighth_note_width_pt) + cfg.bar_padding_pt

    # Pre-compute pixel values used repeatedly in the inner loop
    margin_left_px    = cfg.px(cfg.margin_left_pt)
    margin_right_px   = cfg.px(cfg.margin_right_pt)
    line_sp_px        = cfg.px(cfg.line_spacing_pt)
    beat_w_px         = cfg.px(cfg.eighth_note_width_pt)
    bar_pad_px        = cfg.px(cfg.bar_padding_pt)
    measure_w_px      = cfg.px(measure_width_pt)
    content_w_px      = cfg.px(line_content_width_pt)
    title_h_px        = cfg.px(cfg.title_height_pt)
    system_h_px       = cfg.px(cfg.system_height_pt)
    above_str_px      = cfg.px(cfg.above_strings_pt)
    pm_y_off_px       = cfg.px(cfg.pm_y_offset_pt)
    tick_h_px         = cfg.px(cfg.tick_h_pt)
    mnum_y_off_px     = cfg.px(cfg.measure_num_y_offset_pt)
    stem_h_px         = cfg.px(cfg.stem_h_pt)
    stem_x_off_px     = cfg.px(cfg.stem_x_offset_pt)
    top_padding_px    = cfg.px(cfg.title_padding_pt)
    bottom_padding_px = cfg.px(cfg.below_strings_pt)
    pm_label_y_px     = cfg.px(cfg.pm_label_y_pt)
    pm_label_w_px     = cfg.px(cfg.pm_label_w_pt)
    dot_offset_px     = cfg.px(cfg.dot_offset_pt)
    dot_r_px          = cfg.px(cfg.dot_r_pt)
    beam_stub_px      = cfg.px(cfg.beam_stub_pt)
    slide_nudge_px    = cfg.px(cfg.slide_nudge_pt)

    img_width_px = content_w_px + margin_left_px + margin_right_px

    results = []
    global_measure_counter = 1

    for seg_idx, segment in enumerate(segments):
        segment_notes = segment.GetNotesFromSegment(instrument_name)
        total_units   = sum((n.duration if n.duration else 0) for n in segment_notes)
        num_measures  = math.ceil(total_units / UNITS_PER_MEASURE)
        num_systems   = math.ceil(num_measures / MEASURES_PER_LINE)

        img_height_px = title_h_px + (num_systems * system_h_px) + bottom_padding_px

        img  = Image.new('RGB', (int(img_width_px), int(img_height_px)), color='white')
        draw = ImageDraw.Draw(img)

        # --- Title ---
        current_y_cursor = top_padding_px
        draw.text((margin_left_px, current_y_cursor), segment.title,
                  fill="black", font=title_font)
        current_y_cursor += title_h_px

        acc_dur_segment = 0
        last_style      = None
        last_pm_x       = None
        last_pm_y       = None
        final_x         = margin_left_px
        final_y         = current_y_cursor

        for idx, note in enumerate(segment_notes):
            total_beats_in_segment = acc_dur_segment // UNITS_PER_MEASURE
            system_in_segment      = int(acc_dur_segment // (UNITS_PER_MEASURE * MEASURES_PER_LINE))
            measure_in_system      = int(total_beats_in_segment % MEASURES_PER_LINE)
            unit_in_measure        = acc_dur_segment % UNITS_PER_MEASURE

            # y_top = top of the system row = current_y_cursor + system offset
            # 1st string line = y_top + above_strings_pt
            row_y_top      = current_y_cursor + (system_in_segment * system_h_px)
            row_strings_y  = row_y_top + above_str_px   # y of the 1st string line
            is_new_line    = (acc_dur_segment % (UNITS_PER_MEASURE * MEASURES_PER_LINE) == 0)

            current_x = margin_left_px + (measure_in_system * measure_w_px) + (unit_in_measure * beat_w_px) + bar_pad_px
            note_dur  = (note.duration or 0)
            next_x    = current_x + (note_dur * beat_w_px)

            if note.duration is not None:
                final_y = row_strings_y
                final_x = next_x
                if is_new_line:
                    draw_staff_elements(draw, cfg, fret_font, small_font, string_name_font,
                                        row_strings_y, global_measure_counter)
                    last_pm_x = None
                    last_pm_y = None
                if unit_in_measure == 0 and measure_in_system > 0:
                    bar_x = margin_left_px + (measure_in_system * measure_w_px)
                    draw.line([(bar_x, row_strings_y),
                               (bar_x, row_strings_y + 5 * line_sp_px)],
                              fill="black", width=cfg.lw(cfg.line_width_normal_pt))
                    draw.text((bar_x, row_strings_y + mnum_y_off_px),
                              str(global_measure_counter), fill="gray", font=small_font)

            if note.duration is not None:
                remaining_dur     = note.duration
                chunk_acc         = acc_dur_segment
                prev_stem_x       = None
                prev_stem_y_start = None

                while remaining_dur > 0:
                    ticks_left_in_measure = UNITS_PER_MEASURE - (chunk_acc % UNITS_PER_MEASURE)
                    chunk_dur = min(remaining_dur, ticks_left_in_measure)

                    chunk_total_beats       = chunk_acc // UNITS_PER_MEASURE
                    chunk_system            = int(chunk_acc // (UNITS_PER_MEASURE * MEASURES_PER_LINE))
                    chunk_measure_in_system = int(chunk_total_beats % MEASURES_PER_LINE)
                    chunk_unit_in_measure   = chunk_acc % UNITS_PER_MEASURE

                    chunk_row_y_top   = current_y_cursor + (chunk_system * system_h_px)
                    chunk_strings_y   = chunk_row_y_top + above_str_px
                    chunk_stem_y_start = chunk_strings_y + (6 * line_sp_px)

                    chunk_is_new_line = (chunk_acc % (UNITS_PER_MEASURE * MEASURES_PER_LINE) == 0)
                    if chunk_is_new_line and chunk_acc != acc_dur_segment:
                        draw_staff_elements(draw, cfg, fret_font, small_font, string_name_font,
                                            chunk_strings_y, global_measure_counter)
                        last_pm_x = None
                        last_pm_y = None

                    chunk_x      = margin_left_px + (chunk_measure_in_system * measure_w_px) + (chunk_unit_in_measure * beat_w_px) + bar_pad_px
                    chunk_stem_x = chunk_x + stem_x_off_px
                    chunk_next_x = chunk_x + (chunk_dur * beat_w_px)

                    if chunk_unit_in_measure == 0 and chunk_acc != acc_dur_segment:
                        bar_x = margin_left_px + (chunk_measure_in_system * measure_w_px)
                        draw.line([(bar_x, chunk_strings_y),
                                   (bar_x, chunk_strings_y + 5 * line_sp_px)],
                                  fill="black", width=cfg.lw(cfg.line_width_normal_pt))
                        draw.text((bar_x, chunk_strings_y + mnum_y_off_px),
                                  str(global_measure_counter), fill="gray", font=small_font)

                    if note.chord and note.style != StrumStyle.NO_HIT:
                        strings = [note.chord.string1, note.chord.string2, note.chord.string3,
                                   note.chord.string4, note.chord.string5, note.chord.string6]
                        for i, fret in enumerate(strings):
                            if fret is not None and fret != -1:
                                y     = chunk_strings_y + (i * line_sp_px)
                                label = "X" if note.style == StrumStyle.MUTED else str(fret)

                                text_w, text_h = draw.textbbox((0, 0), label, font=fret_font)[2:]
                                draw.rectangle([chunk_x - 2, y - (text_h // 2),
                                                chunk_x + text_w + 2, y + (text_h // 2)],
                                               fill="white")
                                draw.text((chunk_x, y - (text_h // 2)),
                                          label, fill="black", font=fret_font)

                                if note.style == StrumStyle.SLIDE:
                                    draw.line([(chunk_x + text_w + slide_nudge_px, y),
                                               (chunk_next_x - slide_nudge_px, y)],
                                              fill="black", width=cfg.lw(cfg.line_width_thin_pt))
                                    draw_arc(draw, cfg,
                                             chunk_x + slide_nudge_px,
                                             chunk_next_x - slide_nudge_px,
                                             chunk_strings_y + (i * line_sp_px))

                        if note.style == StrumStyle.PALM_MUTED:
                            pm_y = chunk_strings_y + pm_y_off_px
                            is_first_pm_on_line = (last_style != StrumStyle.PALM_MUTED or chunk_is_new_line)
                            next_real_note = next(
                                (segment_notes[i] for i in range(idx + 1, len(segment_notes))
                                 if segment_notes[i].duration is not None), None)
                            is_last_pm = (next_real_note is None or
                                          next_real_note.style != StrumStyle.PALM_MUTED)
                            if is_first_pm_on_line:
                                draw.text((chunk_x, pm_y - pm_label_y_px), "P.M.",
                                          fill="black", font=annotation_font)
                                last_pm_x = chunk_x + pm_label_w_px
                            else:
                                draw_dashed_segment(draw, cfg, last_pm_x, chunk_x, pm_y)
                                last_pm_x = chunk_x
                            if is_last_pm and not is_first_pm_on_line:
                                draw.line([(chunk_x, pm_y - tick_h_px // 2),
                                           (chunk_x, pm_y + tick_h_px // 2)],
                                          fill="black", width=cfg.lw(cfg.line_width_thin_pt))
                            last_pm_y = pm_y

                    is_rest = (note.chord is None or note.style == StrumStyle.NO_HIT)
                    draw_stem(draw, cfg, chunk_stem_x, chunk_stem_y_start, chunk_dur, is_rest=is_rest)

                    if chunk_acc == acc_dur_segment and is_dotted(note.duration):
                        dot_x = chunk_stem_x + dot_offset_px
                        dot_y = chunk_stem_y_start + dot_offset_px
                        draw.ellipse([dot_x - dot_r_px, dot_y - dot_r_px,
                                      dot_x + dot_r_px, dot_y + dot_r_px], fill="black")

                    if prev_stem_x is not None:
                        draw_arc(draw, cfg, prev_stem_x, chunk_stem_x,
                                 min(prev_stem_y_start, chunk_stem_y_start))

                    if chunk_dur == TICKS_EIGHTH or chunk_dur == TICKS_DOTTED_EIGHTH:
                        chunk_bottom_y = chunk_stem_y_start + stem_h_px
                        next_real_idx  = next(
                            (i for i in range(idx + 1, len(segment_notes))
                             if segment_notes[i].duration is not None), None)
                        next_real_note = segment_notes[next_real_idx] if next_real_idx is not None else None

                        prev_real_idx  = next(
                            (i for i in range(idx - 1, -1, -1)
                             if segment_notes[i].duration is not None), None)
                        prev_real_note = segment_notes[prev_real_idx] if prev_real_idx is not None else None

                        is_at_measure_end  = (chunk_acc + chunk_dur) % UNITS_PER_MEASURE == 0
                        can_beam_fwd = (not is_at_measure_end
                                        and next_real_note is not None
                                        and next_real_note.duration == note.duration
                                        and note.chord is not None
                                        and next_real_note.chord is not None)

                        is_at_measure_start = (chunk_acc % UNITS_PER_MEASURE == 0)
                        is_beamed_back = (not is_at_measure_start
                                          and prev_real_note is not None
                                          and prev_real_note.duration == note.duration
                                          and note.chord is not None
                                          and prev_real_note.chord is not None)

                        if can_beam_fwd:
                            draw.line([(chunk_stem_x, chunk_bottom_y),
                                       (chunk_stem_x + beat_w_px * chunk_dur, chunk_bottom_y)],
                                      fill="black", width=cfg.lw(cfg.line_width_thick_pt))
                        elif not is_beamed_back:
                            draw.line([(chunk_stem_x, chunk_bottom_y),
                                       (chunk_stem_x + beam_stub_px, chunk_bottom_y)],
                                      fill="black", width=cfg.lw(cfg.line_width_normal_pt))

                    prev_stem_x       = chunk_stem_x
                    prev_stem_y_start = chunk_stem_y_start
                    chunk_acc     += chunk_dur
                    remaining_dur -= chunk_dur

                    if chunk_acc % UNITS_PER_MEASURE == 0:
                        global_measure_counter += 1

                    if chunk_acc % (UNITS_PER_MEASURE * MEASURES_PER_LINE) == 0:
                        eol_system    = int((chunk_acc - 1) // (UNITS_PER_MEASURE * MEASURES_PER_LINE))
                        eol_strings_y = current_y_cursor + (eol_system * system_h_px) + above_str_px
                        draw.line([(margin_left_px + content_w_px, eol_strings_y),
                                   (margin_left_px + content_w_px, eol_strings_y + 5 * line_sp_px)],
                                  fill="black", width=cfg.lw(cfg.line_width_normal_pt))

            if note.style is not None:
                last_style = note.style
            acc_dur_segment += (note.duration if note.duration else 0)

        if acc_dur_segment % (UNITS_PER_MEASURE * MEASURES_PER_LINE) != 0:
            draw.line([(final_x, final_y),
                       (final_x, final_y + 5 * line_sp_px)],
                      fill="black", width=cfg.lw(cfg.line_width_normal_pt))

        if segment.lyrics is not None:
            from object.SyllableUtils import split_syllables

            lyrics_y_off_px = cfg.px(cfg.lyrics_y_offset_pt)
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
                syl_system          = int(abs_tick // (UNITS_PER_MEASURE * MEASURES_PER_LINE))
                syl_total_measures  = abs_tick // UNITS_PER_MEASURE
                syl_measure_in_sys  = int(syl_total_measures % MEASURES_PER_LINE)
                syl_unit_in_measure = abs_tick % UNITS_PER_MEASURE

                syl_row_y_top   = current_y_cursor + (syl_system * system_h_px)
                syl_strings_y   = syl_row_y_top + above_str_px
                syl_y           = syl_strings_y + (5 * line_sp_px) + lyrics_y_off_px

                syl_x_left = (margin_left_px
                              + syl_measure_in_sys * measure_w_px
                              + syl_unit_in_measure * beat_w_px
                              + bar_pad_px)

                text_w = draw.textbbox((0, 0), syl_text, font=lyrics_tab_font)[2]
                syl_x  = syl_x_left - text_w // 2

                draw.text((syl_x, syl_y), syl_text, fill="black", font=lyrics_tab_font)

        safe_title = "".join(
            [c for c in segment.title if c.isalnum() or c in (' ', '_')]
        ).strip().replace(' ', '_')
        file_path = f"{output_base_path}_{seg_idx + 1}_{safe_title}.png"
        results.append((file_path, img))

    return results


def render_title_page(song: Song, cfg: LayoutConfig = None,
                      num_columns: int = 2) -> Image.Image | None:
    # Collect segments that have lyrics or are worth listing on the title page
    sections = [(seg.title, seg.lyrics.text if seg.lyrics is not None else None) for seg in song.segments]
    has_content = any(lyrics for _, lyrics in sections)
    if not sections:
        return None

    if cfg is None:
        cfg = LayoutConfig()

    title_font, _fret, _small, _str_name, _ann, lyrics_font, _lyrics_tab = cfg.load_fonts()

    from reportlab.lib.pagesizes import A4
    A4_WIDTH_PT, A4_HEIGHT_PT = A4

    img_w_px = cfg.px(cfg.printable_width_pt if cfg.printable_width_pt > 0
                      else cfg._natural_width_pt)
    page_h_pt = A4_HEIGHT_PT - cfg.page_top_margin_pt - cfg.page_bottom_margin_pt
    img_h_px  = cfg.px(page_h_pt)

    img  = Image.new('RGB', (img_w_px, img_h_px), color='white')
    draw = ImageDraw.Draw(img)

    margin_px    = cfg.px(cfg.margin_left_pt)
    title_fs_px  = cfg.px(cfg.title_font_size_pt)
    lyrics_fs_px = cfg.px(cfg.lyrics_font_size_pt)

    title_line_h  = int(title_fs_px  * 1.4)
    lyrics_line_h = int(lyrics_fs_px * 1.4)
    section_gap   = lyrics_line_h

    top_pad_px = cfg.px(cfg.page_top_margin_pt * 0.5)

    # --- Song title (centered across full width) ---
    title_w = draw.textbbox((0, 0), song.title, font=title_font)[2]
    title_x = (img_w_px - title_w) // 2
    draw.text((title_x, top_pad_px), song.title, fill="black", font=title_font)
    columns_top_y = top_pad_px + title_line_h * 2

    # --- Column geometry ---
    usable_w   = img_w_px - 2 * margin_px
    col_gap    = margin_px
    col_w      = (usable_w - col_gap * (num_columns - 1)) // num_columns
    col_starts = [margin_px + i * (col_w + col_gap) for i in range(num_columns)]
    col_bottom = img_h_px
    col_height = col_bottom - columns_top_y

    # --- Pre-compute height of each section block ---
    def section_height(title, lyrics) -> int:
        h = title_line_h
        if lyrics:
            h += len(lyrics.splitlines()) * lyrics_line_h
        h += section_gap
        return h

    # --- Distribute sections into columns greedily ---
    columns: list[list] = [[] for _ in range(num_columns)]
    col_used = [0] * num_columns
    col_idx  = 0

    for title, lyrics in sections:
        sh = section_height(title, lyrics)
        if col_used[col_idx] + sh > col_height and col_idx < num_columns - 1:
            col_idx += 1
        columns[col_idx].append((title, lyrics))
        col_used[col_idx] += sh

    # --- Draw columns ---
    for c_idx, col_sections in enumerate(columns):
        x = col_starts[c_idx]
        y = columns_top_y
        for title, lyrics in col_sections:
            draw.text((x, y), title, fill="black", font=title_font)
            y += title_line_h

            if lyrics:
                for line in lyrics.splitlines():
                    draw.text((x, y), line, fill="black", font=lyrics_font)
                    y += lyrics_line_h

            y += section_gap

    return img


def render_song(song: Song, cfg: LayoutConfig = None) -> list[tuple[str, object]]:
    results = []
    safe_song_title = song.title.lower().replace(' ', '_')
    for instrument in song.instruments:
        safe_instrument_name = instrument.name.lower().replace(' ', '_')
        output_base_path = f"tabs/{safe_song_title}/{safe_instrument_name}/tab"
        results += render_tab(instrument.segments, instrument.name, output_base_path, cfg)
    return results