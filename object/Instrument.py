from typing import List
from object.Segment import Segment


class Instrument:
    def __init__(self, name: str, segments: List[Segment]):
        self.name = name
        self.segments = segments