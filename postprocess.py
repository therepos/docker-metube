import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileMovedEvent
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB
from mutagen.mp4 import MP4, MP4Cover

WATCH_DIR = "/music"
COVER_PATH = "/cover.png"

class Handler(FileSystemEventHandler):
    def on_moved(self, event: FileMovedEvent):
        dest = event.dest_path
        if not dest.lower().endswith((".mp3", ".m4a")):
            return

        print(f"📦 Final file moved in: {dest}")
        time.sleep(1)  # Ensure file is finalized
        self.process(dest)

    def process(self, path):
        print(f"🎯 Processing: {path}")
        name = os.path.basename(path)
        if " - " not in name:
            print(f"⚠️ Skipping invalid filename: {name}")
            return

        artist, title = name.rsplit(" - ", 1)
        title = title.rsplit(".", 1)[0]

        try:
            if path.endswith(".mp3"):
                audio = MP3(path)
                audio.delete()
                audio.save()
                tags = ID3(path)
                tags["TIT2"] = TIT2(encoding=3, text=title)
                tags["TPE1"] = TPE1(encoding=3, text=artist)
                tags["TALB"] = TALB(encoding=3, text="MeTube")
                with open(COVER_PATH, "rb") as img:
                    tags.add(APIC(mime="image/png", type=3, desc="Cover", data=img.read()))
                tags.save()
                print("✅ MP3 metadata + cover set.")

            elif path.endswith(".m4a"):
                audio = MP4(path)
                audio["\xa9nam"] = [title]
                audio["\xa9ART"] = [artist]
                audio["\xa9alb"] = ["MeTube"]
                with open(COVER_PATH, "rb") as f:
                    audio["covr"] = [MP4Cover(f.read(), imageformat=MP4Cover.FORMAT_PNG)]
                audio.save()
                print("✅ M4A metadata + cover set.")

        except Exception as e:
            print(f"❌ Failed to process {path}: {e}")

if __name__ == "__main__":
    print("🚀 Starting postprocessor (on file move)...")
    observer = Observer()
    handler = Handler()
    observer.schedule(handler, WATCH_DIR, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
