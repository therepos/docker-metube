import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileMovedEvent
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
from mutagen.mp4 import MP4, MP4Cover

WATCH_DIR = "/music"
COVER_PATH = "/cover.png"

class Handler(FileSystemEventHandler):
    def on_moved(self, event: FileMovedEvent):
        dest = event.dest_path
        if not dest.lower().endswith((".mp3", ".m4a")):
            return

        print(f"📦 Final file moved in: {dest}")
        time.sleep(1)
        self.process(dest)

    def process(self, path):
        print(f"🎯 Processing: {path}")
        try:
            if path.endswith(".mp3"):
                # Remove all tags and add custom cover
                audio = MP3(path)
                audio.delete()
                audio.save()
                tags = ID3()
                with open(COVER_PATH, "rb") as img:
                    tags.add(APIC(mime="image/png", type=3, desc="Cover", data=img.read()))
                tags.save(path)
                print("✅ MP3: cover injected.")

            elif path.endswith(".m4a"):
                audio = MP4(path)
                # Remove all tags
                for k in list(audio.keys()):
                    del audio[k]
                with open(COVER_PATH, "rb") as f:
                    audio["covr"] = [MP4Cover(f.read(), imageformat=MP4Cover.FORMAT_PNG)]
                audio.save()
                print("✅ M4A: cover injected.")

        except Exception as e:
            print(f"❌ Failed to process {path}: {e}")

if __name__ == "__main__":
    print("🚀 Starting postprocessor (simplified)...")
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
