from enum import Enum
from object.TimeUtils import convertTimeToTicks


class StrumStyle(Enum):
    NO_HIT = -1 # silent, no hit, no strum
    NORMAL = 0
    MUTED = 1
    PALM_MUTED = 2
    BEND = 3
    SLIDE = 4

    @staticmethod
    def flattenStyle(style: 'StrumStyle') -> list['StrumStyle']:
        ticks = convertTimeToTicks(1)  # each style entry covers one eighth note = TIME_RESOLUTION ticks
        return [style] * ticks