import os
import sys
import shutil
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC, error
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4, MP4Cover

COVER_PATH = "/postprocess/cover.png"
DEST_FOLDER = "/downloads"
DEFAULT_ALBUM = ""  # Use blank instead of "Unknown"

WHITELIST_ID3 = {"title", "artist", "album", "albumartist"}
WHITELIST_MP4 = ["\xa9nam", "\xa9ART", "aART", "\xa9alb"]

def clean_mp3(file_path):
    print(f"Processing MP3: {file_path}")
    audio = MP3(file_path, ID3=EasyID3)

    title = audio.get("title", [""])[0]
    artist = audio.get("artist", [""])[0]
    album = audio.get("album", [""])[0] or DEFAULT_ALBUM

    # Remove all EasyID3 metadata
    audio.delete()

    audio["title"] = title
    audio["artist"] = artist
    audio["albumartist"] = artist
    audio["album"] = album
    audio.save()

    # Reload with full ID3 tag control
    audio = MP3(file_path, ID3=ID3)
    try:
        audio.add_tags()
    except error:
        pass

    # Remove all existing cover images
    for tag in list(audio.tags.keys()):
        if tag.startswith("APIC") or tag not in WHITELIST_ID3:
            del audio.tags[tag]

    # Add new embedded cover
    with open(COVER_PATH, "rb") as img:
        audio.tags.add(
            APIC(
                encoding=3,
                mime="image/png",
                type=3,
                desc="Cover",
                data=img.read()
            )
        )

    audio.save()

    # Rename to title
    new_name = f"{title}.mp3" if title else os.path.basename(file_path)
    dest_path = os.path.join(DEST_FOLDER, new_name)
    if file_path != dest_path:
        if os.path.exists(dest_path):
            os.remove(dest_path)
        shutil.move(file_path, dest_path)

def clean_m4a(file_path):
    print(f"Processing M4A: {file_path}")
    audio = MP4(file_path)

    title = audio.tags.get("\xa9nam", [""])[0]
    artist = audio.tags.get("\xa9ART", [""])[0]
    album = audio.tags.get("\xa9alb", [""])[0] if "\xa9alb" in audio.tags else DEFAULT_ALBUM

    # Clear all tags
    audio.clear()

    # Set only desired metadata
    audio["\xa9nam"] = title
    audio["\xa9ART"] = artist
    audio["aART"] = artist
    audio["\xa9alb"] = album

    # Remove old covers, then set custom one
    with open(COVER_PATH, "rb") as f:
        cover_data = f.read()
        audio["covr"] = [MP4Cover(cover_data, imageformat=MP4Cover.FORMAT_PNG)]

    audio.save()

    new_name = f"{title}.m4a" if title else os.path.basename(file_path)
    dest_path = os.path.join(DEST_FOLDER, new_name)
    if file_path != dest_path:
        if os.path.exists(dest_path):
            os.remove(dest_path)
        shutil.move(file_path, dest_path)

def process(file_path):
    if file_path.endswith(".mp3"):
        clean_mp3(file_path)
    elif file_path.endswith(".m4a"):
        clean_m4a(file_path)
    else:
        print(f"Unsupported file type: {file_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        if os.path.exists(input_file):
            process(input_file)
        else:
            print(f"File not found: {input_file}")
    else:
        print("Usage: python3 postprocess.py <file>")
