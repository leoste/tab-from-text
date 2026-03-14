from song.object.NoteProvider import NoteProvider
from song.object.ChordSpan import ChordSpan
from song.object.StrumStyle import StrumStyle
from song.object.Note import Note
from song.object.Chord import Chord


class StrummedChordSpan(NoteProvider):
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