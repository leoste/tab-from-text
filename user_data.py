class RhythmicChordSpan:

    # TODO: add typing hints to variables except self. durations is int[] and chords is ChordSpan[]
    def RhythmicChordSpan(self, durations, chords):
        self.durations = durations
        self.chords = chords

class ChordSpan:

    # TODO: add typing hints. chord is Chord, duration is int[]
    def ChordSpan(self, duration, chord):
        self.duration = duration
        self.chord = chord

class Chord:

    # TODO: add typing hints except self. string1-string6 are ints representing the fret position to be placed on a given string.
    # TODO: -1 means the string isn't a part of the chord, it isn't played at all. document this.
    def Chord(self, string1, string2, string3, string4, string5, string6):
        self.string1 = string1
        self.string2 = string2
        self.string3 = string3
        self.string4 = string4
        self.string5 = string5
        self.string6 = string6

    @staticmethod
    def get_power_chord(base_string, base_fret):
        if (base_string == 6):
            return Chord(-1,-1,-1,base_fret+2,base_fret+2,base_fret)
        elif (base_string == 5):
            return Chord(-1,-1,base_fret+2,base_fret+2,base_fret,-1)

intro_rhythmic_pattern = [2,1,1,2,1,1,1,1,1,2,1,1,1]
intro_chord_duration = 16

chord_11_d_sharp = Chord.get_power_chord(6, 11)
chord_9_c_sharp = Chord.get_power_chord(6, 9)
chord_8_c = Chord.get_power_chord(6, 8)
chord_6_a_sharp = Chord.get_power_chord(6, 6)
chord_4_g_sharp = Chord.get_power_chord(6, 4)
chord_2_f_sharp = Chord.get_power_chord(6, 2)
chord_1_f = Chord.get_power_chord(6, 1)

user_data = [
    RhythmicChordSpan(
        intro_rhythmic_pattern,
        [
            ChordSpan(16, chord_6_a_sharp),
            ChordSpan(16, chord_2_f_sharp),
            ChordSpan(16, chord_4_g_sharp),
            ChordSpan(16, chord_1_f),
            ChordSpan(16, chord_6_a_sharp),
            ChordSpan(16, chord_2_f_sharp),
            ChordSpan(16, chord_11_d_sharp),
            ChordSpan(32, chord_1_f)
        ]
    )
]