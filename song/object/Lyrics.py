from object.TimeUtils import convertTimeToTicks


class Lyrics:
    def __init__(self, text: str, durations: list, offset: float = 0) -> None:
        self.text = text
        self.durations = durations
        self.offset = offset  # in 1/8th notes; positive = start later, negative = start earlier (draws left of margin)

    def flatten_durations(self) -> list:
        result = []
        for dur in self.durations:
            ticks = convertTimeToTicks(dur)
            result.append(ticks)
            result.extend([None] * (ticks - 1))
        return result