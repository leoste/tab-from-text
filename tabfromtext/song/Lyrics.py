from tabfromtext.util.TimeUtils import convertTimeToTicks


class Lyrics:
    def __init__(self, text: str, durations: list, offset: float = 0) -> None:
        self.text = text
        self.durations = durations
        self.offset = offset

    def flatten_durations(self) -> list:
        result = []
        for dur in self.durations:
            ticks = convertTimeToTicks(dur)
            result.append(ticks)
            result.extend([None] * (ticks - 1))
        return result

    def total_ticks(self) -> int:
        """Total duration in ticks across all syllables."""
        return sum(convertTimeToTicks(d) for d in self.durations if d is not None)