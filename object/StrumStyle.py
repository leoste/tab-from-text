from enum import Enum

class StrumStyle(Enum):
    NO_HIT = -1 # silent, no hit, no strum
    NORMAL = 0
    MUTED = 1
    PALM_MUTED = 2
    BEND = 3
    SLIDE = 4