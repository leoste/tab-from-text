from typing import List
from tabfromtext.song.StrumStyle import StrumStyle

class Rhythm:
    def __init__(self, durations: List[int], styles: List[StrumStyle] = [StrumStyle.NORMAL]):
        self.durations = durations
        self.styles = styles