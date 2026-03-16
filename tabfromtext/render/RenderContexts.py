from dataclasses import dataclass


@dataclass
class NoteContext:
    """Everything known about a note at the outer loop level."""
    note:           object   # the Note object
    idx:            int      # index in segment_notes
    segment_notes:  list
    tick:           int      # absolute tick of note start
    strings_y:      int      # y of 1st string in this note's system row
    x:              int      # left edge x of the note
    next_x:         int      # x after the note's full duration
    is_new_line:    bool
    # neighbours for beam decisions (resolved once per note, not per chunk)
    prev_real_note: object
    next_real_note: object
    # mutable palm-mute threading state
    last_style:     object
    last_pm_x:      object   # int | None
    last_pm_y:      object   # int | None


@dataclass
class ChunkContext:
    """Everything known about one chunk of a (possibly split) note."""
    acc:         int   # absolute tick of chunk start
    dur:         int   # duration of this chunk in ticks
    strings_y:   int   # y of 1st string in this chunk's system row
    stem_y:      int   # y where stems start (below 6th string)
    is_new_line: bool
    x:           int   # left edge x
    next_x:      int   # x after chunk duration
    stem_x:      int   # x of the stem
    is_first:    bool  # True for the first chunk of a note