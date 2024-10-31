"""intefface module"""
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import pygame

from composition import Composition
from linked_list_item import LinkedListItem
from playlist import PlayList


def first_track():
    """Добавить первый трек в плейлист."""
    file_path = filedialog.askopenfilename(
        defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3"), ("All files", "*.*")]
    )
    comp = Composition(file_path)
    item = LinkedListItem(comp)
    if file_path:
        return item


def first_playlist():
    """Запрос имени плейлиста при первом включе"""
    playlist_name = None
    while playlist_name is None:
        playlist_name = simpledialog.askstring("",
                                               "Введите название своего первого плейлиста: ")
    item = first_track()
    return PlayList(playlist_name, item)


class PlayerGUI:
    """Интерфейс приложения"""

    def __init__(self, master):
        self.master = master
        self.master.title("Музыкальный плеер")
        self.playlist = first_playlist()
        self.all_playlists = [self.playlist]

        # Кнопки
        self.add_button = tk.Button(master, text="Добавить трек", command=self.add_track)
        self.add_button.pack()

        self.play_button = tk.Button(master, text="Play/Stop", command=self.play_stop)
        self.play_button.pack()

        self.next_button = tk.Button(master, text="Следующий трек", command=self.next_track)
        self.next_button.pack()

        self.prev_button = tk.Button(master, text="Предыдущий трек", command=self.previous_track)
        self.prev_button.pack()

        self.add_button = tk.Button(master, text="Добавить плейлист", command=self.add_playlist)
        self.add_button.pack()

        self.add_button = tk.Button(master, text="Удалить плейлист", command=self.delete_playlist)
        self.add_button.pack()

        self.add_button = tk.Button(master, text="Удалить трек", command=self.delete_track)
        self.add_button.pack()

        # Лейблы
        self.playlist_label = tk.Label(master, text=f"Плейлист: {self.playlist.name}")
        self.playlist_label.pack()

        self.track_label = tk.Label(master, text="Трек: ")
        self.track_label.pack()

        self.playlist_frame = tk.Frame(master)
        self.playlist_frame.pack()

        # Список плейлистов
        self.playlist_list = tk.Listbox(self.playlist_frame, selectmode="extended")
        self.playlist_list.pack(side="left", fill="both", expand=False)

        # Список треков
        self.track_list = tk.Listbox(self.playlist_frame, selectmode="extended")
        self.track_list.pack(side="right", fill="both", expand=False)

        # Обновление списка треков и плейлистов
        self.update_track_list()
        self.update_playlist_list()

        # Обработка выбора трека в списке
        self.track_list.bind("<<ListboxSelect>>", self.select_track)
        self.playlist_list.bind("<<ListboxSelect>>", self.select_playlist)

        pygame.init()
        self.master.after(0, self.check_for_music_end)

    def add_track(self):
        """Добавить трек в плейлист."""
        file_path = filedialog.askopenfilename(
            defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3"), ("All files", "*.*")]
        )
        if file_path:
            self.playlist.add_track(file_path)
            self.update_track_list()

    def delete_track(self):
        """Удалить текущий трек."""
        if self.playlist.current_item:
            self.playlist.remove(self.playlist.current_item.track)
            # Обновление текущего трека, если удаленный трек был текущим
            pygame.mixer.music.stop()
            self.playlist.current_item = self.playlist.first_item \
                if self.playlist.first_item else None
            self.update_track_list()
            self.update_track_label()

        else:
            messagebox.showerror("Ошибка", "Трек не выбран!")

    def play_stop(self):
        """Play/Stop текущий трек."""
        self.playlist.play_stop()
        if pygame.mixer.music.get_busy():
            self.play_button.config(text="Stop")
        else:
            self.play_button.config(text="Play")

    def next_track(self):
        """Перейти к следующему треку."""
        self.playlist.next_track()
        self.update_track_selection()
        self.update_track_label()

    def previous_track(self):
        """Перейти к предыдущему треку."""
        self.playlist.previous_track()
        self.update_track_selection()
        self.update_track_label()

    def update_track_list(self):
        """Обновить список треков в Listbox."""
        self.track_list.delete(0, tk.END)
        for i, track in enumerate(self.playlist.get_track_list()):
            self.track_list.insert(tk.END, str(track.title) + " - " + str(track.artist))
            if self.playlist.current_item and track == self.playlist.current_item.track.file_path:
                self.track_list.selection_set(i)

    def select_track(self, event):
        """Обработать выбор трека в Listbox."""
        selection = self.track_list.curselection()
        if selection:
            track_index = selection[0]
            self.playlist.set_current_track(track_index)
            self.update_track_label()
            if pygame.mixer.get_busy():
                self.play_button.config(text="Play")
            else:
                self.play_button.config(text="Stop")

    def update_track_selection(self):
        """Обновить выделение в Listbox, чтобы соответствовало текущему треку."""
        self.track_list.selection_clear(0, tk.END)
        for i, track in enumerate(self.playlist.get_track_list()):
            if self.playlist.current_item and track.file_path == self.playlist.current_item.track.file_path:
                self.track_list.selection_set(i)
                break

    def add_playlist(self):
        """Добавить плейлист."""
        playlist_name = simpledialog.askstring("", "Введите названия для нового плейлиста: ")
        item = first_track()
        self.all_playlists.append(PlayList(name=playlist_name, first_item=item))
        self.update_playlist_list()

    def delete_playlist(self):
        """Удалить плейлист."""
        if len(self.all_playlists) == 1:
            messagebox.showerror("Так нельзя!", "У вас должен остаться хотя бы один плейлист :(")
            return 0
        pygame.mixer.music.stop()
        self.all_playlists.remove(self.playlist)
        self.playlist = self.all_playlists[0]
        self.update_track_list()
        self.update_track_label()
        self.update_playlist_list()
        self.update_playlist_label()

    def update_playlist_list(self):
        """Обновить список треков в Listbox."""
        self.playlist_list.delete(0, tk.END)
        for playlist in self.all_playlists:
            self.playlist_list.insert(tk.END, playlist.name)

    def select_playlist(self, event):
        """Обработать выбор трека в Listbox."""
        selection = self.playlist_list.curselection()
        if selection:
            playlist_index = selection[0]
            self.playlist = self.all_playlists[playlist_index]
            pygame.mixer.music.stop()
            self.update_track_list()
            self.update_playlist_label()

    def update_track_label(self):
        """Обновить лейбл с названием текущего трека."""
        if self.playlist.current:
            track_name = self.playlist.current.title
            if not track_name:
                track_name = self.playlist.current.file_path
            self.track_label.config(text=f"Трек: {track_name}")
        else:
            self.track_label.config(text="Трек: ")

    def update_playlist_label(self):
        """Обновление лейбл с названием текущего плейлиста."""
        self.playlist_label.config(text=f"Плейлист: {self.playlist.name}")

    def check_for_music_end(self):
        """проверка на концовку песни"""
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT + 1:
                self.next_track()
        self.master.after(100, self.check_for_music_end)

    # def move_track_up(self):
    #     selected_index = self.track_list.curselection()
    #     if selected_index:
    #         index = selected_index[0]
    #         if index > 0:
    #             self.playlist.move_track(index, index - 1)
    #             # self.track_list.selection_set(index - 1)
    #             self.update_track_list()
    #             self.update_track_selection()
    #
    #         else:
    #             print("Трек уже находится вверху.")


root = tk.Tk()
root.geometry('600x400+200+100')
player_gui = PlayerGUI(root)
root.mainloop()
