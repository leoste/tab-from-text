from typing import List
from object.RhythmicChordSpan import RhythmicChordSpan


class Segment:
    def __init__(self, title: str, parts: List[RhythmicChordSpan]):
        self.title = title
        self.parts = parts