from typing import List
from object.StrumStyle import StrumStyle

class Rhythm:
    def __init__(self, durations: List[int], styles: List[StrumStyle]):
        self.durations = durations
        self.styles = styles