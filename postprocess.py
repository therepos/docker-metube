import sys
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.id3 import ID3, APIC, TIT2, TALB, TPE1, TPE2
from mutagen.easymp4 import EasyMP4

def clean_mp3(file):
    audio = MP3(file, ID3=ID3)
    audio.delete()
    audio.save()
    audio["TIT2"] = TIT2(encoding=3, text="Title")
    audio["TALB"] = TALB(encoding=3, text="Album")
    audio["TPE1"] = TPE1(encoding=3, text="Artist")
    audio["TPE2"] = TPE2(encoding=3, text="Artist")
    with open("cover.png", "rb") as img:
        audio.tags.add(APIC(mime="image/png", type=3, desc=u"Cover", data=img.read()))
    audio.save()

def clean_m4a(file):
    audio = EasyMP4(file)
    audio.clear()
    audio["title"] = ["Title"]
    audio["album"] = ["Album"]
    audio["artist"] = ["Artist"]
    audio["albumartist"] = ["Artist"]
    audio.save()
    audio = MP4(file)
    with open("cover.png", "rb") as img:
        audio["covr"] = [MP4Cover(img.read(), imageformat=MP4Cover.FORMAT_PNG)]
    audio.save()

file = sys.argv[1]
if file.endswith(".mp3"):
    clean_mp3(file)
elif file.endswith(".m4a"):
    clean_m4a(file)
