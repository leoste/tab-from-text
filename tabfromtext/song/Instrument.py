from typing import List


class Instrument:
    def __init__(self, name: str, segments: List):
        self.name = name
        self.segments = segments