import math
from PIL import Image, ImageDraw, ImageFont
from object.StrumStyle import StrumStyle
from object.Segment import Segment
from object.Note import Note

def render_tab(segments: list[Segment], output_path="guitar_tab.png"):
    # --- Constants ---
    MEASURES_PER_LINE = 4
    UNITS_PER_MEASURE = 8
    
    # Font and Sizing Constants
    FRET_FONT_SIZE = 26        # Base height for fret numbers (~1.5x of previous)
    TITLE_FONT_SIZE = 28
    MEASURE_NUM_FONT_SIZE = 12
    
    LINE_SPACING = 30          # Increased to accommodate larger numbers
    BEAT_WIDTH = 55            # Slightly wider to prevent numbers overlapping horizontally
    BAR_PADDING = 25  
    MARGIN_LEFT = 80
    MARGIN_RIGHT = 80 
    
    TITLE_HEIGHT = 80   
    SYSTEM_HEIGHT = (6 * LINE_SPACING) + 160 
    
    PM_Y_OFFSET = -25
    DASH_GAP = 5
    TICK_H = 8
    MEASURE_NUM_Y_OFFSET = -50

    MEASURE_WIDTH = (UNITS_PER_MEASURE * BEAT_WIDTH) + BAR_PADDING
    LINE_CONTENT_WIDTH = MEASURES_PER_LINE * MEASURE_WIDTH

    # 1. Calculate Total Systems for Image Height
    total_systems = 0
    for segment in segments:
        notes = Note.GetNotesFromSegment(segment)
        total_units = sum((n.duration if n.duration else 0.5) for n in notes)
        num_measures = math.ceil(total_units / UNITS_PER_MEASURE)
        num_systems = math.ceil(num_measures / MEASURES_PER_LINE)
        total_systems += num_systems

    img_width = LINE_CONTENT_WIDTH + MARGIN_LEFT + MARGIN_RIGHT
    img_height = (total_systems * SYSTEM_HEIGHT) + (len(segments) * TITLE_HEIGHT) + 100
    
    img = Image.new('RGB', (int(img_width), int(img_height)), color='white')
    draw = ImageDraw.Draw(img)
    
    try:
        title_font = ImageFont.truetype("arialbd.ttf", TITLE_FONT_SIZE)
        fret_font = ImageFont.truetype("arial.ttf", FRET_FONT_SIZE)
        small_font = ImageFont.truetype("arial.ttf", MEASURE_NUM_FONT_SIZE)
    except:
        title_font = fret_font = small_font = ImageFont.load_default()

    # --- Helpers ---
    def draw_staff_elements(y_top, start_measure_num):
        string_names = ['e', 'B', 'G', 'D', 'A', 'E']
        for i, name in enumerate(string_names):
            y = y_top + (i * LINE_SPACING)
            draw.text((20, y - (MEASURE_NUM_FONT_SIZE // 2)), name, fill="black")
            draw.line([(MARGIN_LEFT, y), (MARGIN_LEFT + LINE_CONTENT_WIDTH, y)], fill=(200, 200, 200))
        draw.line([(MARGIN_LEFT, y_top), (MARGIN_LEFT, y_top + 5 * LINE_SPACING)], fill="black", width=2)
        draw.text((MARGIN_LEFT, y_top + MEASURE_NUM_Y_OFFSET), str(start_measure_num), fill="gray", font=small_font)

    def draw_dashed_segment(x_start, x_end, y):
        curr = x_start
        while curr < x_end:
            draw.line([(curr, y), (min(curr + DASH_GAP, x_end), y)], fill="black", width=1)
            curr += DASH_GAP * 2

    # --- Rendering State ---
    current_y_cursor = 40 
    global_measure_counter = 1

    for segment in segments:
        draw.text((MARGIN_LEFT, current_y_cursor), segment.title, fill="black", font=title_font)
        current_y_cursor += TITLE_HEIGHT

        segment_notes = Note.GetNotesFromSegment(segment)
        acc_dur_segment = 0
        last_style = None
        final_x = MARGIN_LEFT
        final_y = current_y_cursor

        for idx, note in enumerate(segment_notes):
            total_beats_in_segment = acc_dur_segment // UNITS_PER_MEASURE
            system_in_segment = int(acc_dur_segment // (UNITS_PER_MEASURE * MEASURES_PER_LINE))
            measure_in_system = int(total_beats_in_segment % MEASURES_PER_LINE)
            unit_in_measure = acc_dur_segment % UNITS_PER_MEASURE
            
            row_y_top = current_y_cursor + (system_in_segment * SYSTEM_HEIGHT)
            final_y = row_y_top
            
            is_new_line = (acc_dur_segment % (UNITS_PER_MEASURE * MEASURES_PER_LINE) == 0)
            if is_new_line:
                draw_staff_elements(row_y_top, global_measure_counter)

            current_x = MARGIN_LEFT + (measure_in_system * MEASURE_WIDTH) + (unit_in_measure * BEAT_WIDTH) + BAR_PADDING
            note_dur = (note.duration or 0.5)
            next_x = current_x + (note_dur * BEAT_WIDTH)
            final_x = next_x

            # Draw Measure Bars
            if unit_in_measure == 0 and measure_in_system > 0:
                bar_x = MARGIN_LEFT + (measure_in_system * MEASURE_WIDTH)
                draw.line([(bar_x, row_y_top), (bar_x, row_y_top + 5 * LINE_SPACING)], fill="black", width=2)
                draw.text((bar_x, row_y_top + MEASURE_NUM_Y_OFFSET), str(global_measure_counter), fill="gray", font=small_font)

            if note.duration is not None:
                # 1. Chord numbers & Slide Logic
                if note.chord and note.style != StrumStyle.NO_HIT:
                    strings = [note.chord.string1, note.chord.string2, note.chord.string3,
                               note.chord.string4, note.chord.string5, note.chord.string6]
                    for i, fret in enumerate(strings):
                        if fret is not None and fret != -1:
                            y = row_y_top + (i * LINE_SPACING)
                            label = "X" if note.style == StrumStyle.MUTED else str(fret)
                            
                            # Calculate dynamic masking rectangle based on font size
                            text_w, text_h = draw.textbbox((0, 0), label, font=fret_font)[2:]
                            draw.rectangle([current_x - 2, y - (text_h//2), current_x + text_w + 2, y + (text_h//2)], fill="white")
                            draw.text((current_x, y - (text_h // 2)), label, fill="black", font=fret_font)

                            # --- SLIDE LOGIC ---
                            if note.style == StrumStyle.SLIDE:
                                draw.line([(current_x + text_w + 5, y), (next_x - 5, y)], fill="black", width=1)
                                arc_box = [current_x + 5, y - 20, next_x - 5, y - 5]
                                draw.arc(arc_box, start=180, end=0, fill="black", width=1)

                    # 2. Palm Mute Logic
                    if note.style == StrumStyle.PALM_MUTED:
                        pm_y = row_y_top + PM_Y_OFFSET
                        line_start_x = current_x
                        if last_style != StrumStyle.PALM_MUTED or is_new_line:
                            draw.text((current_x, pm_y - 12), "P.M.", fill="black", font=small_font)
                            line_start_x += 35 
                        draw_dashed_segment(line_start_x, next_x, pm_y)
                        is_last_pm = (idx + 1 == len(segment_notes)) or (segment_notes[idx+1].style != StrumStyle.PALM_MUTED)
                        if is_last_pm:
                            draw.line([(next_x, pm_y - TICK_H/2), (next_x, pm_y + TICK_H/2)], fill="black", width=1)

                # 3. Rhythmic Stems
                stem_y_start = row_y_top + (6 * LINE_SPACING)
                stem_x = current_x + 4
                bottom_y = stem_y_start + 30
                
                if note.duration >= 2:
                    draw.line([(stem_x, stem_y_start), (stem_x, bottom_y)], fill="black", width=2)
                    if note.duration == 3: # Dot
                        dot_x = stem_x + 8
                        dot_y = bottom_y - 5
                        draw.ellipse([dot_x - 2, dot_y - 2, dot_x + 2, dot_y + 2], fill="black")

                elif note.duration == 1:
                    draw.line([(stem_x, stem_y_start), (stem_x, bottom_y)], fill="black", width=2)
                    can_beam_fwd = (unit_in_measure % 2 == 0) and (idx + 1 < len(segment_notes)) and (segment_notes[idx+1].duration == 1)
                    is_beamed_back = (unit_in_measure % 2 != 0) and (idx > 0) and (segment_notes[idx-1].duration == 1)
                    if can_beam_fwd:
                        draw.line([(stem_x, bottom_y), (stem_x + BEAT_WIDTH, bottom_y)], fill="black", width=4)
                    elif not is_beamed_back:
                        draw.line([(stem_x, bottom_y), (stem_x + 12, bottom_y)], fill="black", width=2)

            last_style = note.style
            if (acc_dur_segment + note_dur) % UNITS_PER_MEASURE == 0 and note.duration is not None:
                global_measure_counter += 1

            if (acc_dur_segment + note_dur) % (UNITS_PER_MEASURE * MEASURES_PER_LINE) == 0:
                draw.line([(MARGIN_LEFT + LINE_CONTENT_WIDTH, row_y_top), 
                           (MARGIN_LEFT + LINE_CONTENT_WIDTH, row_y_top + 5 * LINE_SPACING)], fill="black", width=2)

            acc_dur_segment += (note.duration if note.duration else 0)

        if acc_dur_segment % (UNITS_PER_MEASURE * MEASURES_PER_LINE) != 0:
            draw.line([(final_x, final_y), (final_x, final_y + 5 * LINE_SPACING)], fill="black", width=2)

        num_systems_in_segment = math.ceil(acc_dur_segment / (UNITS_PER_MEASURE * MEASURES_PER_LINE))
        current_y_cursor += (num_systems_in_segment * SYSTEM_HEIGHT) + 20

    img.save(output_path)