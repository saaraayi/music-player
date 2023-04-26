import threading
from tkinter import filedialog, ttk, NS, Canvas, Scrollbar, messagebox
from tkinter import *
import pygame
import os
import tkinter as tk
from pygame import mixer
from PIL import ImageTk, Image

pygame.init()
root = Tk()
root.geometry("500x580")  # size of the window
root.title("Music player- My favourite songs!")  # title of the window
# root.resizable(0, 0) # size is fixed
root.wm_iconbitmap('assets/song.ico')

# load background image
bg_image = Image.open('assets/1.png')
tk_image = ImageTk.PhotoImage(bg_image)

# add image to the root
bg_label = Label(root, image=tk_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# scrollbar to scroll the songs in the playlist
scrollbar = Scrollbar(root, width=23)
scrollbar.pack(side=RIGHT, fill=Y)

menubar = Menu(root)
root.config(menu=menubar)
mixer.init()
pygame.mixer.init()  # initializing the mixer

songs = []
current_song = ""
paused = False

# label for the scale
label = Label(root, text="sound level")
label.pack()
label.configure(bg="#969696", font=("arial", "11"))


# loading a single music in the playlist from the directory that the user selects
def load_mp3():
    global current_song
    root.filename = filedialog.askopenfilename(initialdir="/", title="Select MP3 file",
                                               filetypes=(("MP3 files", "*.mp3"), ("all files", "*.*")))
    if root.filename:
        songs.append(root.filename)
        songList.insert("end", os.path.basename(root.filename))
        songList.selection_set(0)
        current_song = songs[songList.curselection()[0]]
        play_music()


# loading a folder containing music in the playlist from the directory that the user selects
def load_music():
    global current_song
    root.directory = filedialog.askdirectory()

    for song in os.listdir(root.directory):
        print("1", song)
        name, ext = os.path.splitext(song)
        if ext == '.mp3':
            print("2", song)
            songs.append(song)
    print(songs[0])
    print(type(songs[0]))
    print(type(songs))
    for song in songs:
        songList.insert("end", song)

    songList.selection_set(0)
    current_song = songs[songList.curselection()[0]]


def select_song(event):
    global current_song
    current_song = songs[songList.curselection()[0]]
    play_music()


def play_next_music():
    next_music()


def play_music():
    global current_song, paused

    if not paused:
        pygame.mixer.music.load(os.path.join(root.directory, current_song))
        pygame.mixer.music.play()
        pygame.mixer.music.set_endevent(pygame.USEREVENT)

        def music_thread():
            x = 0
            while x == 0:
                for event in pygame.event.get():
                    if event.type == pygame.USEREVENT:
                        # Music has finished playing, play the next song
                        if not paused:
                            play_next_music()
                            x = 1
                if not pygame.mixer.music.get_busy():
                    # Music has finished playing, but the end event was not triggered
                    if not paused:
                        play_next_music()
                        x = 1
                pygame.time.wait(10)

        thread = threading.Thread(target=music_thread)
        thread.start()
    else:
        pygame.mixer.music.unpause()
        paused = False


# pause music button
def pause_music():
    global paused
    pygame.mixer.music.pause()
    paused = True


# next music button
def next_music():
    global current_song, paused

    try:
        songList.selection_clear(0, END)
        songList.selection_set(songs.index(current_song) + 1)
        current_song = songs[songList.curselection()[0]]
        play_music()
    except IndexError:
        messagebox.showerror("Error", "There is no next song")
        pass


# previous music button
def previous_music():
    global current_song, paused

    try:
        songList.selection_clear(0, END)
        songList.selection_set(songs.index(current_song) - 1)
        current_song = songs[songList.curselection()[0]]
        play_music()
    except IndexError:
        messagebox.showerror("Error", "There is no previous song")
        pass


muted = FALSE


# set volume function for the scale
def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)
    # set_volume of mixer takes value only from 0 to 1. Example - 0, 0.1,0.55,0.54.0.99,1


muted = FALSE


# mute button function
def mute_music():
    global muted
    if muted:  # Unmute the music
        mixer.music.set_volume(0.7)
        volume_btn.configure(image=volume_btn_image)
        scale.set(50)
        muted = FALSE
    else:  # mute the music
        mixer.music.set_volume(0)
        volume_btn.configure(image=mute_btn_image)
        scale.set(0)
        muted = TRUE


# to end and exit the program
def end():
    response = messagebox.askyesno("Exit", "do you want to close the playlist?")
    if response == YES:
        mixer.music.stop()
        root.destroy()
    else:
        pass


# scale and its configurations to adjust the sound
scale = tk.Scale(root,
                 from_=0,
                 to=100,
                 orient=tk.HORIZONTAL,
                 length=120,
                 command=set_vol)
scale.set(50)  # implement the default value of scale when music player starts
mixer.music.set_volume(0.7)
scale.pack()
scale.configure()
scale.configure(bg="#969696",
                activebackground="#333333",
                troughcolor="#e6e6e6",
                font=("arial", "11"))

# menubar and the commands
organise_menu = Menu(menubar, tearoff=False)
organise_menu.add_command(label='Select Folder', command=load_music)
organise_menu.add_command(label='Add song', command=load_mp3)
organise_menu.add_command(label='Exit', command=end)
menubar.add_cascade(label='File', menu=organise_menu)

# song list with the configurations

songList = Listbox(root,
                   bg="#b6b6b6",
                   fg="black",
                   width=70,
                   height=25,
                   borderwidth=0.5)
songList.pack(fill="both", expand="yes", padx=35, pady=10)
songList.configure(highlightbackground="black")
songList.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=songList.yview)
songList.bind("<<ListboxSelect>>", select_song)

# my buttons images
play_btn_image = PhotoImage(file='assets/play1.png')
pause_btn_image = PhotoImage(file='assets/pause1.png')
next_btn_image = PhotoImage(file='assets/next1.png')
previous_btn_image = PhotoImage(file='assets/prev1.png')
mute_btn_image = PhotoImage(file='assets/sound-off1.png')
volume_btn_image = PhotoImage(file='assets/sound1.png')

# my control frame for the controllers
control_frame = Frame(root)
control_frame.pack()
control_frame.configure(bg="#2D2E35")

# my buttons with the commands
play_btn = Button(control_frame,
                  image=play_btn_image,
                  borderwidth=0,
                  command=play_music)
pause_btn = Button(control_frame,
                   image=pause_btn_image,
                   borderwidth=0,
                   command=pause_music)
next_btn = Button(control_frame,
                  image=next_btn_image,
                  borderwidth=0,
                  command=next_music)
previous_btn = Button(control_frame,
                      image=previous_btn_image,
                      borderwidth=0,
                      command=previous_music)
volume_btn = Button(control_frame,
                    image=volume_btn_image,
                    borderwidth=0,
                    command=mute_music)

# grid for the buttons to place them in the right place
play_btn.grid(row=0, column=2, padx=10, pady=15)
pause_btn.grid(row=0, column=3, padx=10, pady=15)
next_btn.grid(row=0, column=4, padx=10, pady=15)
previous_btn.grid(row=0, column=1, padx=10, pady=15)
volume_btn.grid(row=0, column=0, padx=10, pady=15)

# calling mainloop
root.mainloop()
