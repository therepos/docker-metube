import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from mutagen import File
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, APIC

WATCH_DIR = "/mnt/music"
COVER_PATH = "/app/cover.png"

def clean_and_tag(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in [".mp3", ".m4a", ".mp4"]:
        return

    # Strip metadata with ffmpeg
    temp = file_path + ".tmp"
    os.system(f"ffmpeg -y -i \"{file_path}\" -map_metadata -1 -c copy \"{temp}\" && mv \"{temp}\" \"{file_path}\"")

    # Add new metadata with mutagen
    try:
        audio = MP3(file_path, ID3=ID3)
        audio.delete()
        audio.add_tags()

        title = os.path.splitext(os.path.basename(file_path))[0]
        artist = "Unknown"
        album = "My Album"

        audio["TIT2"] = TIT2(encoding=3, text=title)
        audio["TALB"] = TALB(encoding=3, text=album)
        audio["TPE1"] = TPE1(encoding=3, text=artist)
        audio["TPE2"] = TPE2(encoding=3, text=artist)  # album artist

        with open(COVER_PATH, "rb") as img:
            audio["APIC"] = APIC(
                encoding=3,
                mime="image/png",
                type=3,
                desc="Cover",
                data=img.read()
            )

        audio.save()
        print(f"Processed: {file_path}")

    except Exception as e:
        print(f"Failed: {file_path} - {e}")

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            time.sleep(1)
            clean_and_tag(event.src_path)

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(Handler(), WATCH_DIR, recursive=False)
    observer.start()
    print("Watching for new files...")
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
