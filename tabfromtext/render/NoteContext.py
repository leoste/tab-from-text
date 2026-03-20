from dataclasses import dataclass
import tabfromtext.render.LayoutUtils as lu


@dataclass
class NoteContext:
    """Immutable positional data about one note — where it lives on the page."""
    note:           object   # the Note object
    tick:           int      # absolute tick of note start
    strings_y:      int      # y of 1st string in this note's system row
    x:              int      # left edge x of the note
    next_x:         int      # x after the note's full duration
    is_new_line:    bool
    prev_real_note: object   # nearest preceding note with a duration (for beam decisions)
    next_real_note: object   # nearest following note with a duration (for beam decisions)

    @staticmethod
    def build(note, idx, segment_notes, tick, base_y) -> "NoteContext":
        x   = lu.tick_to_x(tick)
        dur = note.duration or 0

        next_real_idx = next(
            (i for i in range(idx + 1, len(segment_notes))
             if segment_notes[i].duration is not None), None)
        prev_real_idx = next(
            (i for i in range(idx - 1, -1, -1)
             if segment_notes[i].duration is not None), None)

        return NoteContext(
            note=note,
            tick=tick,
            strings_y=lu.tick_to_strings_y(tick, base_y),
            x=x,
            next_x=x + dur * lu.beat_w_px,
            is_new_line=lu.is_new_system(tick),
            prev_real_note=segment_notes[prev_real_idx] if prev_real_idx is not None else None,
            next_real_note=segment_notes[next_real_idx] if next_real_idx is not None else None,
        )