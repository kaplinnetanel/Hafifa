from mutagen.easyid3 import EasyID3
import pygame
from tkinter.filedialog import askopenfilenames
from tkinter import *
pygame.init()

class FrameApp(Frame):
    def __init__(self,master):
        super().__init__(master)
        self.songs = []
        self.is_paused = False
        self.current_song_index = 0
        self.song_end_event = pygame.USEREVENT + 1
        self.grid()
        self.create_buttons()
        self.create_display()


    def create_display(self):
        self.now_playing_label = Label(
            self, fg='Black',
            font=('Helvetica 12 bold italic', 10),
            bg='ivory2'
        )
        self.now_playing_label.grid(row=6, column=0)

        self.song_list_text = Text(self, wrap=WORD, width=60)

        self.song_list_text.grid(row=8, column=0)

    def create_buttons(self):
        self.create_button("PLAY SONG", self.play_song, 2)
        self.create_button("PREVIOUS SONG", self.previous_song, 4)
        self.create_button("PAUSE/UNPAUSE", self.pause_song, 3)
        self.create_button("NEXT SONG", self.next_song, 5)
        self.create_button("ADD TO LIST", self.add_song, 1)        

    def create_button(self, text, command, row):
        button = Button(
            self,
            text=text,
            command=command,
            bg='AntiqueWhite1',
            width=40
        )
        button.grid(row=row, column=0)
#################################################################################

    def add_song(self):
         ##מוסיפה שירים לרשימה
        selected_files = askopenfilenames()
        for song_path in selected_files:
            self.songs.append(song_path)

        self.show_songs()
    

    def show_songs(self):
    ##מציגה את השירים בממשק
        self.song_list_text.delete("1.0", END)

        for index, song_path in enumerate(self.songs, start=1):
            try:

                song = EasyID3(song_path)

                song_data = f"{index}: {song['title'][0]} - {song['artist'][0]}"

                self.song_list_text.insert(END, song_data + "\n")

            except Exception as e:
                print(f"Error reading song {song_path}: {e}")


#################################################################################
    def get_song_data(self):
        ##  מביא לך את פרטי השיר מתודה שמשתמשת מי שמנגן כרגע
        try:
            song = EasyID3(self.songs[self.current_song_index])
            song_data = "Now playing: Nr:" + str(self.current_song_index + 1) + " " + \
                        str(song['title']) + " - " + str(song['artist'])
            return song_data
        except Exception as e:
            print(f"Error getting song data: {e}")
            return None
    #################################################################################
    def play_song(self):
        try:
                song_path = self.songs[self.current_song_index]

                pygame.mixer.music.load(song_path)
                pygame.mixer.music.play(1, 0.0)
                pygame.mixer.music.set_endevent(self.song_end_event)

                self.is_paused = False
                self.now_playing_label["text"] = self.get_song_data()

        except (IndexError, pygame.error) as e:
            print(f"Error playing song: {e}")
#################################################################################
    def check_music(self):
        try:
            for event in pygame.event.get():
                if event.type == self.song_end_event:
                    self.next_song()
        except pygame.error as e:
            print(f"Error checking music: {e}")
#################################################################################
    def pause_song(self):
        try:
            if self.is_paused:
                pygame.mixer.music.unpause()
                self.is_paused = False
            else:
                pygame.mixer.music.pause()
                self.is_paused = True

        except pygame.error as e:
            print(f"Error pausing song: {e}")

#################################################################################
    def get_next_song(self):

        if self.current_song_index + 1 < len(self.songs):
            return self.current_song_index + 1
        return 0

#################################################################################
    def next_song(self):
        self.current_song_index = self.get_next_song()
        self.play_song()

#################################################################################
    def get_previous_song(self):
        ##מציאת השיר הקודם
        if self.current_song_index > 0:
            return self.current_song_index - 1

        return len(self.songs) - 1
#################################################################################
    def previous_song(self):
        ##מעבר לשיר הקודם 
        self.current_song_index = self.get_previous_song()
        self.play_song()
#################################################################################
#################################################################################
window = Tk()
window.geometry("500x500")
window.title("MP3 Music Player")
#################################################################################
app = FrameApp(window)
#################################################################################
while True:
    # runs mainloop of program
    app.check_music()
    app.update()