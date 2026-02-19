from typing import List
from .chord import Chord

class ChordSpan:
    def __init__(self, duration: List[int], chord: Chord) -> None:
        self.duration: List[int] = duration
        self.chord: Chord = chord
