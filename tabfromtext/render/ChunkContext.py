from dataclasses import dataclass
import tabfromtext.render.LayoutUtils as lu


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

    @staticmethod
    def build(chunk_acc, chunk_dur, note_tick, base_y) -> "ChunkContext":
        x = lu.tick_to_x(chunk_acc)
        return ChunkContext(
            acc=chunk_acc,
            dur=chunk_dur,
            strings_y=lu.tick_to_strings_y(chunk_acc, base_y),
            stem_y=lu.tick_to_stem_y(chunk_acc, base_y),
            is_new_line=lu.is_new_system(chunk_acc),
            x=x,
            next_x=x + chunk_dur * lu.beat_w_px,
            stem_x=x + lu.px(lu.cfg.stems.x_offset_pt),
            is_first=(chunk_acc == note_tick),
        )