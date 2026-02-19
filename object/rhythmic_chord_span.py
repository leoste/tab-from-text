from typing import List
from .chord_span import ChordSpan

class RhythmicChordSpan:
    def __init__(self, durations: List[int], chords: List[ChordSpan]) -> None:
        self.durations: List[int] = durations
        self.chords: List[ChordSpan] = chords
