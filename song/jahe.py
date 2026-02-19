from object.rhythmic_chord_span import RhythmicChordSpan
from object.chord_span import ChordSpan
from object.chord import Chord
from object.guitar_string import GuitarString

INTRO_RHYTHMIC_PATTERN = [2,1,1,2,1,1,1,1,1,2,1,1,1]

CHORD_11_D_SHARP = Chord.get_power_chord(GuitarString.E6, 11)
CHORD_9_C_SHARP = Chord.get_power_chord(GuitarString.E6, 9)
CHORD_8_C = Chord.get_power_chord(GuitarString.E6, 8)
CHORD_6_A_SHARP = Chord.get_power_chord(GuitarString.E6, 6)
CHORD_4_G_SHARP = Chord.get_power_chord(GuitarString.E6, 4)
CHORD_2_F_SHARP = Chord.get_power_chord(GuitarString.E6, 2)
CHORD_1_F = Chord.get_power_chord(GuitarString.E6, 1)

user_data = [
    RhythmicChordSpan(
        INTRO_RHYTHMIC_PATTERN,
        [
            ChordSpan(16, CHORD_6_A_SHARP),
            ChordSpan(16, CHORD_2_F_SHARP),
            ChordSpan(16, CHORD_4_G_SHARP),
            ChordSpan(16, CHORD_1_F),
            ChordSpan(16, CHORD_6_A_SHARP),
            ChordSpan(16, CHORD_2_F_SHARP),
            ChordSpan(16, CHORD_11_D_SHARP),
            ChordSpan(32, CHORD_1_F)
        ]
    )
]