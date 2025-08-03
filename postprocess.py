#!/usr/bin/env python3

import subprocess
import os
import time
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, APIC

WATCH_DIR = "/downloads"
COVER_IMAGE = "/app/cover.png"

def strip_metadata(filepath):
    temp = filepath + ".tmp"
    os.system(f'ffmpeg -y -i "{filepath}" -map_metadata -1 -c copy "{temp}" && mv "{temp}" "{filepath}"')

def inject_metadata(filepath):
    try:
        audio = MP3(filepath, ID3=ID3)
        audio.delete()
        audio.add_tags()

        title = os.path.splitext(os.path.basename(filepath))[0]
        artist = "Unknown"
        album = "My Album"

        audio["TIT2"] = TIT2(encoding=3, text=title)
        audio["TALB"] = TALB(encoding=3, text=album)
        audio["TPE1"] = TPE1(encoding=3, text=artist)
        audio["TPE2"] = TPE2(encoding=3, text=artist)

        with open(COVER_IMAGE, "rb") as img:
            audio["APIC"] = APIC(
                encoding=3,
                mime="image/png",
                type=3,
                desc="Cover",
                data=img.read()
            )

        audio.save()
        print(f"Processed: {filepath}")
    except Exception as e:
        print(f"Failed to process {filepath}: {e}")

def main():
    print(f"Watching {WATCH_DIR} for new files...")
    while True:
        try:
            result = subprocess.run(
                ["inotifywait", "-e", "close_write", "--format", "%w%f", WATCH_DIR],
                capture_output=True,
                text=True,
            )
            path = result.stdout.strip()
            if path.endswith((".mp3", ".m4a", ".mp4")):
                time.sleep(1)  # wait for write to fully finish
                strip_metadata(path)
                inject_metadata(path)
        except Exception as e:
            print("Watcher error:", e)
            time.sleep(5)

if __name__ == "__main__":
    main()
