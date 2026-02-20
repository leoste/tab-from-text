from typing import List
from object.ChordSpan import ChordSpan
from object.Rhythm import Rhythm

class RhythmicChordSpan:
    def __init__(self, rhythm: Rhythm, chordSpans: List[ChordSpan]) -> None:
        self.rhythm: Rhythm = rhythm
        self.chordSpans: List[ChordSpan] = chordSpans
