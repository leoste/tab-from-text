from enum import Enum
from tabfromtext.util.TimeUtils import convertTimeToTicks


class StrumStyle(Enum):
    NO_HIT = -1
    NORMAL = 0
    MUTED = 1
    PALM_MUTED = 2
    BEND = 3
    SLIDE = 4

    @staticmethod
    def flattenStyle(style: 'StrumStyle') -> list['StrumStyle']:
        ticks = convertTimeToTicks(1)
        return [style] * ticks