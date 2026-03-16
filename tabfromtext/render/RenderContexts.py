from dataclasses import dataclass


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


@dataclass
class ChunkContext:
    """Positional data about one chunk of a (possibly split) note."""
    acc:         int   # absolute tick of chunk start
    dur:         int   # duration of this chunk in ticks (determines visual note type)
    strings_y:   int   # y of 1st string in this chunk's system row
    stem_y:      int   # y where stems start (below 6th string)
    is_new_line: bool
    x:           int   # left edge x
    next_x:      int   # x after chunk duration
    stem_x:      int   # x of the stem
    is_first:    bool  # True for the first chunk of a note


@dataclass
class SegmentRenderState:
    """Mutable state that threads through an entire segment render pass.

    Carries everything that depends on what has been drawn so far —
    not properties of any single note, but of the rendering in progress.
    """
    last_style: object = None   # style of the last rendered note
    last_pm_x:  object = None   # x where the current P.M. line left off (int | None)
    last_pm_y:  object = None   # y of the current P.M. line (int | None)