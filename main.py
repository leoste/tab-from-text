from song.jahe import SONG as JAHE
from song.song4243 import SONG as SONG_4243
from song.viirastus import SONG as VIIRASTUS
from TabRenderer import render_tab

render_tab(SONG_4243, "tabs/4243/guitar_tab")
render_tab(JAHE, "tabs/jahe/guitar_tab")
render_tab(VIIRASTUS, "tabs/viirastus/guitar_tab")