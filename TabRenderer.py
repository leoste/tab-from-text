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
    TITLE_HEIGHT = 80 
    SYSTEM_HEIGHT = (6 * LINE_SPACING) + 140 # Increased to accommodate P.M. notation
    
    # P.M. Specific Constants
    PM_Y_OFFSET = -15
    DASH_GAP = 5
    TICK_H = 8

    # Calculate Measure Width based on units
    MEASURE_WIDTH = (UNITS_PER_MEASURE * BEAT_WIDTH) + BAR_PADDING
    LINE_CONTENT_WIDTH = MEASURES_PER_LINE * MEASURE_WIDTH
    
    # Accurate Dimension Calculation
    total_units = sum((n.duration if n.duration else 0.5) for n in notes)
    num_measures = math.ceil(total_units / UNITS_PER_MEASURE)
    num_systems = math.ceil(num_measures / MEASURES_PER_LINE)

    img_width = LINE_CONTENT_WIDTH + MARGIN_LEFT + MARGIN_RIGHT
    img_height = TITLE_HEIGHT + (num_systems * SYSTEM_HEIGHT) + 40
    
    img = Image.new('RGB', (int(img_width), int(img_height)), color='white')
    draw = ImageDraw.Draw(img)
    
    # Global Title
    draw.text((MARGIN_LEFT, 20), segment.title, fill="black")

    def draw_staff_elements(y_top):
        string_names = ['e', 'B', 'G', 'D', 'A', 'E']
        for i, name in enumerate(string_names):
            y = y_top + (i * LINE_SPACING)
            draw.text((20, y - 10), name, fill="black")
            draw.line([(MARGIN_LEFT, y), (MARGIN_LEFT + LINE_CONTENT_WIDTH, y)], fill=(200, 200, 200))
        # First bar of every line
        draw.line([(MARGIN_LEFT, y_top), (MARGIN_LEFT, y_top + 5 * LINE_SPACING)], fill="black", width=2)

    def draw_dashed_segment(x_start, x_end, y):
        curr = x_start
        while curr < x_end:
            draw.line([(curr, y), (min(curr + DASH_GAP, x_end), y)], fill="black", width=1)
            curr += DASH_GAP * 2

    # --- Rendering State ---
    acc_dur_total = 0 
    final_x = MARGIN_LEFT 
    final_y = TITLE_HEIGHT 
    last_style = None # Track the style of the previous note
    
    for idx, note in enumerate(notes):
        # 1. Determine Position
        system_idx = int(acc_dur_total // (UNITS_PER_MEASURE * MEASURES_PER_LINE))
        measure_in_system = int((acc_dur_total // UNITS_PER_MEASURE) % MEASURES_PER_LINE)
        unit_in_measure = acc_dur_total % UNITS_PER_MEASURE
        
        current_y_top = TITLE_HEIGHT + (system_idx * SYSTEM_HEIGHT)
        final_y = current_y_top
        
        if acc_dur_total % (UNITS_PER_MEASURE * MEASURES_PER_LINE) == 0:
            draw_staff_elements(current_y_top)

        current_x = MARGIN_LEFT + (measure_in_system * MEASURE_WIDTH) + (unit_in_measure * BEAT_WIDTH) + BAR_PADDING
        note_dur = (note.duration or 0.5)
        next_x = current_x + (note_dur * BEAT_WIDTH)
        final_x = next_x

        # 2. Draw Mid-line Bars
        if unit_in_measure == 0 and measure_in_system > 0:
            bar_x = MARGIN_LEFT + (measure_in_system * MEASURE_WIDTH)
            draw.line([(bar_x, current_y_top), (bar_x, current_y_top + 5 * LINE_SPACING)], fill="black", width=2)

        # 3. Render Chord/Note
        if note.duration is not None and note.chord and note.style != StrumStyle.NO_HIT:
            strings = [note.chord.string1, note.chord.string2, note.chord.string3,
                       note.chord.string4, note.chord.string5, note.chord.string6]
            for i, fret in enumerate(strings):
                if fret is not None and fret != -1:
                    y = current_y_top + (i * LINE_SPACING)
                    label = "X" if note.style == StrumStyle.MUTED else str(fret)
                    draw.rectangle([current_x - 4, y - 8, current_x + 12, y + 8], fill="white")
                    draw.text((current_x, y - 8), label, fill="black")

            # --- Palm Mute Handling (Look-behind) ---
            if note.style == StrumStyle.PALM_MUTED:
                pm_y = current_y_top + PM_Y_OFFSET
                line_start_x = current_x
                
                # If this is the start of a PM section, draw the text
                if last_style != StrumStyle.PALM_MUTED:
                    draw.text((current_x, pm_y - 10), "P.M.", fill="black")
                    line_start_x += 35 # Offset line to start after "P.M." text
                
                # Draw dashed segment for this note only
                draw_dashed_segment(line_start_x, next_x, pm_y)
                
                # Look ahead ONLY to check if we need to terminate the line with a tick
                is_last_pm = (idx + 1 == len(notes)) or (notes[idx+1].style != StrumStyle.PALM_MUTED)
                if is_last_pm:
                    draw.line([(next_x, pm_y - TICK_H/2), (next_x, pm_y + TICK_H/2)], fill="black", width=1)

            # 4. Rhythmic Stems & Flags
            stem_y_start = current_y_top + (6 * LINE_SPACING)
            stem_x = current_x + 4
            bottom_y = stem_y_start + 30
            draw.line([(stem_x, stem_y_start), (stem_x, bottom_y)], fill="black", width=2)
            
            if note.duration == 1:
                can_beam_forward = (unit_in_measure % 2 == 0) and (idx + 1 < len(notes)) and (notes[idx+1].duration == 1)
                is_beamed_from_behind = (unit_in_measure % 2 != 0) and (idx > 0) and (notes[idx-1].duration == 1)
                
                if can_beam_forward:
                    draw.line([(stem_x, bottom_y), (stem_x + BEAT_WIDTH, bottom_y)], fill="black", width=4)
                elif not is_beamed_from_behind:
                    draw.line([(stem_x, bottom_y), (stem_x + 12, bottom_y)], fill="black", width=2)

        # Update style tracker for next iteration
        last_style = note.style

        # 5. Right-edge closure
        if (acc_dur_total + (note.duration or 0)) % (UNITS_PER_MEASURE * MEASURES_PER_LINE) == 0:
            draw.line([(MARGIN_LEFT + LINE_CONTENT_WIDTH, current_y_top), 
                       (MARGIN_LEFT + LINE_CONTENT_WIDTH, current_y_top + 5 * LINE_SPACING)], fill="black", width=2)

        acc_dur_total += (note.duration if note.duration else 0)

    # 6. ABSOLUTE FINAL BAR
    if acc_dur_total % (UNITS_PER_MEASURE * MEASURES_PER_LINE) != 0:
        draw.line([(final_x, final_y), (final_x, final_y + 5 * LINE_SPACING)], fill="black", width=2)

    img.save(output_path)