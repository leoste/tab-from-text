import math
from PIL import Image, ImageDraw, ImageFont
from object.StrumStyle import StrumStyle
from object.Segment import Segment
from object.Note import Note

def render_tab(segment: Segment, output_path="guitar_tab.png"):
    notes = Note.GetNotesFromSegment(segment)

    # --- Constants ---
    MEASURES_PER_LINE = 4
    UNITS_PER_MEASURE = 8
    LINE_SPACING = 25
    BEAT_WIDTH = 45   
    BAR_PADDING = 25  
    MARGIN_LEFT = 80
    MARGIN_RIGHT = 80 
    
    # Increased TITLE_HEIGHT to prevent overlap with Measure 1 numbers
    TITLE_HEIGHT = 120 
    
    # Vertical spacing between the systems
    SYSTEM_HEIGHT = (6 * LINE_SPACING) + 160 
    
    # P.M. Styling
    PM_Y_OFFSET = -20
    DASH_GAP = 5
    TICK_H = 8
    
    # Measure Number Styling
    MEASURE_NUM_Y_OFFSET = -45

    MEASURE_WIDTH = (UNITS_PER_MEASURE * BEAT_WIDTH) + BAR_PADDING
    LINE_CONTENT_WIDTH = MEASURES_PER_LINE * MEASURE_WIDTH
    
    total_units = sum((n.duration if n.duration else 0.5) for n in notes)
    num_measures = math.ceil(total_units / UNITS_PER_MEASURE)
    num_systems = math.ceil(num_measures / MEASURES_PER_LINE)

    img_width = LINE_CONTENT_WIDTH + MARGIN_LEFT + MARGIN_RIGHT
    img_height = TITLE_HEIGHT + (num_systems * SYSTEM_HEIGHT) + 40
    
    img = Image.new('RGB', (int(img_width), int(img_height)), color='white')
    draw = ImageDraw.Draw(img)
    
    try:
        title_font = ImageFont.truetype("arialbd.ttf", 28)
        small_font = ImageFont.truetype("arial.ttf", 12)
    except:
        title_font = small_font = ImageFont.load_default()

    # Draw Global Title - Positioned higher up
    draw.text((MARGIN_LEFT, 30), segment.title, fill="black", font=title_font)

    def draw_staff_elements(y_top, start_measure_num):
        string_names = ['e', 'B', 'G', 'D', 'A', 'E']
        for i, name in enumerate(string_names):
            y = y_top + (i * LINE_SPACING)
            draw.text((20, y - 10), name, fill="black")
            draw.line([(MARGIN_LEFT, y), (MARGIN_LEFT + LINE_CONTENT_WIDTH, y)], fill=(200, 200, 200))
        
        draw.line([(MARGIN_LEFT, y_top), (MARGIN_LEFT, y_top + 5 * LINE_SPACING)], fill="black", width=2)
        
        # Measure number at start of line
        draw.text((MARGIN_LEFT, y_top + MEASURE_NUM_Y_OFFSET), str(start_measure_num), fill="gray", font=small_font)

    def draw_dashed_segment(x_start, x_end, y):
        curr = x_start
        while curr < x_end:
            draw.line([(curr, y), (min(curr + DASH_GAP, x_end), y)], fill="black", width=1)
            curr += DASH_GAP * 2

    # --- Rendering State ---
    acc_dur_total = 0 
    final_x = MARGIN_LEFT 
    final_y = TITLE_HEIGHT 
    last_style = None 
    
    for idx, note in enumerate(notes):
        total_beats = acc_dur_total // UNITS_PER_MEASURE
        system_idx = int(acc_dur_total // (UNITS_PER_MEASURE * MEASURES_PER_LINE))
        measure_in_system = int(total_beats % MEASURES_PER_LINE)
        unit_in_measure = acc_dur_total % UNITS_PER_MEASURE
        
        # System position relative to the new title margin
        current_y_top = TITLE_HEIGHT + (system_idx * SYSTEM_HEIGHT)
        final_y = current_y_top
        
        is_new_line = (acc_dur_total % (UNITS_PER_MEASURE * MEASURES_PER_LINE) == 0)
        if is_new_line:
            start_num = int(total_beats + 1)
            draw_staff_elements(current_y_top, start_num)

        current_x = MARGIN_LEFT + (measure_in_system * MEASURE_WIDTH) + (unit_in_measure * BEAT_WIDTH) + BAR_PADDING
        note_dur = (note.duration or 0.5)
        next_x = current_x + (note_dur * BEAT_WIDTH)
        final_x = next_x

        if unit_in_measure == 0 and measure_in_system > 0:
            bar_x = MARGIN_LEFT + (measure_in_system * MEASURE_WIDTH)
            draw.line([(bar_x, current_y_top), (bar_x, current_y_top + 5 * LINE_SPACING)], fill="black", width=2)
            m_num = int(total_beats + 1)
            draw.text((bar_x, current_y_top + MEASURE_NUM_Y_OFFSET), str(m_num), fill="gray", font=small_font)

        if note.duration is not None and note.chord and note.style != StrumStyle.NO_HIT:
            strings = [note.chord.string1, note.chord.string2, note.chord.string3,
                       note.chord.string4, note.chord.string5, note.chord.string6]
            for i, fret in enumerate(strings):
                if fret is not None and fret != -1:
                    y = current_y_top + (i * LINE_SPACING)
                    label = "X" if note.style == StrumStyle.MUTED else str(fret)
                    draw.rectangle([current_x - 4, y - 8, current_x + 12, y + 8], fill="white")
                    draw.text((current_x, y - 8), label, fill="black")

            if note.style == StrumStyle.PALM_MUTED:
                pm_y = current_y_top + PM_Y_OFFSET
                line_start_x = current_x
                
                if last_style != StrumStyle.PALM_MUTED or is_new_line:
                    draw.text((current_x, pm_y - 10), "P.M.", fill="black")
                    line_start_x += 35 
                
                draw_dashed_segment(line_start_x, next_x, pm_y)
                
                is_last_pm = (idx + 1 == len(notes)) or (notes[idx+1].style != StrumStyle.PALM_MUTED)
                if is_last_pm:
                    draw.line([(next_x, pm_y - TICK_H/2), (next_x, pm_y + TICK_H/2)], fill="black", width=1)

            stem_y_start = current_y_top + (6 * LINE_SPACING)
            stem_x = current_x + 4
            bottom_y = stem_y_start + 30
            draw.line([(stem_x, stem_y_start), (stem_x, bottom_y)], fill="black", width=2)
            
            if note.duration == 1:
                can_beam_fwd = (unit_in_measure % 2 == 0) and (idx + 1 < len(notes)) and (notes[idx+1].duration == 1)
                is_beamed_back = (unit_in_measure % 2 != 0) and (idx > 0) and (notes[idx-1].duration == 1)
                
                if can_beam_fwd:
                    draw.line([(stem_x, bottom_y), (stem_x + BEAT_WIDTH, bottom_y)], fill="black", width=4)
                elif not is_beamed_back:
                    draw.line([(stem_x, bottom_y), (stem_x + 12, bottom_y)], fill="black", width=2)

        last_style = note.style

        if (acc_dur_total + (note.duration or 0)) % (UNITS_PER_MEASURE * MEASURES_PER_LINE) == 0:
            draw.line([(MARGIN_LEFT + LINE_CONTENT_WIDTH, current_y_top), 
                       (MARGIN_LEFT + LINE_CONTENT_WIDTH, current_y_top + 5 * LINE_SPACING)], fill="black", width=2)

        acc_dur_total += (note.duration if note.duration else 0)

    if acc_dur_total % (UNITS_PER_MEASURE * MEASURES_PER_LINE) != 0:
        draw.line([(final_x, final_y), (final_x, final_y + 5 * LINE_SPACING)], fill="black", width=2)

    img.save(output_path)