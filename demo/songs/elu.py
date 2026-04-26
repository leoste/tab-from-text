from tabfromtext.song.Lyrics import Lyrics
from tabfromtext.song.RhythmicChordSpanList import RhythmicChordSpanList
from tabfromtext.song.ChordSpan import ChordSpan
from tabfromtext.song.Chord import Chord
from tabfromtext.song.Rhythm import Rhythm
from tabfromtext.song.Segment import Segment
from tabfromtext.song.GuitarString import E6, A5, D4, G3, B2, E1
from tabfromtext.song.StrumStyle import StrumStyle
from tabfromtext.song.RepeatingChordSpan import RepeatingChordSpan
from tabfromtext.song.Song import Song

RHYTHM = "Rhythm"
BASS = "Bass"
LEAD = "Lead"

rhythm_vahe_parts = [
    RhythmicChordSpanList(
        Rhythm(
            [1] * 14 + [2] +
            [1] * 8 + [1,2,1,2,2],
            [StrumStyle.NORMAL] * 8 +
            [
                StrumStyle.NORMAL, StrumStyle.NORMAL,
                StrumStyle.MUTED, StrumStyle.NORMAL,
                StrumStyle.MUTED, StrumStyle.MUTED,
            ] +
            [StrumStyle.NORMAL] * 2 +
            [StrumStyle.NORMAL] * 16
        ),
        [
            ChordSpan(8, Chord.power_chord(E6, 7)),
            ChordSpan(8, Chord.power_chord(E6, 6)),
            ChordSpan(4, Chord.power_chord(A5, 6)),
            ChordSpan(4, Chord.power_chord(E6, 6)),
            ChordSpan(6, Chord.power_chord(A5, 6)),
            ChordSpan(2, Chord.power_chord(E6, 7))
        ] * 2
    )
]

bass_vahe_parts = [
    RepeatingChordSpan(1, Chord.single_note(E6, 7), 8),
    RepeatingChordSpan(1, Chord.single_note(E6, 6), 8),
    RepeatingChordSpan(1, Chord.single_note(A5, 6), 4),
    RepeatingChordSpan(1, Chord.single_note(E6, 6), 4),
    RepeatingChordSpan(1, Chord.single_note(A5, 6), 4),
    RepeatingChordSpan(1, Chord.single_note(E6, 7), 3),
    RepeatingChordSpan(1, Chord.single_note(A5, 6))
] * 2

rhythm_salm_first_parts = [
    RepeatingChordSpan(1, Chord.single_note(E6, 6), 4),
    RepeatingChordSpan(1, Chord.power_chord(E6, 7), 3),
    RepeatingChordSpan(1, Chord.power_chord(E6, 6)),
    RepeatingChordSpan(1, Chord.single_note(E6, 7), 4),
    RepeatingChordSpan(1, Chord.power_chord(E6, 7), 3),
    RepeatingChordSpan(1, Chord.power_chord(E6, 6)),
]

rhythm_salm_parts = rhythm_salm_first_parts + [
    RepeatingChordSpan(1, Chord.single_note(A5, 6), 4),
    RepeatingChordSpan(1, Chord.power_chord(A5, 6)),
    RepeatingChordSpan(1, Chord.single_note(A5, 6)),
    RepeatingChordSpan(1, Chord.power_chord(A5, 6)),
    RepeatingChordSpan(1, Chord.single_note(A5, 6)),
    RepeatingChordSpan(1, Chord.single_note(A5, 6), 4),
    RepeatingChordSpan(1, Chord.power_chord(E6, 7), 3),
    RepeatingChordSpan(1, Chord.power_chord(E6, 6)),
] + rhythm_salm_first_parts + [
    RepeatingChordSpan(1, Chord(None, None, None, 13, 11, 11), 8),
    RepeatingChordSpan(1, Chord.power_chord(E6, 11)),
    RepeatingChordSpan(1, Chord(None, None, None, None, 11, 11)),
    RepeatingChordSpan(1, Chord.power_chord(E6, 11)),
    RepeatingChordSpan(1, Chord(None, None, None, None, 11, 11)),
    RepeatingChordSpan(1, Chord.power_chord(E6, 11), 3),
    RepeatingChordSpan(1, Chord(None, None, None, None, 11, 11)),
]

bass_salm_first_parts = [
    RepeatingChordSpan(1, Chord.single_note(E6, 6), 6),
    RepeatingChordSpan(1, Chord.single_note(E6, 7)),
    RepeatingChordSpan(1, Chord.single_note(E6, 6)),
    RepeatingChordSpan(1, Chord.single_note(E6, 7), 7),
    RepeatingChordSpan(1, Chord.single_note(E6, 6)),
    RepeatingChordSpan(1, Chord.single_note(A5, 6), 8),
]

bass_salm_parts = bass_salm_first_parts + [
    RepeatingChordSpan(1, Chord.single_note(A5, 6), 6),
    RepeatingChordSpan(1, Chord.single_note(E6, 7)),
    RepeatingChordSpan(1, Chord.single_note(E6, 6))
] + bass_salm_first_parts + [    
    RepeatingChordSpan(2, Chord.single_note(A5, 9)),
    RepeatingChordSpan(2, Chord.single_note(E6, 6)),
    RepeatingChordSpan(1, Chord.single_note(E6, 6)),
    RepeatingChordSpan(1, Chord.single_note(D4, 3)),
    RepeatingChordSpan(1, Chord.single_note(D4, 4), 2),
]

rhythm_ref_parts = [
    RhythmicChordSpanList(
        Rhythm(
            [2, 1,1,1,1,1,1] +
            [1,1,1,1,1,1,1,1] * 3,
            [StrumStyle.NORMAL] * 8 +
            ([StrumStyle.NORMAL] * 5 + [StrumStyle.NO_HIT, StrumStyle.NORMAL, StrumStyle.NO_HIT]) * 3
        ),
        [
            ChordSpan(8, Chord.power_chord(E6, 2)),
            ChordSpan(4, Chord.power_chord(E6, 7)),
            ChordSpan(8, Chord.power_chord(E6, 6)),
            ChordSpan(8, Chord.power_chord(A5, 6)),
            ChordSpan(4, Chord.power_chord(E6, 6))
        ] * 2
    )
]

lead_ref_parts = [
    RhythmicChordSpanList(
        Rhythm([8, 4, 4, 4, 4, 4, 4]),
        [
            ChordSpan(8, Chord.power_chord(E6, 2)),
            ChordSpan(4, Chord.power_chord(E6, 7)),
            ChordSpan(8, Chord.power_chord(E6, 6)),
            ChordSpan(8, Chord.power_chord(A5, 6)),
            ChordSpan(4, Chord.power_chord(E6, 6))
        ] * 2
    )
]

lead_double_ref_parts = [
    RhythmicChordSpanList(
        Rhythm([8, 4, 4, 4, 4, 4, 4]),
        [
            ChordSpan(8, Chord.power_chord(E6, 2)),
            ChordSpan(4, Chord.power_chord(E6, 7)),
            ChordSpan(8, Chord.power_chord(E6, 6)),
            ChordSpan(8, Chord.power_chord(A5, 6)),
            ChordSpan(4, Chord.power_chord(E6, 6)),
            ChordSpan(8, Chord.power_chord(E6, 2)),
            ChordSpan(4, Chord.power_chord(E6, 7)),
            ChordSpan(8, Chord.power_chord(E6, 6)),
            ChordSpan(8, Chord.power_chord(A5, 6))
        ]
    ),
    RepeatingChordSpan(2, Chord.power_chord(E6, 6)),
    RepeatingChordSpan(1, Chord.single_note(A5, 9), 2),
    RepeatingChordSpan(14, Chord.single_note(A5, 9)),
    RepeatingChordSpan(1, Chord.single_note(D4, 8), 2),
    RepeatingChordSpan(14, Chord.single_note(D4, 8)),
    RepeatingChordSpan(1, Chord.single_note(A5, 9), 2),
    RepeatingChordSpan(16, Chord.single_note(A5, 9)),
    RhythmicChordSpanList(
        Rhythm([4]),
        [
            ChordSpan(4, Chord.power_chord(E6, 6)),
            ChordSpan(8, Chord.power_chord(A5, 6)),
            ChordSpan(4, Chord.power_chord(E6, 6))
        ]
    )
]

bass_ref_parts = [
    RepeatingChordSpan(1, Chord.single_note(D4, 4), 8),
    RepeatingChordSpan(1, Chord.single_note(E6, 7), 4),
    RepeatingChordSpan(1, Chord.single_note(E6, 6), 8),
    RepeatingChordSpan(1, Chord.single_note(A5, 6), 8),
    RepeatingChordSpan(1, Chord.single_note(E6, 6), 4)
] * 2

bass_ref_double = [
    RepeatingChordSpan(1, Chord.single_note(D4, 4), 8),
    RepeatingChordSpan(1, Chord.single_note(E6, 7), 4),
    RepeatingChordSpan(1, Chord.single_note(E6, 6), 8),
    RepeatingChordSpan(1, Chord.single_note(A5, 6), 8),
    RepeatingChordSpan(1, Chord.single_note(E6, 6), 4),
    RepeatingChordSpan(1, Chord.single_note(D4, 4), 8),
    RepeatingChordSpan(1, Chord.single_note(E6, 7), 4),
    RepeatingChordSpan(1, Chord.single_note(E6, 6), 8),
    RepeatingChordSpan(1, Chord.single_note(A5, 6), 4),
    RepeatingChordSpan(8, None)
]

rhythm_outro_parts = [
    RhythmicChordSpanList(
        Rhythm([1]),
        [
            ChordSpan(6, Chord.power_chord(A5, 6)),
            ChordSpan(2, Chord.power_chord(E6, 4)),
            ChordSpan(4, Chord.power_chord(E6, 6)),
            ChordSpan(1, Chord.power_chord(E6, 1)),
            ChordSpan(1, Chord.power_chord(E6, 2)),
            ChordSpan(1, Chord.power_chord(A5, 2)),
            ChordSpan(1, Chord.power_chord(A5, 1)),
            ChordSpan(4, Chord.power_chord(A5, 1)),
            ChordSpan(4, Chord.power_chord(E6, 6)),
            ChordSpan(3, Chord.power_chord(E6, 7)),
            ChordSpan(1, Chord.power_chord(E6, 6)),
            ChordSpan(3, Chord.power_chord(A5, 2)),
            ChordSpan(1, Chord.power_chord(A5, 1)),
        ] * 4
    )
]

bass_outro_parts = [
    RepeatingChordSpan(1, Chord.single_note(E6, 7), 8),
    RepeatingChordSpan(1, Chord.single_note(E6, 6), 8),
    RepeatingChordSpan(1, Chord.single_note(A5, 6), 4),
    RepeatingChordSpan(1, Chord.single_note(G3, 8), 4),
    RepeatingChordSpan(1, Chord.single_note(A5, 6), 4),
    RepeatingChordSpan(1, Chord.single_note(E6, 7), 3),
    RepeatingChordSpan(1, Chord.single_note(A5, 6))
] * 4

lead_vahe_parts = [
    RepeatingChordSpan(1, Chord.single_note(A5, 6), 6),
    RepeatingChordSpan(1, Chord.single_note(E6, 1), 2),
    RepeatingChordSpan(1, Chord.single_note(E6, 6), 4),
    RepeatingChordSpan(1, Chord.single_note(E6, 1)),
    RepeatingChordSpan(1, Chord.single_note(E6, 2)),
    RepeatingChordSpan(1, Chord.single_note(A5, 2)),
    RepeatingChordSpan(1, Chord.single_note(A5, 1)),
    RepeatingChordSpan(1, Chord.single_note(A5, 1), 4),
    RepeatingChordSpan(1, Chord.single_note(E6, 6), 4),
    RepeatingChordSpan(1, Chord.single_note(E6, 7), 3),
    RepeatingChordSpan(1, Chord.single_note(E6, 6)),
    RepeatingChordSpan(1, Chord.single_note(A5, 2), 3),
    RepeatingChordSpan(1, Chord.single_note(A5, 6)),
] * 2

lead_outro_parts = [
    RepeatingChordSpan(1, Chord.single_note(A5, 6), 6),
    RepeatingChordSpan(1, Chord.single_note(E6, 4), 2),
    RepeatingChordSpan(1, Chord.single_note(E6, 6), 4),
    RepeatingChordSpan(1, Chord.single_note(E6, 1)),
    RepeatingChordSpan(1, Chord.single_note(E6, 2)),
    RepeatingChordSpan(1, Chord.single_note(A5, 2)),
    RepeatingChordSpan(1, Chord.single_note(A5, 1)),
    RepeatingChordSpan(1, Chord.single_note(A5, 1), 4),
    RepeatingChordSpan(1, Chord.single_note(E6, 6), 4),
    RepeatingChordSpan(1, Chord.single_note(E6, 7), 3),
    RepeatingChordSpan(1, Chord.single_note(E6, 6)),
    RepeatingChordSpan(1, Chord.single_note(A5, 2), 3),
    RepeatingChordSpan(1, Chord.single_note(A5, 1)),
] * 4

lead_salm_parts = [
    RepeatingChordSpan(8, Chord.single_note(E6, 6), 1, StrumStyle.VIBRATO),
    RepeatingChordSpan(8, None, 2),
    RepeatingChordSpan(3, None),
    RepeatingChordSpan(1, Chord.single_note(E6, 7), 5),
    RepeatingChordSpan(8, Chord.single_note(E6, 6), 1, StrumStyle.VIBRATO),
    RepeatingChordSpan(8, None),
    RepeatingChordSpan(6, None),
    RepeatingChordSpan(1, None),
    RepeatingChordSpan(1, Chord.single_note(A5, 6)),
    RepeatingChordSpan(2, Chord.single_note(A5, 9)),
    RepeatingChordSpan(2, Chord.single_note(E6, 6)),
    RepeatingChordSpan(1, Chord.single_note(E6, 6)),
    RepeatingChordSpan(1, Chord.single_note(D4, 3)),
    RepeatingChordSpan(1, Chord.single_note(D4, 4), 2),
]

VAHE = Segment("INTRO", {
    RHYTHM: rhythm_vahe_parts,
    BASS: bass_vahe_parts,
    LEAD: lead_vahe_parts
})

SALM_1 = Segment("1. SALM", {
    RHYTHM: rhythm_salm_parts,
    BASS: bass_salm_parts,
    LEAD: lead_salm_parts
}, Lyrics("""\
käest ta võttis sinult kõik
tema nimele on võit
juba ette määratud
tema jõud on vääratu
alla anda võid sa nüüd
mis sa ikka ennast müüd
roti moodi ringeldad
ruttu välja vingerda\
""", [
    1,1,1,1,0.5,1.5,2,
    1,1,1,1,0.5,1.5,2,
    1,1,1,1,1,1,2,
    1,1,1,1,1,1,2,
    1,1,1,1,1,1,2,
    1,1,1,1,1,1,2,
    1,1,1,1,1,1,2,
    1,1,1,1,1,1,2
]))

SALM_2 = Segment("2. SALM", {
    RHYTHM: rhythm_salm_parts,
    BASS: bass_salm_parts,
    LEAD: lead_salm_parts
}, Lyrics("""\
vaba hingena nüüd elad
sinu päralt maailmapärand
seda võid sa uskuda
tagant kõik sind kiidavad
aga tegusid ei tee
mitte ükski vaba mees
oma kodus vinguvad
telost porri vaatavad\
""", [
    1,1,1,1,1,1,0.5,1.5,
    1,1,1,1,1,1,0.5,1.5,
    1,1,1,1,1,1,2,
    1,1,1,1,1,1,2,
    1,1,1,1,1,1,2,
    1,1,1,1,1,1,2,
    1,1,1,1,1,1,2,
    1,1,1,1,1,1,2
]))

REF = Segment("REFRÄÄN", {
    RHYTHM: rhythm_ref_parts,
    BASS: bass_ref_parts,
    LEAD: lead_ref_parts,
}, Lyrics("""\
see on elu meie moodi
kui ei meeldi mine poodi
kaasa riiulilt sa haara
pudel džinni, too meil taara\
""", [
    2,2,2,2,2,2,2,2,
    2,2,2,2,2,2,2,2,
    2,2,2,2,2,2,2,2,
    2,2,2,2,2,2,2,2
]))

REF_2X = Segment("TOPELT REFRÄÄN", {
    RHYTHM: rhythm_ref_parts * 2,
    BASS: bass_ref_parts + bass_ref_double,
    LEAD: lead_double_ref_parts
}, Lyrics("""\
see on elu meie moodi
kui ei meeldi mine poodi
kaasa riiulilt sa haara
pudel džinni, too meil taara
see on elu meie moodi
kui ei meeldi mine poodi
kaasa riiulilt sa haara
pudel džinni, too meil taara\
""", [
    2,2,2,2,2,2,2,2,
    2,2,2,2,2,2,2,2,
    2,2,2,2,2,2,2,2,
    2,2,2,2,2,2,2,2
]*2))

OUTRO = Segment("OUTRO", {
    RHYTHM: rhythm_outro_parts,
    BASS: bass_outro_parts,
    LEAD: lead_outro_parts
}, Lyrics("""\
DŽINNITAARA
DŽINNITAARA
""", [
    1,1,1,29,
    1,1,1,1
], 20))

END = Segment("LÕPP", {
    RHYTHM: [
        RepeatingChordSpan(2, Chord.single_note(E6, 6), 1, StrumStyle.SLIDE),
        RepeatingChordSpan(6, Chord.single_note(E6, 18), 1, StrumStyle.NORMAL),
        RepeatingChordSpan(2, Chord.power_chord(E6, 6)),
        RepeatingChordSpan(6, None)
    ],
    BASS: [
        RepeatingChordSpan(8, Chord.single_note(D4, 8)),
        RepeatingChordSpan(2, Chord.single_note(E6, 6)),
        RepeatingChordSpan(6, None)
    ]
})

SONG = Song("Elu meie moodi", [
    VAHE,
    SALM_1,
    REF,
    VAHE,
    SALM_2,
    REF_2X,
    OUTRO,
    END
])