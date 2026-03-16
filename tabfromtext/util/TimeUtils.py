TIME_RESOLUTION = 2

def convertTimeToTicks(duration) -> int:
    return round(duration * TIME_RESOLUTION)