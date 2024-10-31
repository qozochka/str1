from mutagen.mp3 import MP3


class Composition:
    def __init__(self, file_path):
        self.file_path = file_path
        self.title = MP3(file_path).get("TIT2")
        self.artist = MP3(file_path).get("TPE1")
