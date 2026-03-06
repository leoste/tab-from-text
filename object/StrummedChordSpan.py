from object.NoteProvider import NoteProvider
from object.ChordSpan import ChordSpan
from object.StrumStyle import StrumStyle
from object.Note import Note


class StrummedChordSpan(NoteProvider):
    def __init__(self, chordSpan: ChordSpan, style: StrumStyle = StrumStyle.NORMAL) -> None:
        self.chordSpan = chordSpan
        self.style = style

    def getNotes(self) -> list[Note]:
        chords = self.chordSpan.flattenChordSpan()
        durations = Note.flattenDuration(self.chordSpan.duration)
        styles = StrumStyle.flattenStyle(self.style)

        notes = []
        for index, chord in enumerate(chords):
            duration = durations[index % len(durations)]
            if duration is not None:
                style = styles[index % len(styles)]

                if style == StrumStyle.NO_HIT:
                    notes += [Note(None, duration, style)]
                else:
                    notes += [Note(chord, duration, style)]
            else:
                notes += [Note(None, None, None)]
        return notes