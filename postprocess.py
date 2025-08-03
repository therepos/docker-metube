import os
import time
from mutagen.easyid3 import EasyID3
from mutagen.mp4 import MP4, MP4Cover
from mutagen.id3 import ID3, APIC
import inotify.adapters

WATCH_DIR = "/downloads"
COVER_PATH = "/app/cover.png"

def process_file(path):
    ext = os.path.splitext(path)[1].lower()
    base = os.path.splitext(os.path.basename(path))[0]

    if ext == ".mp3":
        try:
            audio = EasyID3(path)
        except Exception:
            audio = EasyID3()
        audio.clear()
        audio['title'] = base
        audio['artist'] = base
        audio['album'] = base
        audio['albumartist'] = base
        audio.save()

        id3 = ID3(path)
        id3.delall("APIC")
        with open(COVER_PATH, "rb") as img:
            id3['APIC'] = APIC(
                encoding=3,
                mime='image/png',
                type=3,
                desc='Cover',
                data=img.read()
            )
        id3.save()

    elif ext == ".m4a":
        audio = MP4(path)
        audio.clear()
        audio["\xa9nam"] = [base]
        audio["\xa9ART"] = [base]
        audio["\xa9alb"] = [base]
        audio["aART"] = [base]
        with open(COVER_PATH, "rb") as img:
            audio["covr"] = [MP4Cover(img.read(), imageformat=MP4Cover.FORMAT_PNG)]
        audio.save()

def watch():
    i = inotify.adapters.Inotify()
    i.add_watch(WATCH_DIR)

    for event in i.event_gen(yield_nones=False):
        (_, type_names, path, filename) = event
        if "CLOSE_WRITE" in type_names:
            fpath = os.path.join(path, filename)
            if fpath.endswith((".mp3", ".m4a")):
                try:
                    process_file(fpath)
                except Exception as e:
                    print(f"Failed to process {fpath}: {e}")

if __name__ == "__main__":
    watch()
