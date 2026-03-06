import math
from PIL import Image, ImageDraw, ImageFont
from object.StrumStyle import StrumStyle
from object.Segment import Segment
from object.TimeUtils import TIME_RESOLUTION
from object.Song import Song

# --- Konstandid ---
MEASURES_PER_LINE = 4
UNITS_PER_MEASURE = 8 * TIME_RESOLUTION

FRET_FONT_SIZE = 26
TITLE_FONT_SIZE = 28
MEASURE_NUM_FONT_SIZE = 12

LINE_SPACING = 30
BEAT_WIDTH = 55 / TIME_RESOLUTION
BAR_PADDING = 25
MARGIN_LEFT = 80
MARGIN_RIGHT = 80

TITLE_HEIGHT = 80
SYSTEM_HEIGHT = (6 * LINE_SPACING) + 160

PM_Y_OFFSET = -25
DASH_GAP = 5
TICK_H = 8
MEASURE_NUM_Y_OFFSET = -50

# Tick thresholds
TICKS_SIXTEENTH        = TIME_RESOLUTION // 2
TICKS_DOTTED_EIGHTH    = TICKS_SIXTEENTH * 3
TICKS_EIGHTH           = 1 * TIME_RESOLUTION
TICKS_HALF_NOTE        = 4 * TIME_RESOLUTION
TICKS_FULL_NOTE        = 8 * TIME_RESOLUTION

# Stem height constants (base unit = 30px = 1 stem height)
STEM_H        = 30
HALF_TOP_H    = int(STEM_H * 0.5)
HALF_GAP      = int(STEM_H * 1.0)
HALF_BOTTOM_H = int(STEM_H * 1.5)
FULL_H        = int(STEM_H * 3.0)

MEASURE_WIDTH = (UNITS_PER_MEASURE * BEAT_WIDTH) + BAR_PADDING
LINE_CONTENT_WIDTH = MEASURES_PER_LINE * MEASURE_WIDTH

try:
    title_font = ImageFont.truetype("arialbd.ttf", TITLE_FONT_SIZE)
    fret_font = ImageFont.truetype("arial.ttf", FRET_FONT_SIZE)
    small_font = ImageFont.truetype("arial.ttf", MEASURE_NUM_FONT_SIZE)
except:
    title_font = fret_font = small_font = ImageFont.load_default()

def is_dotted(duration):
    if duration <= 0:
        return False
    doubled = duration * 2
    if doubled % 3 != 0:
        return False
    base = doubled // 3
    return base > 0 and (base & (base - 1)) == 0

def draw_arc(draw_obj, x_start, x_end, y_top):
        arc_box = [x_start, y_top - 20, x_end, y_top - 5]
        draw_obj.arc(arc_box, start=180, end=0, fill="black", width=1)

def draw_stem(draw_obj, stem_x, stem_y_start, duration):
    if duration >= TICKS_FULL_NOTE:
        draw_obj.line([(stem_x, stem_y_start), (stem_x, stem_y_start + FULL_H)], fill="black", width=2)
    elif duration >= TICKS_HALF_NOTE:
        draw_obj.line([(stem_x, stem_y_start), (stem_x, stem_y_start + HALF_TOP_H)], fill="black", width=2)
        draw_obj.line([(stem_x, stem_y_start + HALF_TOP_H + HALF_GAP), (stem_x, stem_y_start + HALF_TOP_H + HALF_GAP + HALF_BOTTOM_H)], fill="black", width=2)
    else:
        draw_obj.line([(stem_x, stem_y_start), (stem_x, stem_y_start + STEM_H)], fill="black", width=2)

def draw_staff_elements(draw_obj, y_top, start_measure_num):
    string_names = ['e', 'B', 'G', 'D', 'A', 'E']
    for i, name in enumerate(string_names):
        y = y_top + (i * LINE_SPACING)
        draw_obj.text((20, y - (MEASURE_NUM_FONT_SIZE // 2)), name, fill="black")
        draw_obj.line([(MARGIN_LEFT, y), (MARGIN_LEFT + LINE_CONTENT_WIDTH, y)], fill=(200, 200, 200))
    draw_obj.line([(MARGIN_LEFT, y_top), (MARGIN_LEFT, y_top + 5 * LINE_SPACING)], fill="black", width=2)
    draw_obj.text((MARGIN_LEFT, y_top + MEASURE_NUM_Y_OFFSET), str(start_measure_num), fill="gray", font=small_font)

def draw_dashed_segment(draw_obj, x_start, x_end, y):
    curr = x_start
    while curr < x_end:
        draw_obj.line([(curr, y), (min(curr + DASH_GAP, x_end), y)], fill="black", width=1)
        curr += DASH_GAP * 2

def render_tab(segments: list[Segment], output_base_path="guitar_tab"):
    global_measure_counter = 1

    for seg_idx, segment in enumerate(segments):
        segment_notes = segment.GetNotesFromSegment()
        total_units = sum((n.duration if n.duration else 0) for n in segment_notes)
        num_measures = math.ceil(total_units / UNITS_PER_MEASURE)
        num_systems = math.ceil(num_measures / MEASURES_PER_LINE)

        img_width = LINE_CONTENT_WIDTH + MARGIN_LEFT + MARGIN_RIGHT
        img_height = (num_systems * SYSTEM_HEIGHT) + TITLE_HEIGHT + 60

        img = Image.new('RGB', (int(img_width), int(img_height)), color='white')
        draw = ImageDraw.Draw(img)

        current_y_cursor = 40
        draw.text((MARGIN_LEFT, current_y_cursor), segment.title, fill="black", font=title_font)
        current_y_cursor += TITLE_HEIGHT

        acc_dur_segment = 0
        last_style = None
        last_pm_x = None
        last_pm_y = None
        final_x = MARGIN_LEFT
        final_y = current_y_cursor

        for idx, note in enumerate(segment_notes):
            total_beats_in_segment = acc_dur_segment // UNITS_PER_MEASURE
            system_in_segment = int(acc_dur_segment // (UNITS_PER_MEASURE * MEASURES_PER_LINE))
            measure_in_system = int(total_beats_in_segment % MEASURES_PER_LINE)
            unit_in_measure = acc_dur_segment % UNITS_PER_MEASURE

            row_y_top = current_y_cursor + (system_in_segment * SYSTEM_HEIGHT)

            is_new_line = (acc_dur_segment % (UNITS_PER_MEASURE * MEASURES_PER_LINE) == 0)

            current_x = MARGIN_LEFT + (measure_in_system * MEASURE_WIDTH) + (unit_in_measure * BEAT_WIDTH) + BAR_PADDING
            note_dur = (note.duration or 0)
            next_x = current_x + (note_dur * BEAT_WIDTH)

            if note.duration is not None:
                final_y = row_y_top
                final_x = next_x
                if is_new_line:
                    draw_staff_elements(draw, row_y_top, global_measure_counter)
                    last_pm_x = None
                    last_pm_y = None
                if unit_in_measure == 0 and measure_in_system > 0:
                    bar_x = MARGIN_LEFT + (measure_in_system * MEASURE_WIDTH)
                    draw.line([(bar_x, row_y_top), (bar_x, row_y_top + 5 * LINE_SPACING)], fill="black", width=2)
                    draw.text((bar_x, row_y_top + MEASURE_NUM_Y_OFFSET), str(global_measure_counter), fill="gray", font=small_font)

            if note.duration is not None:

                # Split note into measure-sized chunks if it spans multiple measures
                remaining_dur = note.duration
                chunk_acc = acc_dur_segment
                prev_stem_x = None
                prev_stem_y_start = None

                while remaining_dur > 0:
                    ticks_left_in_measure = UNITS_PER_MEASURE - (chunk_acc % UNITS_PER_MEASURE)
                    chunk_dur = min(remaining_dur, ticks_left_in_measure)

                    # Calculate position of this chunk
                    chunk_total_beats = chunk_acc // UNITS_PER_MEASURE
                    chunk_system = int(chunk_acc // (UNITS_PER_MEASURE * MEASURES_PER_LINE))
                    chunk_measure_in_system = int(chunk_total_beats % MEASURES_PER_LINE)
                    chunk_unit_in_measure = chunk_acc % UNITS_PER_MEASURE

                    chunk_row_y_top = current_y_cursor + (chunk_system * SYSTEM_HEIGHT)
                    chunk_stem_y_start = chunk_row_y_top + (6 * LINE_SPACING)

                    # Draw new staff line if this chunk starts a new line
                    chunk_is_new_line = (chunk_acc % (UNITS_PER_MEASURE * MEASURES_PER_LINE) == 0)
                    if chunk_is_new_line and chunk_acc != acc_dur_segment:
                        draw_staff_elements(draw, chunk_row_y_top, global_measure_counter)
                        last_pm_x = None
                        last_pm_y = None

                    chunk_x = MARGIN_LEFT + (chunk_measure_in_system * MEASURE_WIDTH) + (chunk_unit_in_measure * BEAT_WIDTH) + BAR_PADDING
                    chunk_stem_x = chunk_x + 4
                    chunk_next_x = chunk_x + (chunk_dur * BEAT_WIDTH)

                    # Draw barline if this chunk starts a new measure (but not the very first chunk)
                    if chunk_unit_in_measure == 0 and chunk_acc != acc_dur_segment:
                        bar_x = MARGIN_LEFT + (chunk_measure_in_system * MEASURE_WIDTH)
                        draw.line([(bar_x, chunk_row_y_top), (bar_x, chunk_row_y_top + 5 * LINE_SPACING)], fill="black", width=2)
                        draw.text((bar_x, chunk_row_y_top + MEASURE_NUM_Y_OFFSET), str(global_measure_counter), fill="gray", font=small_font)

                    # Draw chord numbers for every chunk
                    if note.chord and note.style != StrumStyle.NO_HIT:
                        strings = [note.chord.string1, note.chord.string2, note.chord.string3,
                                   note.chord.string4, note.chord.string5, note.chord.string6]
                        for i, fret in enumerate(strings):
                            if fret is not None and fret != -1:
                                y = chunk_row_y_top + (i * LINE_SPACING)
                                label = "X" if note.style == StrumStyle.MUTED else str(fret)

                                text_w, text_h = draw.textbbox((0, 0), label, font=fret_font)[2:]
                                draw.rectangle([chunk_x - 2, y - (text_h//2), chunk_x + text_w + 2, y + (text_h//2)], fill="white")
                                draw.text((chunk_x, y - (text_h // 2)), label, fill="black", font=fret_font)

                                if note.style == StrumStyle.SLIDE:
                                    draw.line([(chunk_x + text_w + 5, y), (chunk_next_x - 5, y)], fill="black", width=1)
                                    draw_arc(draw, chunk_x + 5, chunk_next_x - 5, chunk_row_y_top + (i * LINE_SPACING))

                        if note.style == StrumStyle.PALM_MUTED:
                            pm_y = chunk_row_y_top + PM_Y_OFFSET
                            is_first_pm_on_line = (last_style != StrumStyle.PALM_MUTED or chunk_is_new_line)
                            next_real_note = next((segment_notes[i] for i in range(idx+1, len(segment_notes)) if segment_notes[i].duration is not None), None)
                            is_last_pm = next_real_note is None or next_real_note.style != StrumStyle.PALM_MUTED
                            if is_first_pm_on_line:
                                # Draw P.M. label only, no opening tick
                                draw.text((chunk_x, pm_y - 12), "P.M.", fill="black", font=small_font)
                                last_pm_x = chunk_x + 35  # start of dashed line is after the label
                            else:
                                # Draw dashed line backwards from current note's x to previous note's x
                                draw_dashed_segment(draw, last_pm_x, chunk_x, pm_y)
                                last_pm_x = chunk_x
                            # Draw closing tick on the last PM note (but not if it's also the first, as that overlaps the label)
                            if is_last_pm and not is_first_pm_on_line:
                                draw.line([(chunk_x, pm_y - TICK_H/2), (chunk_x, pm_y + TICK_H/2)], fill="black", width=1)
                            last_pm_y = pm_y

                    # Draw stem for this chunk
                    draw_stem(draw, chunk_stem_x, chunk_stem_y_start, chunk_dur)

                    # Draw dot on first chunk only
                    if chunk_acc == acc_dur_segment and is_dotted(note.duration):
                        dot_x = chunk_stem_x + 8
                        dot_y = chunk_stem_y_start + 8
                        draw.ellipse([dot_x - 2, dot_y - 2, dot_x + 2, dot_y + 2], fill="black")

                    # Draw connecting arc from previous chunk's stem top to this chunk's stem top
                    if prev_stem_x is not None:
                        draw_arc(draw, prev_stem_x, chunk_stem_x, min(prev_stem_y_start, chunk_stem_y_start))

                    # Draw horizontal beams for eighth/dotted-eighth chunks
                    if chunk_dur == TICKS_EIGHTH or chunk_dur == TICKS_DOTTED_EIGHTH:
                        chunk_bottom_y = chunk_stem_y_start + STEM_H
                        next_real_idx = next((i for i in range(idx+1, len(segment_notes)) if segment_notes[i].duration is not None), None)
                        next_real_note = segment_notes[next_real_idx] if next_real_idx is not None else None

                        prev_real_idx = next((i for i in range(idx-1, -1, -1) if segment_notes[i].duration is not None), None)
                        prev_real_note = segment_notes[prev_real_idx] if prev_real_idx is not None else None

                        is_at_measure_end = (chunk_acc + chunk_dur) % UNITS_PER_MEASURE == 0
                        can_beam_fwd = (not is_at_measure_end) and (next_real_note is not None) and (next_real_note.duration == note.duration) and (note.chord is not None) and (next_real_note.chord is not None)

                        is_at_measure_start = (chunk_acc % UNITS_PER_MEASURE == 0)
                        is_beamed_back = (not is_at_measure_start) and (prev_real_note is not None) and (prev_real_note.duration == note.duration) and (note.chord is not None) and (prev_real_note.chord is not None)

                        if can_beam_fwd:
                            draw.line([(chunk_stem_x, chunk_bottom_y), (chunk_stem_x + BEAT_WIDTH * chunk_dur, chunk_bottom_y)], fill="black", width=4)
                        elif not is_beamed_back:
                            draw.line([(chunk_stem_x, chunk_bottom_y), (chunk_stem_x + 12, chunk_bottom_y)], fill="black", width=2)

                    prev_stem_x = chunk_stem_x
                    prev_stem_y_start = chunk_stem_y_start
                    chunk_acc += chunk_dur
                    remaining_dur -= chunk_dur

                    # Increment measure counter when a measure boundary is crossed
                    if chunk_acc % UNITS_PER_MEASURE == 0:
                        global_measure_counter += 1

                    # Draw end-of-line barline if needed
                    if chunk_acc % (UNITS_PER_MEASURE * MEASURES_PER_LINE) == 0:
                        eol_system = int((chunk_acc - 1) // (UNITS_PER_MEASURE * MEASURES_PER_LINE))
                        eol_row_y_top = current_y_cursor + (eol_system * SYSTEM_HEIGHT)
                        draw.line([(MARGIN_LEFT + LINE_CONTENT_WIDTH, eol_row_y_top),
                                   (MARGIN_LEFT + LINE_CONTENT_WIDTH, eol_row_y_top + 5 * LINE_SPACING)], fill="black", width=2)

            if note.style is not None:
                last_style = note.style
            acc_dur_segment += (note.duration if note.duration else 0)

        if acc_dur_segment % (UNITS_PER_MEASURE * MEASURES_PER_LINE) != 0:
            draw.line([(final_x, final_y), (final_x, final_y + 5 * LINE_SPACING)], fill="black", width=2)

        safe_title = "".join([c for c in segment.title if c.isalnum() or c in (' ', '_')]).strip().replace(' ', '_')
        file_path = f"{output_base_path}_{seg_idx + 1}_{safe_title}.png"
        img.save(file_path)
        print(f"Salvestatud: {file_path}")

def render_song(song: Song):
    safe_song_title = song.title.lower().replace(' ', '_')
    for instrument in song.instruments:
        safe_instrument_name = instrument.name.lower().replace(' ', '_')
        output_base_path = f"tabs/{safe_song_title}/{safe_instrument_name}/tab"
        render_tab(instrument.segments, output_base_path)