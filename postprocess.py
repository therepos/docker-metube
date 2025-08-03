import os
import time
from mutagen import File
from mutagen.id3 import ID3, APIC, ID3NoHeaderError, error as ID3Error
from mutagen.mp4 import MP4Cover
from mutagen.flac import Picture, FLAC
from mutagen.mp3 import MP3
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
<<<<<<< HEAD
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB
from mutagen.mp4 import MP4, MP4Cover
from mutagen.flac import FLAC, Picture
=======
>>>>>>> 3c27266f9f40c75a973b1302d5abacdc824508a7

WATCH_DIR = "/music"
COVER_PATH = "/cover.png"

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        path = event.src_path
        ext = path.lower()
        if not any(ext.endswith(x) for x in [".mp3", ".m4a", ".mp4", ".flac"]):
            return
<<<<<<< HEAD
        if ".temp" in path or ".part" in path:
            print(f"⏳ Skipping temporary file: {path}")
=======
        if ".temp" in ext or ".part" in ext:
            print(f"⏳ Skipping temporary file: {path}")
>>>>>>> 3c27266f9f40c75a973b1302d5abacdc824508a7
            return

        print(f"Detected new file: {path}")

<<<<<<< HEAD
=======
        # Wait for write to complete
>>>>>>> 3c27266f9f40c75a973b1302d5abacdc824508a7
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
<<<<<<< HEAD
        title = title.rsplit(".", 1)[0]
        ext = path.lower()
=======
        title = title.rsplit(".", 1)[0]
>>>>>>> 3c27266f9f40c75a973b1302d5abacdc824508a7

        ext = path.lower()
        try:
<<<<<<< HEAD
            if ext.endswith(".mp3"):
                audio = MP3(path)
                audio.delete()
                audio.save()
                tags = ID3(path)
                tags.delall("APIC")
                tags["TIT2"] = TIT2(encoding=3, text=title)
                tags["TPE1"] = TPE1(encoding=3, text=artist)
                tags["TALB"] = TALB(encoding=3, text="MeTube")
                with open(COVER_PATH, "rb") as img:
                    tags.add(APIC(mime="image/png", type=3, desc="Cover", data=img.read()))
                tags.save()
                print("✅ MP3 updated.")
=======
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
>>>>>>> 3c27266f9f40c75a973b1302d5abacdc824508a7

<<<<<<< HEAD
            elif ext.endswith(".m4a") or ext.endswith(".mp4"):
                audio = MP4(path)
                for key in list(audio.keys()):
                    del audio[key]
                audio["\xa9nam"] = [title]
                audio["\xa9ART"] = [artist]
                audio["\xa9alb"] = ["MeTube"]
                with open(COVER_PATH, "rb") as f:
                    audio["covr"] = [MP4Cover(f.read(), imageformat=MP4Cover.FORMAT_PNG)]
                audio.save()
                print("✅ M4A/MP4 updated.")
=======
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
>>>>>>> 3c27266f9f40c75a973b1302d5abacdc824508a7

<<<<<<< HEAD
            elif ext.endswith(".flac"):
                audio = FLAC(path)
                audio.clear()
                audio["title"] = title
                audio["artist"] = artist
                audio["album"] = "MeTube"
                picture = Picture()
                picture.type = 3
                picture.mime = "image/png"
                picture.desc = "Cover"
                picture.data = open(COVER_PATH, "rb").read()
                audio.clear_pictures()
                audio.add_picture(picture)
                audio.save()
                print("✅ FLAC updated.")
=======
            elif ext.endswith(".flac"):
                audio = FLAC(path)
                audio.clear()
                audio["title"] = title
                audio["artist"] = artist
                audio["album"] = "MeTube"
>>>>>>> 3c27266f9f40c75a973b1302d5abacdc824508a7

<<<<<<< HEAD
=======
                image = Picture()
                image.type = 3
                image.mime = "image/png"
                image.desc = "Cover"
                image.data = open(COVER_PATH, "rb").read()
                audio.clear_pictures()
                audio.add_picture(image)
                audio.save()
                print("✅ FLAC updated.")

>>>>>>> 3c27266f9f40c75a973b1302d5abacdc824508a7
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
