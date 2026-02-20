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
    SYSTEM_HEIGHT = (6 * LINE_SPACING) + 120 
    
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

    # --- Rendering State ---
    acc_dur_total = 0 
    
    for idx, note in enumerate(notes):
        # 1. Determine Position
        system_idx = int(acc_dur_total // (UNITS_PER_MEASURE * MEASURES_PER_LINE))
        measure_in_system = int((acc_dur_total // UNITS_PER_MEASURE) % MEASURES_PER_LINE)
        unit_in_measure = acc_dur_total % UNITS_PER_MEASURE
        
        current_y_top = TITLE_HEIGHT + (system_idx * SYSTEM_HEIGHT)
        
        if acc_dur_total % (UNITS_PER_MEASURE * MEASURES_PER_LINE) == 0:
            draw_staff_elements(current_y_top)

        current_x = MARGIN_LEFT + (measure_in_system * MEASURE_WIDTH) + (unit_in_measure * BEAT_WIDTH) + BAR_PADDING

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

            # 4. FIXED Rhythmic Stems & Flags
            stem_y_start = current_y_top + (6 * LINE_SPACING)
            stem_x = current_x + 4
            bottom_y = stem_y_start + 30
            
            # Every note gets a vertical stem
            draw.line([(stem_x, stem_y_start), (stem_x, bottom_y)], fill="black", width=2)
            
            if note.duration == 1:
                # Check if we beam forward (starts on even beat position)
                can_beam_forward = (unit_in_measure % 2 == 0) and (idx + 1 < len(notes)) and (notes[idx+1].duration == 1)
                
                # Check if we are receiving a beam from behind
                is_beamed_from_behind = (unit_in_measure % 2 != 0) and (idx > 0) and (notes[idx-1].duration == 1)
                
                if can_beam_forward:
                    # Draw thick beam to the next note
                    draw.line([(stem_x, bottom_y), (stem_x + BEAT_WIDTH, bottom_y)], fill="black", width=4)
                elif not is_beamed_from_behind:
                    # If neither, it's a lone note (on-beat or off-beat) -> Draw the 'L' flag
                    draw.line([(stem_x, bottom_y), (stem_x + 12, bottom_y)], fill="black", width=2)

        # 5. Right-edge closure
        if (acc_dur_total + (note.duration or 0)) % (UNITS_PER_MEASURE * MEASURES_PER_LINE) == 0:
            draw.line([(MARGIN_LEFT + LINE_CONTENT_WIDTH, current_y_top), 
                       (MARGIN_LEFT + LINE_CONTENT_WIDTH, current_y_top + 5 * LINE_SPACING)], fill="black", width=2)

        acc_dur_total += (note.duration if note.duration else 0)

    img.save(output_path)