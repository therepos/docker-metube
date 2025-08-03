import os, time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC

WATCH_DIR = "/music"
COVER_PATH = "/cover.png"

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith(".mp3"):
            self.process(event.src_path)

    def process(self, path):
        name = os.path.basename(path)
        if " - " not in name: return
        artist, title = name.rsplit(" - ", 1)
        title = title.rsplit(".mp3", 1)[0]

        audio = EasyID3(path)
        audio.clear()
        audio["title"] = title
        audio["artist"] = artist
        audio["album"] = "MeTube"
        audio.save()

        id3 = ID3(path)
        id3.delall("APIC")
        with open(COVER_PATH, "rb") as img:
            id3.add(APIC(mime="image/png", type=3, desc="Cover", data=img.read()))
        id3.save()

if __name__ == "__main__":
    obs = Observer()
    obs.schedule(Handler(), WATCH_DIR, recursive=False)
    obs.start()
    try:
        while True: time.sleep(10)
    except KeyboardInterrupt:
        obs.stop()
    obs.join()
