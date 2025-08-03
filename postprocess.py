import os
import time
from mutagen import File
from mutagen.id3 import ID3, APIC, ID3NoHeaderError, error as ID3Error
from mutagen.mp4 import MP4Cover
from mutagen.flac import Picture, FLAC
from mutagen.mp3 import MP3
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCH_DIR = "/music"
COVER_PATH = "/cover.png"

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        path = event.src_path
        ext = path.lower()
        if not any(ext.endswith(x) for x in [".mp3", ".m4a", ".mp4", ".flac"]):
            return
        if ".temp" in ext or ".part" in ext:
            print(f"⏳ Skipping temporary file: {path}")
            return

        print(f"Detected new file: {path}")

        # Wait for write to complete
        for _ in range(10):
            try:
                before = os.path.getsize(path)
                time.sleep(1)
                after = os.path.getsize(path)
                if before == after and before > 0:
                    break
            except FileNotFoundError:
                time.sleep(1)

        self.process(path)

    def process(self, path):
        print(f"Processing: {path}")
        name = os.path.basename(path)
        if " - " not in name:
            print("❌ Skipping: invalid filename format.")
            return
        artist, title = name.rsplit(" - ", 1)
        title = title.rsplit(".", 1)[0]

        ext = path.lower()
        try:
            if ext.endswith(".mp3"):
                audio = MP3(path)
                audio.delete()
                audio.save()
                tags = ID3(path)
                tags.delall("APIC")
                tags.add(APIC(mime="image/png", type=3, desc="Cover", data=open(COVER_PATH, "rb").read()))
                tags["TIT2"] = title
                tags["TPE1"] = artist
                tags["TALB"] = "MeTube"
                tags.save()
                print("✅ MP3 updated.")

            elif ext.endswith(".m4a") or ext.endswith(".mp4"):
                audio = File(path)
                audio.delete()
                audio["\xa9nam"] = title
                audio["\xa9ART"] = artist
                audio["\xa9alb"] = "MeTube"
                with open(COVER_PATH, "rb") as f:
                    cover_data = f.read()
                    audio["covr"] = [MP4Cover(cover_data, imageformat=MP4Cover.FORMAT_PNG)]
                audio.save()
                print("✅ M4A/MP4 updated.")

            elif ext.endswith(".flac"):
                audio = FLAC(path)
                audio.clear()
                audio["title"] = title
                audio["artist"] = artist
                audio["album"] = "MeTube"

                image = Picture()
                image.type = 3
                image.mime = "image/png"
                image.desc = "Cover"
                image.data = open(COVER_PATH, "rb").read()
                audio.clear_pictures()
                audio.add_picture(image)
                audio.save()
                print("✅ FLAC updated.")

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
