TIME_RESOLUTION = 2

TICKS_SIXTEENTH     = TIME_RESOLUTION // 2
TICKS_DOTTED_EIGHTH = TICKS_SIXTEENTH * 3
TICKS_EIGHTH        = 1 * TIME_RESOLUTION
TICKS_HALF_NOTE     = 4 * TIME_RESOLUTION
TICKS_FULL_NOTE     = 8 * TIME_RESOLUTION


def convertTimeToTicks(duration) -> int:
    return round(duration * TIME_RESOLUTION)


def is_dotted(duration: int) -> bool:
    """True if duration represents a dotted rhythm value."""
    if duration <= 0:
        return False
    doubled = duration * 2
    if doubled % 3 != 0:
        return False
    base = doubled // 3
    return base > 0 and (base & (base - 1)) == 0