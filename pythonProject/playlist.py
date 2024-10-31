from tkinter import filedialog

from linked_list import LinkedList
from composition import Composition
import pygame

from linked_list_item import LinkedListItem


class PlayList(LinkedList):
    def __init__(self, name, first_item):
        super().__init__(first_item)
        self.current_item = None
        self.name = name

    def play_all(self):
        """Начать проигрывать все треки, начиная с item."""
        if self.current_item is None:
            raise ValueError("Не выбран начальный трек")
        pygame.mixer.init()
        pygame.mixer.music.load(self.current_item.track.file_path)
        pygame.mixer.music.play()
        pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)
        print(f"Играет трек: {self.current_item.track.title}")

    def next_track(self):
        """Перейти к следующему треку."""
        if self.current_item is None:
            raise ValueError("Не выбран начальный трек")
        if self.current_item.next_item:
            self.current_item = self.current_item.next_item
        else:
            self.current_item = self.first_item

        self.play_all()

    def previous_track(self):
        """Перейти к предыдущему треку."""
        if self.current_item is None:
            raise ValueError("Не выбран начальный трек")

        previous = None
        current = self.first_item
        while current:
            if current == self.current_item:
                if previous:
                    self.current_item = previous
                    self.play_all()
                    return
                else:
                    self.current_item = self.last()
                    self.play_all()
                    return
            previous = current
            current = current.next_item

    @property
    def current(self):
        """Получить текущий трек."""
        if self.current_item is None:
            return None
        return self.current_item.track

    def add_track(self, file_path):
        """Добавить трек в плейлист."""
        composition = Composition(file_path)
        self.append(composition)
        print(f"Трек '{file_path}' добавлен в плейлист {self.name}")

    def play_stop(self):
        """Play/Stop текущий трек."""
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
        else:
            if self.current_item:
                pygame.mixer.music.unpause()
            else:
                print("Не выбран начальный трек")

    def set_current_track(self, track_index):
        """Установить текущий трек по индексу."""
        if track_index >= 0:
            current = self.first_item
            for i in range(track_index):
                current = current.next_item
            self.current_item = current
            self.play_all()

    def get_track_list(self):
        """Получить список треков."""
        track_list = []
        current = self.first_item
        while current:
            track_list.append(current.track)
            current = current.next_item
        return track_list
