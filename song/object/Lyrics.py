from object.TimeUtils import convertTimeToTicks


class Lyrics:
    def __init__(self, text: str, durations: list) -> None:
        self.text = text
        self.durations = durations

    def flatten_durations(self) -> list:
        result = []
        for dur in self.durations:
            ticks = convertTimeToTicks(dur)
            result.append(ticks)
            result.extend([None] * (ticks - 1))
        return result