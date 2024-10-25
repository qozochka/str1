import tkinter as tk
from tkinter import filedialog, simpledialog
from playlist import PlayList
import pygame


def first_playlist():
    playlist_name = None
    while playlist_name is None:
        playlist_name = simpledialog.askstring("",
                                               "Введите название своего первого плейлиста: ")
    return PlayList(playlist_name)


class PlayerGUI:
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

    def add_track(self):
        """Добавить трек в плейлист."""
        file_path = filedialog.askopenfilename(
            defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3"), ("All files", "*.*")]
        )
        if file_path:
            self.playlist.add_track(file_path)
            self.update_track_list()

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

    def previous_track(self):
        """Перейти к предыдущему треку."""
        self.playlist.previous_track()
        self.update_track_selection()

    def update_track_list(self):
        """Обновить список треков в Listbox."""
        self.track_list.delete(0, tk.END)
        for i, track in enumerate(self.playlist.get_track_list()):
            self.track_list.insert(tk.END, track)
            if self.playlist.current_item and track == self.playlist.current_item.data.file_path:
                self.track_list.selection_set(i)

    def select_track(self, event):
        """Обработать выбор трека в Listbox."""
        selection = self.track_list.curselection()
        if selection:
            track_index = selection[0]
            self.playlist.set_current_track(track_index)
            if pygame.mixer.get_busy():
                self.play_button.config(text="Play")
            else:
                self.play_button.config(text="Stop")

    def update_track_selection(self):
        """Обновить выделение в Listbox, чтобы соответствовало текущему треку."""
        self.track_list.selection_clear(0, tk.END)
        for i, track in enumerate(self.playlist.get_track_list()):
            if self.playlist.current_item and track == self.playlist.current_item.data.file_path:
                self.track_list.selection_set(i)
                break

    def update_playlist_list(self):
        """Обновить список треков в Listbox."""
        self.playlist_list.delete(0, tk.END)
        for i, playlist in enumerate(self.all_playlists):
            self.playlist_list.insert(tk.END, playlist.name)


# Создание окна
root = tk.Tk()

# Создание плейлиста
player_gui = PlayerGUI(root)

# Запуск главного цикла
root.mainloop()
