import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC

WATCH_DIR = "/music"
COVER_PATH = "/cover.png"

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith(".mp3"):
            print(f"Detected new file: {event.src_path}")
            self.process(event.src_path)

    def process(self, path):
        print(f"Processing: {path}")
        name = os.path.basename(path)
        if " - " not in name:
            print("❌ Skipping: invalid filename format.")
            return

        artist, title = name.rsplit(" - ", 1)
        title = title.rsplit(".mp3", 1)[0]

        try:
            audio = EasyID3(path)
            audio.clear()
        except Exception:
            audio = EasyID3()
        audio["title"] = title
        audio["artist"] = artist
        audio["album"] = "MeTube"
        audio.save(path)

        try:
            id3 = ID3(path)
            id3.delall("APIC")
            with open(COVER_PATH, "rb") as img:
                id3.add(APIC(mime="image/png", type=3, desc="Cover", data=img.read()))
            id3.save(path)
            print("✅ Cover injected.")
        except Exception as e:
            print(f"❌ Failed to inject cover: {e}")

if __name__ == "__main__":
    print("🎵 Starting postprocessor...")
    observer = Observer()
    handler = Handler()
    observer.schedule(handler, WATCH_DIR, recursive=False)

    # Initial scan
    for f in os.listdir(WATCH_DIR):
        if f.endswith(".mp3"):
            handler.process(os.path.join(WATCH_DIR, f))

    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
