from object.Chord import Chord
from object.Note import Note


class ChordSpan:
    def __init__(self, duration: int, chord: Chord) -> None:
        self.duration: int = duration
        self.chord: Chord = chord

    def flattenChordSpan(self) -> list[Chord]:
        return [self.chord] * Note.convertTimeToTicks(self.duration)