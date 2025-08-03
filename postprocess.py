import sys, os
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4, MP4Cover
from mutagen.id3 import ID3, APIC, TIT2, TALB, TPE1, TPE2
from mutagen.easymp4 import EasyMP4

def parse_metadata(filename):
    name = os.path.splitext(os.path.basename(filename))[0]
    parts = name.split(" - ")
    artist = parts[0] if len(parts) > 0 else ""
    album = parts[1] if len(parts) > 1 else ""
    title = parts[2] if len(parts) > 2 else name
    return {"artist": artist, "album": album, "title": title}

def process_mp3(file, meta):
    audio = MP3(file, ID3=ID3)
    audio.delete()
    audio.save()
    audio["TIT2"] = TIT2(encoding=3, text=meta["title"])
    audio["TALB"] = TALB(encoding=3, text=meta["album"])
    audio["TPE1"] = TPE1(encoding=3, text=meta["artist"])
    audio["TPE2"] = TPE2(encoding=3, text=meta["artist"])
    with open("/app/cover.png", "rb") as img:
        audio.tags.add(APIC(mime="image/png", type=3, desc="Cover", data=img.read()))
    audio.save()

def process_m4a(file, meta):
    audio = EasyMP4(file)
    audio.clear()
    audio["title"] = [meta["title"]]
    if meta["album"]: audio["album"] = [meta["album"]]
    if meta["artist"]:
        audio["artist"] = [meta["artist"]]
        audio["albumartist"] = [meta["artist"]]
    audio.save()
    audio = MP4(file)
    with open("/app/cover.png", "rb") as img:
        audio["covr"] = [MP4Cover(img.read(), imageformat=MP4Cover.FORMAT_PNG)]
    audio.save()

file = sys.argv[1]
meta = parse_metadata(file)
if file.endswith(".mp3"):
    process_mp3(file, meta)
elif file.endswith(".m4a"):
    process_m4a(file, meta)
