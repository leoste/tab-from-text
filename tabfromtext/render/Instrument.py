class Instrument:
    def __init__(self, name: str, segments: list):
        self.name = name
        self.segments = segments   # list[Segment] — shared objects, not copies