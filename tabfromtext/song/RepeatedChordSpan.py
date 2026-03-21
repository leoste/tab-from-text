from tabfromtext.song.NoteProvider import NoteProvider
from tabfromtext.song.ChordSpan import ChordSpan
from tabfromtext.song.StrumStyle import StrumStyle
from tabfromtext.song.Note import Note
from tabfromtext.song.Chord import Chord


class RepeatedChordSpan(NoteProvider):
    def __init__(self, duration: int, chord: Chord, times: int = 1, style: StrumStyle = StrumStyle.NORMAL) -> None:
        self.chordSpan = ChordSpan(duration, chord)
        self.times = times
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
                    notes += [Note(chord, duration, style)] * self.times
            else:
                notes += [Note(None, None, None)]
        return notes