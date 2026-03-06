import os
from PIL import Image
from object.Song import Song
from TabRenderer import render_song


def save_images(images: list[tuple[str, Image.Image]]) -> None:
    for file_path, img in images:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        img.save(file_path)
        print(f"Salvestatud: {file_path}")


def save_song(song: Song) -> None:
    images = render_song(song)
    save_images(images)