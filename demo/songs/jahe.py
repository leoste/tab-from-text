from tabfromtext.song.Lyrics import Lyrics
from tabfromtext.song.RhythmicChordSpan import RhythmicChordSpan
from tabfromtext.song.ChordSpan import ChordSpan
from tabfromtext.song.Chord import Chord
from tabfromtext.song.Rhythm import Rhythm
from tabfromtext.song.Segment import Segment
from tabfromtext.song.GuitarString import GuitarString
from tabfromtext.song.StrumStyle import StrumStyle
from tabfromtext.song.Song import Song
from tabfromtext.song.StrummedChordSpan import StrummedChordSpan

RHYTHM = "Rhythm"
LEAD = "Lead"

CHORD_13_F = Chord.power_chord(GuitarString.E6, 13)
CHORD_13_C = Chord(None, None, None, 15, 13, 13)
CHORD_11_D_SHARP = Chord.power_chord(GuitarString.E6, 11)
CHORD_9_C_SHARP = Chord.power_chord(GuitarString.E6, 9)
CHORD_8_C = Chord.power_chord(GuitarString.E6, 8)
CHORD_6_A_SHARP = Chord.power_chord(GuitarString.E6, 6)
CHORD_4_G_SHARP = Chord.power_chord(GuitarString.E6, 4)
CHORD_2_F_SHARP = Chord.power_chord(GuitarString.E6, 2)
CHORD_1_F = Chord.power_chord(GuitarString.E6, 1)

DURATIONS_232 = [1,1,1,2,1,1,1]
INTRO_RHYTHM = Rhythm(
    [2,1,1,2,1,1] + DURATIONS_232,
    [StrumStyle.NORMAL] * 16
)

intro_parts = [
    RhythmicChordSpan(
        INTRO_RHYTHM,
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

SALM_RHYTHM = Rhythm(
    [1] * 16,
    [StrumStyle.PALM_MUTED] * 16
)

SALM_HALF_END_RHYTHM = Rhythm(
    DURATIONS_232 + [1] * 8,
    [StrumStyle.NORMAL] * 16
)

SALM_END_RHYTHM = Rhythm(
    DURATIONS_232 * 2,
    [StrumStyle.NORMAL] * 16
)

salm_parts = [
    RhythmicChordSpan(
        SALM_RHYTHM,
        [
            ChordSpan(16, CHORD_6_A_SHARP),
            ChordSpan(16, CHORD_4_G_SHARP),
            ChordSpan(16, CHORD_2_F_SHARP),
        ]
    ),
    RhythmicChordSpan(
        SALM_HALF_END_RHYTHM,
        [ ChordSpan(16, CHORD_1_F) ]
    ),
    RhythmicChordSpan(
        SALM_RHYTHM,
        [
            ChordSpan(16, CHORD_6_A_SHARP),
            ChordSpan(16, CHORD_4_G_SHARP),
            ChordSpan(16, CHORD_2_F_SHARP),
        ]
    ),
    RhythmicChordSpan(
        SALM_END_RHYTHM,
        [ ChordSpan(16, CHORD_1_F) ]
    )
]

CHORUS_FIRST_MEASURE_RHYTHM = Rhythm(
    [2] + [1] * 14,
    [StrumStyle.NORMAL] * 16
)

CHORUS_THIRD_MEASURE_RHYTHM = Rhythm(
        [1] * 16,
        [StrumStyle.NORMAL] * 16
)

CHORUS_SEVENTH_MEASURE_RHYTHM = Rhythm(
    [3,3,2,1,1,1,1,1,1,1,1],
    [StrumStyle.NORMAL] * 16
)

chorus_parts = [
        RhythmicChordSpan(
            CHORUS_FIRST_MEASURE_RHYTHM,
            [ ChordSpan(16, CHORD_9_C_SHARP) ]
        ),
        RhythmicChordSpan(
            CHORUS_THIRD_MEASURE_RHYTHM,
            [
                ChordSpan(16, CHORD_6_A_SHARP),
                ChordSpan(16, CHORD_4_G_SHARP)
            ],
        ),
        RhythmicChordSpan(
            CHORUS_SEVENTH_MEASURE_RHYTHM,
            [
                ChordSpan(9, CHORD_9_C_SHARP),
                ChordSpan(7, CHORD_8_C)
            ]
        )
    ] * 2

BREAK_LAST_MEASURE_RHYTHM = Rhythm(
    [1] * 8 + DURATIONS_232,
    [StrumStyle.NORMAL] * 16
)

breakdown_parts = [
    RhythmicChordSpan(
        Rhythm(
            [1] * 16,
            [StrumStyle.NORMAL] * 16
        ),
        [
            ChordSpan(16, CHORD_13_F),
            ChordSpan(4, CHORD_9_C_SHARP),
            ChordSpan(4, CHORD_8_C),
            ChordSpan(8, CHORD_9_C_SHARP),
            ChordSpan(16, CHORD_6_A_SHARP),
            ChordSpan(16, CHORD_8_C),
            ChordSpan(16, CHORD_13_F),
            ChordSpan(4, CHORD_9_C_SHARP),
            ChordSpan(4, CHORD_8_C),
            ChordSpan(8, CHORD_9_C_SHARP),
            ChordSpan(16, CHORD_6_A_SHARP)
        ]
    ),
    RhythmicChordSpan(
        BREAK_LAST_MEASURE_RHYTHM,
        [ ChordSpan(16, CHORD_8_C) ]
    ),
    RhythmicChordSpan(
        Rhythm(
            [ 
                2,
                2,
                4,
                8
            ],
            [
                StrumStyle.SLIDE,
                StrumStyle.SLIDE,
                StrumStyle.NORMAL,
                StrumStyle.NORMAL                
            ] +
            [ StrumStyle.NO_HIT ] * 12
        ),
        [
            ChordSpan(2, CHORD_8_C),
            ChordSpan(2, CHORD_13_F),
            ChordSpan(12, Chord.no_strings_hit_chord())
        ]
    )
]

end_parts = [
    RhythmicChordSpan(
        Rhythm(
            [1] * 8 + DURATIONS_232,
            [StrumStyle.NORMAL] * 16
        ),
        [
            ChordSpan(2, CHORD_13_F),
            ChordSpan(2, CHORD_13_C),
            ChordSpan(2, CHORD_13_F),
            ChordSpan(2, CHORD_13_C),
            ChordSpan(2, CHORD_13_F),
            ChordSpan(1, CHORD_13_C),
            ChordSpan(2, CHORD_13_F),
            ChordSpan(1, CHORD_13_F),
            ChordSpan(1, CHORD_13_C),
            ChordSpan(1, CHORD_13_C)
        ] * 3
    ),
    RhythmicChordSpan(
        Rhythm(
            [1] * 8 + [2,6],
            [ StrumStyle.NORMAL ] * 10 +
            [ StrumStyle.NO_HIT ] * 6
        ),
        [
            ChordSpan(2, CHORD_13_F),
            ChordSpan(2, CHORD_13_C),
            ChordSpan(6, CHORD_13_F),
            ChordSpan(6, Chord.no_strings_hit_chord())
        ]
    )
]

salm_1_lyrics = Lyrics("""\
sõpradena võime ju koos
minna sinna kuhu tahtnud hoos
aga tulla sealt ära me
vaid võhivõõrastena või-me\
""", [
    2,2,1,3,1,2,5,16,
    2,1,3,2,1,2,3,2,16,
    1,2,3,2,4,1,3,16,
    2,1,1,2,2,1,3,4,16
]
) 

salm_2_lyrics = Lyrics("""\
tuulega mul kõrvus kõlab noot
pilvedega toob ta miskit uut
aimasingi et nii minna võib
selguse see mulle pähe tõi\
""", [
    1,2,3,2,2,2,1,3,16,
    3,1,1,3,2,1,3,2,16,
    2,2,1,3,2,2,2,2,16,
    2,1,3,2,2,2,1,3,16
]
)

chorus_lyrics = Lyrics("""\
siiski ootan mina sinu järel
järgnen sulle kasvõi kui oleks hambad sul verel
tahan teada vaid et mis on su tahe
suhtlus tundub pikimööda täitsa meil jahe\
""", [
    2,2,2,2,1,3,1,3,1,15,
    2,2,2,2,2,2,2,1,1,2,4,2,1,6,1,
    3,3,2,2,2,1,1,1,1,16,
    2,2,2,2,3,1,3,1,2,4,2,1,7
])

lead_intro_section = [
    StrummedChordSpan(2, Chord.single_note(GuitarString.B2, 14)),
    StrummedChordSpan(1, Chord.single_note(GuitarString.B2, 14), 2),
    StrummedChordSpan(2, Chord.single_note(GuitarString.B2, 14), 2),
    
    StrummedChordSpan(2, Chord.single_note(GuitarString.B2, 13)),
    StrummedChordSpan(1, Chord.single_note(GuitarString.B2, 13), 2),
    StrummedChordSpan(2, Chord.single_note(GuitarString.B2, 13), 2),
]

lead_intro_first = (lead_intro_section + [
    StrummedChordSpan(3, Chord.single_note(GuitarString.G3, 15)),
    StrummedChordSpan(3, Chord.single_note(GuitarString.G3, 13)),
    StrummedChordSpan(1, Chord.single_note(GuitarString.G3, 13)),
    StrummedChordSpan(1, Chord.single_note(GuitarString.G3, 15)),
    StrummedChordSpan(8, Chord.single_note(GuitarString.G3, 13)),
])

lead_intro_second = (lead_intro_section + [
    StrummedChordSpan(3, Chord.single_note(GuitarString.G3, 11)),
    StrummedChordSpan(3, Chord.single_note(GuitarString.G3, 10)),
    StrummedChordSpan(1, Chord.single_note(GuitarString.G3, 10)),
    StrummedChordSpan(1, Chord.single_note(GuitarString.G3, 11)),
    StrummedChordSpan(8, Chord.single_note(GuitarString.G3, 10)),
])

lead_intro_third = (lead_intro_section + [
    StrummedChordSpan(3, Chord.single_note(GuitarString.G3, 15)),
    StrummedChordSpan(3, Chord.single_note(GuitarString.G3, 13)),
    StrummedChordSpan(2, Chord.single_note(GuitarString.G3, 15)),
    StrummedChordSpan(6, Chord.single_note(GuitarString.G3, 13)),
    StrummedChordSpan(2, Chord.single_note(GuitarString.G3, 13)),
])

lead_intro_last = [
    StrummedChordSpan(2, Chord.single_note(GuitarString.B2, 11)),
    StrummedChordSpan(1, Chord.single_note(GuitarString.B2, 11), 2),
    StrummedChordSpan(2, Chord.single_note(GuitarString.B2, 11)),
    StrummedChordSpan(2, Chord.single_note(GuitarString.B2, 13)),
    
    StrummedChordSpan(2, Chord.single_note(GuitarString.E1, 11)),
    StrummedChordSpan(1, Chord.single_note(GuitarString.E1, 11), 2),
    StrummedChordSpan(2, Chord.single_note(GuitarString.E1, 11), 2),
    
    StrummedChordSpan(2, Chord.single_note(GuitarString.E1, 13), 4),
    StrummedChordSpan(2, Chord.single_note(GuitarString.G3, 10), 4),
    
    StrummedChordSpan(1, Chord.single_note(GuitarString.G3, 10), 7),
    StrummedChordSpan(1, Chord.single_note(GuitarString.G3, 11)),    
    StrummedChordSpan(6, Chord.single_note(GuitarString.G3, 10), 1, StrumStyle.VIBRATO),
    StrummedChordSpan(2, Chord.no_strings_hit_chord())
]

lead_intro_parts = lead_intro_first + lead_intro_second + lead_intro_third + lead_intro_last

lead_vahe_first_repeat = [
    StrummedChordSpan(1, Chord.single_note(GuitarString.B2, 14)),
    StrummedChordSpan(1, Chord.single_note(GuitarString.G3, 15))
] * 8

lead_vahe_second_repeat = [
    StrummedChordSpan(1, Chord.single_note(GuitarString.B2, 13)),
    StrummedChordSpan(1, Chord.single_note(GuitarString.G3, 13))
] * 8

lead_vahe_first_inter = [
    StrummedChordSpan(1, Chord.single_note(GuitarString.G3, 11), 3),
    StrummedChordSpan(2, Chord.single_note(GuitarString.G3, 11)),
    StrummedChordSpan(1, Chord.single_note(GuitarString.G3, 11), 2),
    StrummedChordSpan(2, Chord.single_note(GuitarString.G3, 11)),
    StrummedChordSpan(1, Chord.single_note(GuitarString.G3, 11), 3),
    StrummedChordSpan(2, Chord.single_note(GuitarString.G3, 11), 2),
]

lead_vahe_second_inter = [
    StrummedChordSpan(1, Chord.single_note(GuitarString.G3, 10), 3),
    StrummedChordSpan(2, Chord.single_note(GuitarString.G3, 10)),
    StrummedChordSpan(1, Chord.single_note(GuitarString.G3, 10), 2),
    StrummedChordSpan(2, Chord.single_note(GuitarString.G3, 10)),
    StrummedChordSpan(1, Chord.single_note(GuitarString.G3, 10), 3),
    StrummedChordSpan(2, Chord.single_note(GuitarString.G3, 10), 2),
]

lead_vahe_parts = (lead_vahe_first_repeat + lead_vahe_first_inter + lead_vahe_second_repeat + lead_vahe_second_inter +
    lead_vahe_first_repeat + lead_vahe_first_inter + [
        StrummedChordSpan(1, Chord.single_note(GuitarString.B2, 11), 4),
        StrummedChordSpan(2, Chord.single_note(GuitarString.B2, 11)),
        StrummedChordSpan(2, Chord.single_note(GuitarString.B2, 13)),
        StrummedChordSpan(2, Chord.single_note(GuitarString.E1, 11)),
        StrummedChordSpan(1, Chord.single_note(GuitarString.E1, 11), 2),
        StrummedChordSpan(2, Chord.single_note(GuitarString.E1, 11), 2),
        
        StrummedChordSpan(3, Chord.single_note(GuitarString.G3, 11)),
        StrummedChordSpan(3, Chord.single_note(GuitarString.G3, 10)),
        StrummedChordSpan(1, Chord.single_note(GuitarString.G3, 10)),
        StrummedChordSpan(1, Chord.single_note(GuitarString.G3, 11)),
        StrummedChordSpan(6, Chord.single_note(GuitarString.G3, 11), 1, StrumStyle.VIBRATO),
        StrummedChordSpan(2, Chord.no_strings_hit_chord())
    ])

lead_solo_first_part = [
    StrummedChordSpan(2, Chord.single_note(GuitarString.B2, 13)),
    StrummedChordSpan(1, Chord.single_note(GuitarString.E1, 13), 2),
    StrummedChordSpan(2, Chord.single_note(GuitarString.E1, 13)),
    StrummedChordSpan(2, Chord.single_note(GuitarString.B2, 13)),
    StrummedChordSpan(3, Chord.single_note(GuitarString.E1, 13), 2),
    StrummedChordSpan(2, Chord.single_note(GuitarString.B2, 13))
]

lead_solo_parts = lead_solo_first_part + [    
    StrummedChordSpan(16, Chord.single_note(GuitarString.G3, 10), 1, StrumStyle.VIBRATO),
] + lead_solo_first_part + [
    StrummedChordSpan(16, Chord.single_note(GuitarString.G3, 12), 1, StrumStyle.VIBRATO),
] + lead_solo_first_part + [    
    StrummedChordSpan(16, Chord.single_note(GuitarString.G3, 10), 1, StrumStyle.VIBRATO),
] + lead_solo_first_part + [
    StrummedChordSpan(6, Chord.single_note(GuitarString.B2, 13)),
    StrummedChordSpan(2, Chord.single_note(GuitarString.G3, 12)),
    StrummedChordSpan(3, Chord.single_note(GuitarString.B2, 13)),
    StrummedChordSpan(5, Chord.single_note(GuitarString.G3, 12), 1, StrumStyle.VIBRATO),
    StrummedChordSpan(8, Chord.no_strings_hit_chord(), 2)
]

lead_end_first = [
    StrummedChordSpan(2, Chord.single_note(GuitarString.B2, 14)),
    StrummedChordSpan(1, Chord.single_note(GuitarString.B2, 14), 6),
    StrummedChordSpan(2, Chord.single_note(GuitarString.B2, 13)),
    StrummedChordSpan(1, Chord.single_note(GuitarString.B2, 13), 6),
]

lead_end_first_block = lead_end_first + [
    StrummedChordSpan(3, Chord.single_note(GuitarString.E1, 13), 2),
    StrummedChordSpan(2, Chord.single_note(GuitarString.B2, 11), 2),
    StrummedChordSpan(1, Chord.single_note(GuitarString.B2, 11), 6),
]

lead_end_second_block = lead_end_first + [    
    StrummedChordSpan(3, Chord.single_note(GuitarString.G3, 11), 2),
    StrummedChordSpan(2, Chord.single_note(GuitarString.G3, 11)),
    StrummedChordSpan(1, Chord.single_note(GuitarString.G3, 11)),
    StrummedChordSpan(1, Chord.single_note(GuitarString.G3, 10), 7),
]

lead_end_parts = (lead_end_first_block + lead_end_second_block) * 2

lead_chorus = [
    StrummedChordSpan(2, Chord.single_note(GuitarString.G3, 10), 2),
    StrummedChordSpan(1, Chord.single_note(GuitarString.G3, 10), 12),
    StrummedChordSpan(2, Chord.single_note(GuitarString.G3, 8), 7),
    StrummedChordSpan(1, Chord.single_note(GuitarString.G3, 8), 2),
    StrummedChordSpan(3, Chord.single_note(GuitarString.G3, 11), 2),
    StrummedChordSpan(2, Chord.single_note(GuitarString.G3, 11), 2),
    StrummedChordSpan(1, Chord.single_note(GuitarString.G3, 11)),
    StrummedChordSpan(2, Chord.single_note(GuitarString.G3, 10), 7),
] * 2

lead_salm = [
    StrummedChordSpan(8, Chord.no_strings_hit_chord(), 16)
]

lead_real_end_parts = [
    StrummedChordSpan(16, Chord.single_note(GuitarString.G3, 10), 1, StrumStyle.VIBRATO),
    StrummedChordSpan(8, Chord.no_strings_hit_chord(), 2)
]

lead_chorus_mute = [
    StrummedChordSpan(8, Chord.no_strings_hit_chord(), 16)
]

FIRST_INTRO = Segment("INTRO 1", {RHYTHM: intro_parts, LEAD: lead_intro_parts})
SECOND_INTRO = Segment("INTRO 2", {RHYTHM: intro_parts, LEAD: lead_vahe_parts})
SALM_1 = Segment("SALM", {RHYTHM: salm_parts, LEAD: lead_salm}, lyrics=salm_1_lyrics)
SALM_2 = Segment("SALM", {RHYTHM: salm_parts, LEAD: lead_salm}, lyrics=salm_2_lyrics)
CHORUS = Segment("REFRÄÄN", {RHYTHM: chorus_parts, LEAD: lead_chorus_mute}, lyrics=chorus_lyrics)
LAST_CHORUS = Segment("REFRÄÄN", {RHYTHM: chorus_parts, LEAD: lead_chorus}, lyrics=chorus_lyrics)
INSTRUMENTAL_CHORUS = Segment("INSTRUMENTAALNE REFRÄÄN", {RHYTHM: chorus_parts, LEAD: lead_end_parts})
BREAKDOWN = Segment("BREAKDOWN", {RHYTHM: breakdown_parts, LEAD: lead_solo_parts})
END = Segment("LÕPP", {RHYTHM: end_parts, LEAD: lead_real_end_parts})

SONG = Song("Jahe", [
    FIRST_INTRO,
    SALM_1,
    CHORUS,
    SECOND_INTRO,
    SALM_2,
    CHORUS,
    BREAKDOWN,
    LAST_CHORUS,
    INSTRUMENTAL_CHORUS,
    END,
])