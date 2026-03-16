from tabfromtext.song.Chord import Chord
from tabfromtext.song.ChordSpan import ChordSpan
from tabfromtext.song.GuitarString import GuitarString
from tabfromtext.song.Lyrics import Lyrics
from tabfromtext.song.Rhythm import Rhythm
from tabfromtext.song.RhythmicChordSpan import RhythmicChordSpan
from tabfromtext.song.Segment import Segment
from tabfromtext.song.Song import Song
from tabfromtext.song.StrumStyle import StrumStyle
from tabfromtext.song.StrummedChordSpan import StrummedChordSpan

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

RIFF = Segment("RIFF", {
    RHYTHM: [RhythmicChordSpan(
        Rhythm(
            [1,1,1,1] * 3 + [2,2],
            [StrumStyle.NORMAL] * 16
       ),
       riff_chord_spans
    )] * 4
})

salm_rhythm = Rhythm(
    [1,1,1,1] * 4,
    ([StrumStyle.NORMAL] * 3 + [StrumStyle.NO_HIT]) * 3 + [StrumStyle.NORMAL, StrumStyle.NO_HIT] * 2
)

salm_measure = RhythmicChordSpan(
    salm_rhythm,
    riff_chord_spans
)

salm_main_durations = [1,1,2,1,1,2,1,1,2,2,2]
salm_alt_durations = [1,1,2,1,1,2,2,1,1,2,2]

SALM_1 = Segment("1. SALM", {
    RHYTHM: [salm_measure] * 3 + [
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
        salm_measure,
        RhythmicChordSpan(
            Rhythm(
                [1,1,1,1] * 2 + [2,1,1,2,2],
                ([StrumStyle.NORMAL] * 3 + [StrumStyle.NO_HIT]) * 2 + 
                [StrumStyle.NORMAL, StrumStyle.NO_HIT, StrumStyle.NORMAL, StrumStyle.NORMAL] +
                [StrumStyle.NORMAL] * 4
            ),
            riff_chord_spans
        ),
        salm_measure,
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

rhythm_first_measures = [
    StrummedChordSpan(1, Chord.power_chord(GuitarString.A5, 4),8),
    StrummedChordSpan(1, Chord.power_chord(GuitarString.A5, 7),2),
    StrummedChordSpan(1, Chord.power_chord(GuitarString.A5, 6),1),
    StrummedChordSpan(1, Chord.power_chord(GuitarString.A5, 7),2),
    StrummedChordSpan(1, Chord.power_chord(GuitarString.A5, 6),1),
    StrummedChordSpan(1, Chord.power_chord(GuitarString.A5, 7),1),
    StrummedChordSpan(1, Chord.power_chord(GuitarString.A5, 6),1),]

rhythm_chorus = rhythm_first_measures + [
    StrummedChordSpan(1, Chord.power_chord(GuitarString.E6, 5),8),
    StrummedChordSpan(1, Chord.power_chord(GuitarString.A5, 4),2),
    StrummedChordSpan(1, Chord.power_chord(GuitarString.A5, 4),1,StrumStyle.MUTED),
    StrummedChordSpan(2, Chord.power_chord(GuitarString.A5, 2),1),
    StrummedChordSpan(1, Chord.power_chord(GuitarString.A5, 2),3)        
] + rhythm_first_measures + [
    StrummedChordSpan(2, Chord.power_chord(GuitarString.E6, 5),2),
    StrummedChordSpan(1, Chord.power_chord(GuitarString.E6, 5),3),
    StrummedChordSpan(9, Chord.power_chord(GuitarString.E6, 4))
]

CHORUS = Segment("REFRÄÄN", {
    RHYTHM: rhythm_chorus
}, Lyrics("""\
otse minu ees
on maailma-asja paigutus
tunnen vastust enda sees
see on ilmutus
""", [
    2,2,1,2,4,
    1, 2,2,2,2, 1,2,5,
    2,2,2,2, 2,1,5,
    2,2, 1,2,5
], 4))

TOPELT_CHORUS = Segment("TOPELT REFRÄÄN", {
    RHYTHM: rhythm_first_measures + [
        StrummedChordSpan(1, Chord.power_chord(GuitarString.E6, 5),8),
        StrummedChordSpan(1, Chord.power_chord(GuitarString.A5, 4),2),
        StrummedChordSpan(1, Chord.power_chord(GuitarString.A5, 4),1,StrumStyle.MUTED),
        StrummedChordSpan(2, Chord.power_chord(GuitarString.A5, 2),1),
        StrummedChordSpan(1, Chord.power_chord(GuitarString.A5, 2),3)        
    ] + rhythm_first_measures + [
        StrummedChordSpan(2, Chord.power_chord(GuitarString.E6, 5),2),
        StrummedChordSpan(1, Chord.power_chord(GuitarString.E6, 5),3),
        StrummedChordSpan(5, Chord.power_chord(GuitarString.E6, 4)),
        StrummedChordSpan(4, Chord.power_chord(GuitarString.E6, 4)),
    ] + rhythm_chorus
}, Lyrics("""\
otse minu ees
on maailma-asja paigutus
tunnen vastust enda sees
see on ilmutus
otse minu ees
on maailma-asja paigutus
tunnen vastust enda sees
see on ilmutus
""", [
    2,2,1,2,4,
    1, 2,2,2,2, 1,2,5,
    2,2,2,2, 2,1,5,
    2,2, 1,2,13
] + [
    2,2,1,2,4,
    1, 2,2,2,2, 1,2,5,
    2,2,2,2, 2,1,5,
    2,2, 1,2,5
], 4))

END = Segment("END", {
    RHYTHM: [
        StrummedChordSpan(4, Chord.power_chord(GuitarString.E6, 9)),
        StrummedChordSpan(4, Chord.power_chord(GuitarString.E6, 7)),
        StrummedChordSpan(1, Chord.power_chord(GuitarString.E6, 5)),
        StrummedChordSpan(2, Chord.power_chord(GuitarString.E6, 5)),
        StrummedChordSpan(3, Chord.power_chord(GuitarString.E6, 4)),
        StrummedChordSpan(2, Chord.power_chord(GuitarString.E6, 4)),
    ] + [
        StrummedChordSpan(1, Chord.power_chord(GuitarString.E6, 9),2),
        StrummedChordSpan(1, Chord.power_chord(GuitarString.E6, 9),2, StrumStyle.MUTED),
        StrummedChordSpan(1, Chord.power_chord(GuitarString.E6, 7),2),
        StrummedChordSpan(1, Chord.power_chord(GuitarString.E6, 7),2, StrumStyle.MUTED),
        StrummedChordSpan(1, Chord.power_chord(GuitarString.E6, 5),2),
        StrummedChordSpan(1, Chord.power_chord(GuitarString.E6, 5),1, StrumStyle.MUTED),
        StrummedChordSpan(2, Chord.power_chord(GuitarString.E6, 4)),
        StrummedChordSpan(1, Chord.power_chord(GuitarString.E6, 4),3),
    ] * 3 + [
        StrummedChordSpan(1, Chord.power_chord(GuitarString.E6, 9),2),
        StrummedChordSpan(1, Chord.power_chord(GuitarString.E6, 9),2, StrumStyle.MUTED),
        StrummedChordSpan(1, Chord.power_chord(GuitarString.E6, 7),2),
        StrummedChordSpan(1, Chord.power_chord(GuitarString.E6, 7),2, StrumStyle.MUTED),
        StrummedChordSpan(8, Chord.power_chord(GuitarString.E6, 4))
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