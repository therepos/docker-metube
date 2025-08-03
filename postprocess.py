import sys, os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, TALB, TPE1, TPE2, ID3NoHeaderError
from mutagen.mp4 import MP4, MP4Cover
from mutagen.easymp4 import EasyMP4

def parse_metadata(file):
    name = os.path.splitext(os.path.basename(file))[0]
    parts = name.split(" - ")
    return {
        "artist": parts[0] if len(parts) > 0 else "",
        "album": parts[1] if len(parts) > 1 else "",
        "title": parts[2] if len(parts) > 2 else name
    }

def process_mp3(file, meta):
    try:
        audio = MP3(file, ID3=ID3)
        audio.delete()
    except ID3NoHeaderError:
        audio = MP3(file)
        audio.add_tags()

    audio["TIT2"] = TIT2(encoding=3, text=meta["title"])
    audio["TALB"] = TALB(encoding=3, text=meta["album"])
    audio["TPE1"] = TPE1(encoding=3, text=meta["artist"])
    audio["TPE2"] = TPE2(encoding=3, text=meta["artist"])
    with open("/cover.png", "rb") as img:
        audio.tags.add(APIC(mime="image/png", type=3, desc=u"Cover", data=img.read()))
    audio.save()

def process_m4a(file, meta):
    # Clear all atoms
    audio = MP4(file)
    audio.clear()
    audio["\xa9nam"] = [meta["title"]]
    audio["\xa9alb"] = [meta["album"]]
    audio["\xa9ART"] = [meta["artist"]]
    audio["aART"] = [meta["artist"]]
    with open("/cover.png", "rb") as img:
        audio["covr"] = [MP4Cover(img.read(), imageformat=MP4Cover.FORMAT_PNG)]
    audio.save()

file = sys.argv[1]
meta = parse_metadata(file)

if file.endswith(".mp3"):
    process_mp3(file, meta)
elif file.endswith(".m4a"):
    process_m4a(file, meta)
