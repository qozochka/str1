from linked_list import LinkedList
from composition import Composition
import pygame


class PlayList(LinkedList):
    def __init__(self, name):
        super().__init__()
        self.compositions = LinkedList()
        self.current_item = None
        self.name = name
        pygame.mixer.init()

    def play_all(self):
        """Начать проигрывать все треки, начиная с item."""
        if self.current_item is None:
            raise ValueError("Не выбран начальный трек")
        pygame.mixer.music.load(self.current_item.data)
        pygame.mixer.music.play()
        print(f"Играет трек: {self.current_item.data}")

    def next_track(self):
        """Перейти к следующему треку."""
        if self.current_item is None:
            raise ValueError("Не выбран начальный трек")
        if self.current_item.next:
            self.current_item = self.current_item.next
            pygame.mixer.music.load(self.current_item.data.file_path)
            pygame.mixer.music.play()
            print(f"Играет трек: {self.current_item.data.title}")
        else:
            print("Достигнут конец плейлиста")

    def previous_track(self):
        """Перейти к предыдущему треку."""
        if self.current_item is None:
            raise ValueError("Не выбран начальный трек")

        previous = None
        current = self.compositions.head
        while current:
            if current == self.current_item:
                if previous:
                    self.current_item = previous
                    pygame.mixer.music.load(self.current_item.data.file_path)
                    pygame.mixer.music.play()
                    print(f"Играет трек: {self.current_item.data.title}")
                    return
                else:
                    print("Достигнут начало плейлиста")
                    return
            previous = current
            current = current.next

    @property
    def current(self):
        """Получить текущий трек."""
        if self.current_item is None:
            return None
        return self.current_item.data

    def add_track(self, file_path, title="", artist=""):
        """Добавить трек в плейлист."""
        composition = Composition(file_path, title, artist)
        self.compositions.append(composition)
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
            current = self.compositions.head
            for i in range(track_index):
                current = current.next
            self.current_item = current
            pygame.mixer.music.load(self.current_item.data.file_path)
            pygame.mixer.music.play()

    def get_track_list(self):
        """Получить список треков."""
        track_list = []
        current = self.compositions.head
        while current:
            track_list.append(current.data.file_path)
            current = current.next
        return track_list



