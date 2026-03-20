"""Title page rendering — separate from tab rendering."""
from PIL import ImageDraw
from tabfromtext.song.Song import Song
from tabfromtext.render.ImageFactory import new_title_page_image
import tabfromtext.render.LayoutUtils as lu


def render_title_page(song: Song, num_columns: int = 2):
    sections = [(seg.title, seg.lyrics.text if seg.lyrics is not None else None)
                for seg in song.segments]
    if not sections:
        return None

    img, draw = new_title_page_image()
    img_w_px  = img.width
    img_h_px  = img.height

    margin_px     = lu.margin_left_px
    title_line_h  = int(lu.px(lu.cfg.fonts.title_pt)  * 1.4)
    lyrics_line_h = int(lu.px(lu.cfg.fonts.lyrics_pt) * 1.4)
    section_gap   = lyrics_line_h
    top_pad_px    = lu.px(lu.cfg.page.top_margin_pt * 0.5)

    title_w = draw.textbbox((0, 0), song.title, font=lu.title_font)[2]
    draw.text(((img_w_px - title_w) // 2, top_pad_px), song.title,
              fill="black", font=lu.title_font)
    columns_top_y = top_pad_px + title_line_h * 2

    if song.description is not None:
        for desc_line in song.description.splitlines():
            draw.text((margin_px, columns_top_y), desc_line,
                      fill="black", font=lu.lyrics_font)
            columns_top_y += lyrics_line_h
        columns_top_y += section_gap

    usable_w   = img_w_px - 2 * margin_px
    col_gap    = margin_px
    col_w      = (usable_w - col_gap * (num_columns - 1)) // num_columns
    col_starts = [margin_px + i * (col_w + col_gap) for i in range(num_columns)]
    col_height = img_h_px - columns_top_y

    def section_height(title, lyrics) -> int:
        h = title_line_h
        if lyrics:
            h += len(lyrics.splitlines()) * lyrics_line_h
        return h + section_gap

    columns: list[list] = [[] for _ in range(num_columns)]
    col_used = [0] * num_columns
    col_idx  = 0
    for title, lyrics in sections:
        sh = section_height(title, lyrics)
        if col_used[col_idx] + sh > col_height and col_idx < num_columns - 1:
            col_idx += 1
        columns[col_idx].append((title, lyrics))
        col_used[col_idx] += sh

    for c_idx, col_sections in enumerate(columns):
        x = col_starts[c_idx]
        y = columns_top_y
        for title, lyrics in col_sections:
            draw.text((x, y), title, fill="black", font=lu.title_font)
            y += title_line_h
            if lyrics:
                for line in lyrics.splitlines():
                    draw.text((x, y), line, fill="black", font=lu.lyrics_font)
                    y += lyrics_line_h
            y += section_gap

    return img