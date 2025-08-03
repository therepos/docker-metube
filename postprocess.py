import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
from mutagen.mp3 import MP3

WATCH_DIR = "/music"
COVER_PATH = "/cover.png"

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.src_path.endswith(".mp3"):
            return
        if ".temp" in event.src_path or ".part" in event.src_path:
            print(f"⏳ Skipping temporary file: {event.src_path}")
            return

        print(f"Detected new file: {event.src_path}")

        # Wait for file write to finish
        for _ in range(10):
            try:
                before = os.path.getsize(event.src_path)
                time.sleep(1)
                after = os.path.getsize(event.src_path)
                if before == after and before > 0:
                    break
            except FileNotFoundError:
                time.sleep(1)

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
            # Clear existing tags
            audio = MP3(path)
            audio.delete()
            audio.save()
            print("🧹 Metadata wiped.")

            tags = EasyID3(path)
            tags["title"] = title
            tags["artist"] = artist
            tags["album"] = "MeTube"
            tags.save()
            print("✅ ID3 tags set.")

            id3 = ID3(path)
            id3.delall("APIC")
            with open(COVER_PATH, "rb") as img:
                id3.add(APIC(mime="image/png", type=3, desc="Cover", data=img.read()))
            id3.save()
            print("✅ Cover injected.")

            # Confirm
            test = ID3(path)
            if any(k.startswith("APIC") for k in test.keys()):
                print("✅ Confirmed: cover embedded.")
            else:
                print("❌ Cover not found after saving.")

        except Exception as e:
            print(f"❌ Error processing {path}: {e}")

if __name__ == "__main__":
    print("🎵 Starting postprocessor...")
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
