from song.object.Chord import Chord
from song.object.ChordSpan import ChordSpan
from song.object.GuitarString import GuitarString
from song.object.Lyrics import Lyrics
from song.object.Rhythm import Rhythm
from song.object.RhythmicChordSpan import RhythmicChordSpan
from song.object.Segment import Segment
from song.object.Song import Song
from song.object.StrumStyle import StrumStyle
from song.object.StrummedChordSpan import StrummedChordSpan

RHYTHM = "Rhythm"

INTRO = Segment("INTRO", {
    RHYTHM: [
        StrummedChordSpan(4, Chord.power_chord(GuitarString.E6, 9)),
        StrummedChordSpan(4, Chord.power_chord(GuitarString.E6, 7)),
        StrummedChordSpan(4, Chord.power_chord(GuitarString.E6, 5)),
        StrummedChordSpan(4, Chord.power_chord(GuitarString.E6, 4)),
        StrummedChordSpan(4, Chord.power_chord(GuitarString.A5, 4)),
        StrummedChordSpan(4, Chord.power_chord(GuitarString.A5, 2)),
        StrummedChordSpan(8, Chord.power_chord(GuitarString.E6, 4)),
    ]
})

riff_chord_spans = [
    ChordSpan(4, Chord.power_chord(GuitarString.A5, 4)),
    ChordSpan(4, Chord.power_chord(GuitarString.E6, 5)),
    ChordSpan(4, Chord.power_chord(GuitarString.E6, 4)),
    ChordSpan(2, Chord.power_chord(GuitarString.E6, 5)),
    ChordSpan(2, Chord.power_chord(GuitarString.E6, 7)),
]

riff_rhythm = Rhythm(
    [1,1,1,1] * 4,
    ([StrumStyle.NORMAL] * 3 + [StrumStyle.NO_HIT]) * 3 + [StrumStyle.NORMAL, StrumStyle.NO_HIT] * 2
)

riff_measure = RhythmicChordSpan(
            riff_rhythm,
            riff_chord_spans
        )

RIFF = Segment("RIFF", {
    RHYTHM: [riff_measure] * 4
})

salm_main_durations = [1,1,2,1,1,2,1,1,2,2,2]
salm_alt_durations = [1,1,2,1,1,2,2,1,1,2,2]

SALM_1 = Segment("1. SALM", {
    RHYTHM: [riff_measure] * 3 + [
        RhythmicChordSpan(
            Rhythm(
                [1,1,1,1] * 3 + [2,1,1],
                ([StrumStyle.NORMAL] * 3 + [StrumStyle.NO_HIT]) * 3 + [StrumStyle.NORMAL] * 4
            ),
            [ChordSpan(16,Chord.power_chord(GuitarString.A5, 4))]
        )
    ]
}, Lyrics("""\
pimedas tänavas kõledas kostab
imelik virelik häbelik hüüdja
midagi polegi tänani muutun'd
kajaga lajatab lämmatav luumurd\
""", salm_main_durations * 4))

SALM_2 = Segment("2. SALM", {
    RHYTHM: [
        riff_measure,
        RhythmicChordSpan(
            Rhythm(
                [1,1,1,1] * 2 + [2,1,1,2,2],
                ([StrumStyle.NORMAL] * 3 + [StrumStyle.NO_HIT]) * 2 + 
                [StrumStyle.NORMAL, StrumStyle.NO_HIT, StrumStyle.NORMAL, StrumStyle.NORMAL] +
                [StrumStyle.NORMAL] * 4
            ),
            riff_chord_spans
        ),
        riff_measure,
        RhythmicChordSpan(
            Rhythm(
                [1,1,1,1] * 3 + [1,1,1,1],
                ([StrumStyle.NORMAL] * 3 + [StrumStyle.NO_HIT]) * 2 +
                [StrumStyle.NORMAL, StrumStyle.NO_HIT, StrumStyle.NORMAL, StrumStyle.NORMAL] +
                [StrumStyle.NORMAL] * 4
            ),
            [ChordSpan(16,Chord.power_chord(GuitarString.A5, 4))]
        )
    ]
}, Lyrics("""\
hämarast lagedast asulast torman
kiiresti teisiti vahvasti välja
tuttavalt ustavalt tuntavalt kuulen
sügaval pinnapeal kõikjal on juured\
""", (salm_main_durations + salm_alt_durations) * 2))

CHORUS = Segment("REFRÄÄN", {
    RHYTHM: [
        
    ]
}, Lyrics("", []))

TOPELT_CHORUS = Segment("REFRÄÄN", {
    RHYTHM: [

    ]
}, Lyrics("", []))

END = Segment("END", {
    RHYTHM: [
        
    ]
})

SONG = Song("Ilmutus", [
    INTRO,
    RIFF,
    SALM_1,
    CHORUS,
    RIFF,
    SALM_2,
    TOPELT_CHORUS,
    END
])