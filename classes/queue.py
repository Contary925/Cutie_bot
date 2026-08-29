import random

class Queue():
    def __init__(self):
        self.songs = []
        self.current_song = None
    def add(self, song):
        self.songs.append(song)
    def next(self):
        if self.songs:
            return self.songs.pop(0)
        return None
    def is_empty(self):
        return len(self.songs) == 0
    def set_current(self, song):
        self.current_song = song
    def show(self):
        songs_list=""
        index = 0
        if self.current_song is not None:
            index = 1
            songs_list += f"{index}. **{self.current_song['title']}**\n"
        for song in self.songs:
            index += 1
            if index>20:
                songs_list += "Cannot display more songs...\nPlease refrain from creating very long queues as streaming URLs may expire over time."
                break
            songs_list += f"{index}. **{song['title']}**\n"
        return songs_list
    def shuffle(self):
        random.shuffle(self.songs)
    def push(self, index):
        song = self.songs.pop(index-2)
        self.songs.insert(0, song)
    def repeat_current(self):
        song = self.current_song
        self.songs.insert(0, song)
    def insert(self, index, song):
        self.songs.insert(index, song)