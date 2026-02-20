from object.GuitarString import GuitarString

class Chord:    

    def __init__(self, string1: int, string2: int, string3: int, string4: int, string5: int, string6: int) -> None:
        self.string1 = string1
        self.string2 = string2
        self.string3 = string3
        self.string4 = string4
        self.string5 = string5
        self.string6 = string6

    def __str__(self):
        return f"({self.string1}, {self.string2}, {self.string3}, {self.string4}, {self.string5}, {self.string6})"
    
    def __repr__(self):
        return self.__str__()

    @staticmethod
    def get_power_chord(base_string: GuitarString, base_fret: int) -> 'Chord':
        if base_string == GuitarString.E6:
            return Chord(None, None, None, base_fret + 2, base_fret + 2, base_fret)
        elif base_string == GuitarString.A5:
            return Chord(None, None, base_fret + 2, base_fret + 2, base_fret, None)

    @staticmethod
    def get_no_strings_hit_chord():
        return Chord(-1,-1,-1,-1,-1,-1)