import os
import sys
import shutil
import tempfile
import subprocess
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TPE2, APIC
from mutagen.mp4 import MP4, MP4Cover

COVER_PATH = "/postprocess/cover.png"
DEST_FOLDER = "/downloads"
DEFAULT_ALBUM = ""

def clean_mp3(file_path):
    print(f"Cleaning MP3: {file_path}")

    # Load metadata before clearing
    audio = MP3(file_path)
    id3 = ID3(file_path)
    title = id3.get("TIT2", TIT2(encoding=3, text=[""])).text[0]
    artist = id3.get("TPE1", TPE1(encoding=3, text=[""])).text[0]

    # Strip embedded metadata (ID3v1/v2/extra frames) via ffmpeg
    temp_output = tempfile.mktemp(suffix=".mp3")
    subprocess.run([
        "ffmpeg", "-y", "-i", file_path,
        "-map", "0:a", "-c:a", "copy", "-f", "mp3", temp_output
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    shutil.move(temp_output, file_path)

    # Re-tag using clean ID3
    audio = MP3(file_path, ID3=ID3)
    audio.delete()

    audio["TIT2"] = TIT2(encoding=3, text=title)
    audio["TPE1"] = TPE1(encoding=3, text=artist)
    audio["TALB"] = TALB(encoding=3, text=DEFAULT_ALBUM)
    audio["TPE2"] = TPE2(encoding=3, text=artist)

    with open(COVER_PATH, "rb") as img:
        audio["APIC"] = APIC(
            encoding=3,
            mime="image/png",
            type=3,
            desc="Cover",
            data=img.read()
        )

    audio.save()

    new_name = f"{title}.mp3" if title else os.path.basename(file_path)
    dest_path = os.path.join(DEST_FOLDER, new_name)
    if file_path != dest_path:
        if os.path.exists(dest_path):
            os.remove(dest_path)
        shutil.move(file_path, dest_path)

def clean_m4a(file_path):
    print(f"Cleaning M4A: {file_path}")

    audio = MP4(file_path)

    # Extract safe fallback values
    title = audio.tags.get("\xa9nam", [""])[0]
    artist = audio.tags.get("\xa9ART", [""])[0]

    # 🔥 Hard reset: remove all metadata and cover
    audio.clear()
    audio.tags = {}

    # Apply only desired fields
    audio["\xa9nam"] = title
    audio["\xa9ART"] = artist
    audio["aART"] = artist
    audio["\xa9alb"] = DEFAULT_ALBUM

    # Inject custom cover
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