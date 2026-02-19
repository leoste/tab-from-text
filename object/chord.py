from .guitar_string import GuitarString

# Yes I know it's not the best to store this constant here, yes I did it anyways
FRET_NOT_PLAYED = -1

class Chord:    

    def __init__(self, string1: int, string2: int, string3: int, string4: int, string5: int, string6: int) -> None:
        self.string1 = string1
        self.string2 = string2
        self.string3 = string3
        self.string4 = string4
        self.string5 = string5
        self.string6 = string6

    @staticmethod
    def get_power_chord(base_string: GuitarString, base_fret: int) -> 'Chord':
        if base_string == GuitarString.E6:
            return Chord(FRET_NOT_PLAYED, FRET_NOT_PLAYED, FRET_NOT_PLAYED, base_fret + 2, base_fret + 2, base_fret)
        elif base_string == GuitarString.A5:
            return Chord(FRET_NOT_PLAYED, FRET_NOT_PLAYED, base_fret + 2, base_fret + 2, base_fret, FRET_NOT_PLAYED)
