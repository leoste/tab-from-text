import math
from PIL import Image, ImageDraw, ImageFont
from object.StrumStyle import StrumStyle
from object.Segment import Segment
from object.Note import Note

def render_tab(segment: Segment, output_path="guitar_tab_v5.png"):
    notes = Note.GetNotesFromSegment(segment)

    # --- Configuration ---
    LINE_SPACING = 25
    BEAT_WIDTH = 45   
    MARGIN_LEFT = 80
    BAR_PADDING = 20  # The extra space we add after each bar line
    
    TITLE_HEIGHT = 40
    MARGIN_TOP = 60 + TITLE_HEIGHT 
    
    STEM_Y_START = MARGIN_TOP + (6 * LINE_SPACING) 
    STEM_HEIGHT = 30
    FLAG_SIZE = 12
    UNITS_PER_MEASURE = 8
    
    # 1. Calculate dimensions accurately
    total_units = sum((n.duration if n.duration else 0.5) for n in notes)
    
    # NEW: Account for the cumulative BAR_PADDING
    num_measures = math.ceil(total_units / UNITS_PER_MEASURE)
    # Total width = notes + (bars * padding) + margins + ending buffer
    img_width = int(total_units * BEAT_WIDTH) + (num_measures * BAR_PADDING) + MARGIN_LEFT + 100
    
    img_height = STEM_Y_START + 80
    img = Image.new('RGB', (img_width, img_height), color='white')
    draw = ImageDraw.Draw(img)
    
    try:
        title_font = ImageFont.truetype("arialbd.ttf", 24)
    except:
        title_font = ImageFont.load_default()

    # Draw Title
    draw.text((MARGIN_LEFT, MARGIN_TOP - TITLE_HEIGHT - 20), segment.title, fill="black", font=title_font)

    # 2. Draw Strings
    string_names = ['e', 'B', 'G', 'D', 'A', 'E']
    for i, name in enumerate(string_names):
        y = MARGIN_TOP + (i * LINE_SPACING)
        draw.text((20, y - 10), name, fill="black")
        # Ensure string lines span the full calculated width
        draw.line([(MARGIN_LEFT, y), (img_width - 40, y)], fill=(200, 200, 200))

    current_x = MARGIN_LEFT
    acc_dur = 0 
    
    def draw_bar(x):
        draw.line([(x, MARGIN_TOP), (x, MARGIN_TOP + 5 * LINE_SPACING)], fill="black", width=2)

    # Initial Bar
    draw_bar(current_x)
    current_x += BAR_PADDING 

    for idx, note in enumerate(notes):
        # 3. Measure Boundary Reset
        if acc_dur >= UNITS_PER_MEASURE:
            draw_bar(current_x)
            current_x += BAR_PADDING
            acc_dur = 0

        if note.duration is None:
            current_x += (BEAT_WIDTH * 0.5)
            continue

        # 4. Render Chord
        if note.chord and note.style != StrumStyle.NO_HIT:
            strings = [note.chord.string1, note.chord.string2, note.chord.string3,
                       note.chord.string4, note.chord.string5, note.chord.string6]
            
            for i, fret in enumerate(strings):
                if fret is not None and fret != -1:
                    y = MARGIN_TOP + (i * LINE_SPACING)
                    label = "X" if note.style == StrumStyle.MUTED else str(fret)
                    draw.rectangle([current_x - 4, y - 8, current_x + 12, y + 8], fill="white")
                    draw.text((current_x, y - 8), label, fill="black")

            # 5. Rhythmic Stems & Beams
            stem_x = current_x + 4
            bottom_y = STEM_Y_START + STEM_HEIGHT
            draw.line([(stem_x, STEM_Y_START), (stem_x, bottom_y)], fill="black", width=2)

            if note.duration == 1:
                can_beam = False
                if acc_dur % 2 == 0 and (idx + 1) < len(notes):
                    next_note = notes[idx + 1]
                    if next_note.duration == 1:
                        can_beam = True
                
                is_second_half = False
                if acc_dur % 2 != 0 and idx > 0:
                    prev_note = notes[idx - 1]
                    if prev_note.duration == 1:
                        is_second_half = True

                if can_beam:
                    draw.line([(stem_x, bottom_y), (stem_x + (note.duration * BEAT_WIDTH), bottom_y)], fill="black", width=4)
                elif not is_second_half:
                    draw.line([(stem_x, bottom_y), (stem_x + FLAG_SIZE, bottom_y)], fill="black", width=2)

        current_x += (note.duration * BEAT_WIDTH)
        acc_dur += note.duration

    # Final closing bar
    draw_bar(current_x)
    img.save(output_path)