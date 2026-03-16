import math
from PIL import Image, ImageDraw
from tabfromtext.song.StrumStyle import StrumStyle
from tabfromtext.song.Segment import Segment
from tabfromtext.song.Song import Song
from tabfromtext.render.LayoutConfig import LayoutConfig
from tabfromtext.render.LayoutUtils import LayoutUtils, UNITS_PER_MEASURE, MEASURES_PER_LINE
from tabfromtext.util.TimeUtils import convertTimeToTicks, TIME_RESOLUTION

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
# Row-level drawing — things that belong to a system of six string lines
# ---------------------------------------------------------------------------

def draw_row(draw_obj, utils: LayoutUtils, fret_font, small_font,
             string_name_font, y_top, start_measure_num):
    """Draw one complete system row: six string lines, opening barline,
    string names, and the measure number. y_top is the y of the 1st string."""
    cfg          = utils.cfg
    string_names = ['e', 'B', 'G', 'D', 'A', 'E']
    font_h       = utils.px(cfg.fonts.string_name_pt)
    mnum_y_off   = utils.px(cfg.measures.num_y_offset_pt)

    for i, name in enumerate(string_names):
        y = y_top + i * utils.line_sp_px
        draw_obj.text(
            (utils.margin_left_px - utils.px(cfg.row.string_name_x_pt) - font_h,
             y - font_h // 2),
            name, fill="black", font=string_name_font,
        )
        draw_obj.line(
            [(utils.margin_left_px, y),
             (utils.margin_left_px + utils.content_w_px, y)],
            fill=(200, 200, 200), width=utils.lw(cfg.line_width.thin_pt),
        )

    draw_obj.line(
        [(utils.margin_left_px, y_top),
         (utils.margin_left_px, y_top + 5 * utils.line_sp_px)],
        fill="black", width=utils.lw(cfg.line_width.normal_pt),
    )
    draw_obj.text(
        (utils.margin_left_px, y_top + mnum_y_off),
        str(start_measure_num), fill="gray", font=small_font,
    )


def draw_barline(draw_obj, utils: LayoutUtils, small_font,
                 strings_y, bar_x, measure_num):
    """Draw a mid-row barline and its measure number label."""
    cfg = utils.cfg
    draw_obj.line(
        [(bar_x, strings_y),
         (bar_x, strings_y + 5 * utils.line_sp_px)],
        fill="black", width=utils.lw(cfg.line_width.normal_pt),
    )
    draw_obj.text(
        (bar_x, strings_y + utils.px(cfg.measures.num_y_offset_pt)),
        str(measure_num), fill="gray", font=small_font,
    )


def draw_row_end_barline(draw_obj, utils: LayoutUtils, strings_y):
    """Draw the closing barline at the right edge of a system row."""
    cfg = utils.cfg
    draw_obj.line(
        [(utils.margin_left_px + utils.content_w_px, strings_y),
         (utils.margin_left_px + utils.content_w_px, strings_y + 5 * utils.line_sp_px)],
        fill="black", width=utils.lw(cfg.line_width.normal_pt),
    )


def draw_final_barline(draw_obj, utils: LayoutUtils, final_x, final_y):
    """Draw the closing barline after the last note of a segment."""
    cfg = utils.cfg
    draw_obj.line(
        [(final_x, final_y),
         (final_x, final_y + 5 * utils.line_sp_px)],
        fill="black", width=utils.lw(cfg.line_width.normal_pt),
    )


# ---------------------------------------------------------------------------
# Note-level drawing — everything that belongs to a single note event
# ---------------------------------------------------------------------------

def draw_note(draw_obj, utils: LayoutUtils,
              fret_font, annotation_font,
              note, chunk_acc, chunk_dur,
              chunk_x, chunk_next_x, chunk_stem_x,
              strings_y, stem_y_start,
              is_first_chunk,
              prev_stem_x, prev_stem_y_start,
              next_real_note, prev_real_note,
              last_style,
              last_pm_x,
              segment_notes, idx):
    """Draw all visual elements that belong to one note-chunk:
      - fret numbers (or muted markers)
      - slide lines and arcs
      - palm mute annotation
      - stem
      - dot (dotted rhythm marker)
      - tie arc to previous chunk
      - beam or beam stub

    Returns updated (last_pm_x, last_pm_y) for palm mute state threading.
    """
    cfg = utils.cfg
    last_pm_y = None

    # --- Fret numbers, mute markers, slides ---
    if note.chord and note.style != StrumStyle.NO_HIT:
        last_pm_x, last_pm_y = _draw_fret_numbers(
            draw_obj, utils, fret_font, annotation_font,
            note, chunk_acc, chunk_x, chunk_next_x,
            strings_y,
            last_style, last_pm_x,
            segment_notes, idx,
        )

    # --- Stem ---
    is_rest = (note.chord is None or note.style == StrumStyle.NO_HIT)
    _draw_stem(draw_obj, utils, chunk_stem_x, stem_y_start, chunk_dur, is_rest=is_rest)

    # --- Dot (dotted rhythm) — only on the first chunk of the note ---
    if is_first_chunk and is_dotted(note.duration):
        _draw_dot(draw_obj, utils, chunk_stem_x, stem_y_start)

    # --- Tie arc to previous chunk (note spans a barline) ---
    if prev_stem_x is not None:
        draw_arc(draw_obj, utils, prev_stem_x, chunk_stem_x,
                 min(prev_stem_y_start, stem_y_start))

    # --- Beam or beam stub ---
    if chunk_dur in (TICKS_EIGHTH, TICKS_DOTTED_EIGHTH):
        _draw_beam(draw_obj, utils, note, chunk_acc, chunk_dur,
                   chunk_stem_x, stem_y_start,
                   next_real_note, prev_real_note)

    return last_pm_x, last_pm_y


def _draw_fret_numbers(draw_obj, utils: LayoutUtils,
                       fret_font, annotation_font,
                       note, chunk_acc, chunk_x, chunk_next_x,
                       strings_y,
                       last_style, last_pm_x,
                       segment_notes, idx):
    """Draw fret number labels (or 'X') for each string in the chord,
    plus slide lines and palm mute annotation.
    Returns updated (last_pm_x, last_pm_y)."""
    cfg     = utils.cfg
    strings = [note.chord.string1, note.chord.string2, note.chord.string3,
               note.chord.string4, note.chord.string5, note.chord.string6]
    last_pm_y = None

    for i, fret in enumerate(strings):
        if fret is not None and fret != -1:
            y     = strings_y + i * utils.line_sp_px
            label = "X" if note.style == StrumStyle.MUTED else str(fret)

            text_w, text_h = draw_obj.textbbox((0, 0), label, font=fret_font)[2:]
            draw_obj.rectangle(
                [chunk_x - 2,         y - text_h // 2,
                 chunk_x + text_w + 2, y + text_h // 2],
                fill="white",
            )
            draw_obj.text(
                (chunk_x, y - text_h // 2),
                label, fill="black", font=fret_font,
            )

            if note.style == StrumStyle.SLIDE:
                _draw_slide(draw_obj, utils, chunk_x, chunk_next_x,
                            strings_y, i, text_w)

    if note.style == StrumStyle.PALM_MUTED:
        last_pm_x, last_pm_y = _draw_palm_mute(
            draw_obj, utils, annotation_font,
            note, chunk_acc, chunk_x, strings_y,
            last_style, last_pm_x,
            segment_notes, idx,
        )

    return last_pm_x, last_pm_y


def _draw_slide(draw_obj, utils: LayoutUtils, chunk_x, chunk_next_x,
                strings_y, string_index, text_w):
    """Draw the horizontal slide line and arc for one string."""
    cfg   = utils.cfg
    nudge = utils.px(cfg.arcs.slide_nudge_pt)
    y     = strings_y + string_index * utils.line_sp_px
    draw_obj.line(
        [(chunk_x + text_w + nudge, y),
         (chunk_next_x - nudge, y)],
        fill="black", width=utils.lw(cfg.line_width.thin_pt),
    )
    draw_arc(draw_obj, utils,
             chunk_x + nudge, chunk_next_x - nudge,
             strings_y + string_index * utils.line_sp_px)


def _draw_palm_mute(draw_obj, utils: LayoutUtils, annotation_font,
                    note, chunk_acc, chunk_x, strings_y,
                    last_style, last_pm_x,
                    segment_notes, idx):
    """Draw P.M. label, dashed continuation line, and closing tick.
    Returns updated (last_pm_x, last_pm_y)."""
    cfg  = utils.cfg
    pm_y = strings_y + utils.px(cfg.palm_mute.y_offset_pt)

    is_first_pm_on_line = (last_style != StrumStyle.PALM_MUTED or last_pm_x is None)
    next_real_note = next(
        (segment_notes[i] for i in range(idx + 1, len(segment_notes))
         if segment_notes[i].duration is not None), None,
    )
    is_last_pm = (next_real_note is None
                  or next_real_note.style != StrumStyle.PALM_MUTED)

    if is_first_pm_on_line:
        draw_obj.text(
            (chunk_x, pm_y - utils.px(cfg.palm_mute.label_y_pt)),
            "P.M.", fill="black", font=annotation_font,
        )
        last_pm_x = chunk_x + utils.px(cfg.palm_mute.label_w_pt)
    else:
        _draw_dashed_segment(draw_obj, utils, last_pm_x, chunk_x, pm_y)
        last_pm_x = chunk_x

    if is_last_pm and not is_first_pm_on_line:
        tick_h = utils.px(cfg.palm_mute.tick_h_pt)
        draw_obj.line(
            [(chunk_x, pm_y - tick_h // 2),
             (chunk_x, pm_y + tick_h // 2)],
            fill="black", width=utils.lw(cfg.line_width.thin_pt),
        )

    return last_pm_x, pm_y


def _draw_stem(draw_obj, utils: LayoutUtils, stem_x, stem_y_start, duration,
               is_rest: bool = False):
    """Draw the stem below the note at (stem_x, stem_y_start)."""
    cfg = utils.cfg
    if is_rest:
        full_h = utils.px(cfg.stems.h_pt)
        rest_h = utils.px(cfg.notes.rest_stem_pt)
        draw_obj.line(
            [(stem_x, stem_y_start + full_h - rest_h),
             (stem_x, stem_y_start + full_h)],
            fill="black", width=utils.lw(cfg.line_width.normal_pt),
        )
        return
    if duration >= TICKS_FULL_NOTE:
        draw_obj.line(
            [(stem_x, stem_y_start),
             (stem_x, stem_y_start + utils.px(cfg.stems.h_pt * 3.0))],
            fill="black", width=utils.lw(cfg.line_width.normal_pt),
        )
    elif duration >= TICKS_HALF_NOTE:
        top_h = utils.px(cfg.stems.h_pt * 0.5)
        gap   = utils.px(cfg.stems.h_pt * 1.0)
        bot_h = utils.px(cfg.stems.h_pt * 1.5)
        draw_obj.line(
            [(stem_x, stem_y_start),
             (stem_x, stem_y_start + top_h)],
            fill="black", width=utils.lw(cfg.line_width.normal_pt),
        )
        draw_obj.line(
            [(stem_x, stem_y_start + top_h + gap),
             (stem_x, stem_y_start + top_h + gap + bot_h)],
            fill="black", width=utils.lw(cfg.line_width.normal_pt),
        )
    else:
        draw_obj.line(
            [(stem_x, stem_y_start),
             (stem_x, stem_y_start + utils.px(cfg.stems.h_pt))],
            fill="black", width=utils.lw(cfg.line_width.normal_pt),
        )


def _draw_dot(draw_obj, utils: LayoutUtils, stem_x, stem_y_start):
    """Draw the dot for a dotted-rhythm note."""
    cfg       = utils.cfg
    dot_offset = utils.px(cfg.beams.dot_offset_pt)
    dot_r      = utils.px(cfg.beams.dot_r_pt)
    dot_x      = stem_x + dot_offset
    dot_y      = stem_y_start + dot_offset
    draw_obj.ellipse(
        [dot_x - dot_r, dot_y - dot_r,
         dot_x + dot_r, dot_y + dot_r],
        fill="black",
    )


def _draw_beam(draw_obj, utils: LayoutUtils,
               note, chunk_acc, chunk_dur,
               chunk_stem_x, stem_y_start,
               next_real_note, prev_real_note):
    """Draw a beam connecting to the next note, or a stub flag if unbeamed."""
    cfg           = utils.cfg
    chunk_bottom_y = stem_y_start + utils.px(cfg.stems.h_pt)

    is_at_measure_end  = utils.is_new_measure(chunk_acc + chunk_dur)
    can_beam_fwd = (not is_at_measure_end
                    and next_real_note is not None
                    and next_real_note.duration == note.duration
                    and note.chord is not None
                    and next_real_note.chord is not None)

    is_at_measure_start = utils.is_new_measure(chunk_acc)
    is_beamed_back = (not is_at_measure_start
                      and prev_real_note is not None
                      and prev_real_note.duration == note.duration
                      and note.chord is not None
                      and prev_real_note.chord is not None)

    if can_beam_fwd:
        draw_obj.line(
            [(chunk_stem_x, chunk_bottom_y),
             (chunk_stem_x + utils.beat_w_px * chunk_dur, chunk_bottom_y)],
            fill="black", width=utils.lw(cfg.line_width.thick_pt),
        )
    elif not is_beamed_back:
        draw_obj.line(
            [(chunk_stem_x, chunk_bottom_y),
             (chunk_stem_x + utils.px(cfg.beams.stub_pt), chunk_bottom_y)],
            fill="black", width=utils.lw(cfg.line_width.normal_pt),
        )


# ---------------------------------------------------------------------------
# Shared primitives (used by both row-level and note-level drawing)
# ---------------------------------------------------------------------------

def draw_arc(draw_obj, utils: LayoutUtils, x_start, x_end, y_top):
    cfg     = utils.cfg
    top_off = utils.px(cfg.arcs.top_offset_pt)
    bot_off = utils.px(cfg.arcs.bot_offset_pt)
    arc_box = [x_start, y_top - top_off, x_end, y_top - bot_off]
    draw_obj.arc(arc_box, start=180, end=0, fill="black",
                 width=utils.lw(cfg.line_width.thin_pt))


def _draw_dashed_segment(draw_obj, utils: LayoutUtils, x_start, x_end, y):
    dash_gap = utils.px(utils.cfg.palm_mute.dash_gap_pt)
    curr = x_start
    while curr < x_end:
        draw_obj.line(
            [(curr, y), (min(curr + dash_gap, x_end), y)],
            fill="black", width=utils.lw(utils.cfg.line_width.thin_pt),
        )
        curr += dash_gap * 2


# ---------------------------------------------------------------------------
# Segment rendering — drives the row/note layers
# ---------------------------------------------------------------------------

def render_tab(segments: list[Segment], instrument_name: str,
               output_base_path: str = "guitar_tab",
               cfg: LayoutConfig = None) -> list[tuple[str, object]]:
    if cfg is None:
        cfg = LayoutConfig()

    utils = LayoutUtils(cfg)
    (title_font, fret_font, small_font,
     string_name_font, annotation_font,
     _lyrics_font, lyrics_tab_font) = utils.load_fonts()

    cfg = utils.cfg

    results = []
    global_measure_counter = 1

    for seg_idx, segment in enumerate(segments):
        segment_notes = segment.GetNotesFromSegment(instrument_name)
        total_units   = sum((n.duration if n.duration else 0) for n in segment_notes)
        num_measures  = math.ceil(total_units / UNITS_PER_MEASURE)
        num_systems   = math.ceil(num_measures / MEASURES_PER_LINE)

        img_height_px = (utils.px(cfg.page.title_padding_pt)
                         + utils.title_h_px
                         + num_systems * utils.system_h_px
                         + utils.below_str_px)

        img  = Image.new('RGB', (int(utils.img_width_px), int(img_height_px)), color='white')
        draw = ImageDraw.Draw(img)

        # --- Segment title ---
        top_padding_px = utils.px(cfg.page.title_padding_pt)
        draw.text((utils.margin_left_px, top_padding_px), segment.title,
                  fill="black", font=title_font)
        base_y = top_padding_px + utils.title_h_px  # top of the first system row

        acc_dur_segment = 0
        last_style      = None
        last_pm_x       = None
        last_pm_y       = None
        final_x         = utils.margin_left_px
        final_y         = base_y

        for idx, note in enumerate(segment_notes):
            strings_y   = utils.tick_to_strings_y(acc_dur_segment, base_y)
            is_new_line = utils.is_new_system(acc_dur_segment)
            current_x   = utils.tick_to_x(acc_dur_segment)
            note_dur    = note.duration or 0
            next_x      = current_x + note_dur * utils.beat_w_px

            if note.duration is not None:
                final_y = strings_y
                final_x = next_x

                # --- Start of a new system row ---
                if is_new_line:
                    draw_row(draw, utils, fret_font, small_font,
                             string_name_font, strings_y, global_measure_counter)
                    last_pm_x = None
                    last_pm_y = None

                # --- Mid-row barline (not the first measure of the row) ---
                if (utils.tick_to_unit_in_measure(acc_dur_segment) == 0
                        and utils.tick_to_measure_in_system(acc_dur_segment) > 0):
                    draw_barline(draw, utils, small_font, strings_y,
                                 utils.barline_x(acc_dur_segment), global_measure_counter)

            if note.duration is not None:
                remaining_dur     = note.duration
                chunk_acc         = acc_dur_segment
                prev_stem_x       = None
                prev_stem_y_start = None

                # A note may span a barline and must be split into chunks.
                while remaining_dur > 0:
                    ticks_left = UNITS_PER_MEASURE - utils.tick_to_unit_in_measure(chunk_acc)
                    chunk_dur  = min(remaining_dur, ticks_left)

                    chunk_strings_y    = utils.tick_to_strings_y(chunk_acc, base_y)
                    chunk_stem_y_start = utils.tick_to_stem_y(chunk_acc, base_y)
                    chunk_is_new_line  = utils.is_new_system(chunk_acc)
                    chunk_x            = utils.tick_to_x(chunk_acc)
                    chunk_stem_x       = chunk_x + utils.px(cfg.stems.x_offset_pt)
                    chunk_next_x       = chunk_x + chunk_dur * utils.beat_w_px

                    # --- New system row opened by a continuation chunk ---
                    if chunk_is_new_line and chunk_acc != acc_dur_segment:
                        draw_row(draw, utils, fret_font, small_font,
                                 string_name_font, chunk_strings_y,
                                 global_measure_counter)
                        last_pm_x = None
                        last_pm_y = None

                    # --- Mid-row barline opened by a continuation chunk ---
                    if utils.is_new_measure(chunk_acc) and chunk_acc != acc_dur_segment:
                        draw_barline(draw, utils, small_font, chunk_strings_y,
                                     utils.barline_x(chunk_acc), global_measure_counter)

                    # --- Look up neighbours for beam decisions ---
                    next_real_idx  = next(
                        (i for i in range(idx + 1, len(segment_notes))
                         if segment_notes[i].duration is not None), None)
                    next_real_note = (segment_notes[next_real_idx]
                                      if next_real_idx is not None else None)
                    prev_real_idx  = next(
                        (i for i in range(idx - 1, -1, -1)
                         if segment_notes[i].duration is not None), None)
                    prev_real_note = (segment_notes[prev_real_idx]
                                      if prev_real_idx is not None else None)

                    # --- Draw the note ---
                    last_pm_x, last_pm_y = draw_note(
                        draw, utils,
                        fret_font, annotation_font,
                        note, chunk_acc, chunk_dur,
                        chunk_x, chunk_next_x, chunk_stem_x,
                        chunk_strings_y, chunk_stem_y_start,
                        is_first_chunk=(chunk_acc == acc_dur_segment),
                        prev_stem_x=prev_stem_x,
                        prev_stem_y_start=prev_stem_y_start,
                        next_real_note=next_real_note,
                        prev_real_note=prev_real_note,
                        last_style=last_style,
                        last_pm_x=last_pm_x,
                        segment_notes=segment_notes,
                        idx=idx,
                    )

                    prev_stem_x       = chunk_stem_x
                    prev_stem_y_start = chunk_stem_y_start
                    chunk_acc     += chunk_dur
                    remaining_dur -= chunk_dur

                    if utils.is_new_measure(chunk_acc):
                        global_measure_counter += 1

                    if utils.is_new_system(chunk_acc):
                        eol_strings_y = utils.tick_to_strings_y(chunk_acc - 1, base_y)
                        draw_row_end_barline(draw, utils, eol_strings_y)

            if note.style is not None:
                last_style = note.style
            acc_dur_segment += note.duration if note.duration else 0

        # --- Final barline after the last note ---
        if not utils.is_new_system(acc_dur_segment):
            draw_final_barline(draw, utils, final_x, final_y)

        # --- Inline lyrics ---
        if segment.lyrics is not None:
            _draw_lyrics(draw, utils, lyrics_tab_font, segment, base_y)

        safe_title = "".join(
            c for c in segment.title if c.isalnum() or c in (' ', '_')
        ).strip().replace(' ', '_')
        file_path = f"{output_base_path}_{seg_idx + 1}_{safe_title}.png"
        results.append((file_path, img))

    return results


def _draw_lyrics(draw_obj, utils: LayoutUtils, lyrics_tab_font,
                 segment, base_y):
    """Draw syllable-aligned inline lyrics below the string lines."""
    from tabfromtext.util.SyllableUtils import split_syllables

    cfg             = utils.cfg
    lyrics_y_off_px = utils.px(cfg.lyrics.y_offset_pt)
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
        syl_strings_y = utils.tick_to_strings_y(abs_tick, base_y)
        syl_y         = syl_strings_y + 5 * utils.line_sp_px + lyrics_y_off_px
        syl_x_left    = utils.tick_to_x(abs_tick)
        text_w        = draw_obj.textbbox((0, 0), syl_text, font=lyrics_tab_font)[2]
        draw_obj.text(
            (syl_x_left - text_w // 2, syl_y),
            syl_text, fill="black", font=lyrics_tab_font,
        )


# ---------------------------------------------------------------------------
# Title page
# ---------------------------------------------------------------------------

def render_title_page(song: Song, cfg: LayoutConfig = None,
                      num_columns: int = 2) -> Image.Image | None:
    sections = [(seg.title, seg.lyrics.text if seg.lyrics is not None else None)
                for seg in song.segments]
    if not sections:
        return None

    if cfg is None:
        cfg = LayoutConfig()

    utils = LayoutUtils(cfg)
    title_font, _fret, _small, _str_name, _ann, lyrics_font, _lyrics_tab = utils.load_fonts()

    from reportlab.lib.pagesizes import A4
    A4_WIDTH_PT, A4_HEIGHT_PT = A4

    img_w_px  = utils.img_width_px
    page_h_pt = A4_HEIGHT_PT - cfg.page.top_margin_pt - cfg.page.bottom_margin_pt
    img_h_px  = utils.px(page_h_pt)

    img  = Image.new('RGB', (img_w_px, img_h_px), color='white')
    draw = ImageDraw.Draw(img)

    margin_px     = utils.margin_left_px
    title_line_h  = int(utils.px(cfg.fonts.title_pt)  * 1.4)
    lyrics_line_h = int(utils.px(cfg.fonts.lyrics_pt) * 1.4)
    section_gap   = lyrics_line_h
    top_pad_px    = utils.px(cfg.page.top_margin_pt * 0.5)

    # --- Song title (centered) ---
    title_w = draw.textbbox((0, 0), song.title, font=title_font)[2]
    draw.text(((img_w_px - title_w) // 2, top_pad_px), song.title,
              fill="black", font=title_font)
    columns_top_y = top_pad_px + title_line_h * 2

    # --- Column geometry ---
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