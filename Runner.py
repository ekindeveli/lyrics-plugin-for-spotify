import threading
import time
import SpotiAuth
import WebScraper
from tkinter import *
import codecs

# -----------------------------------------------------------------------------------------------------------
# Runner Script:
#
# Thread 1- from Spoti Auth class, call initializer, then create thread and put timer of thread
# to call token reinit, this thread calls itself every 50 mins
#
# Thread 2- create thread and call backend script
# this thread calls itself every 10s
#
# Thread 3 (Not a thread)- Start GUI
# -----------------------------------------------------------------------------------------------------------


def backend_script():
    retrieved_song = "none"
    while True:
        token = SpotiAuth.token_response2
        song, artist, is_playing = SpotiAuth.SpotiAuth.currently_playing(token)
        if is_playing:
            if song != retrieved_song:
                lyrics_to_get = f'{song} - {artist}'
                lyrics, source, retrieved_song = WebScraper.WebScraper.lyrics_method_iterator(song, artist)

                # Show the retrieved lyrics on the GUI
                with open('song_lyrics.txt', 'w+', encoding='utf-16') as lyrics_file:
                    lyrics_file.write(f'\n{lyrics_to_get}\n\n{lyrics}\n\nsource: {source}')
                txt = Text(root, height=32, width=68, background='#0066CC', foreground='white',
                           wrap=WORD, font="Calibri")
                txt.tag_configure("center", justify='center')
                scrollb = Scrollbar(root, command=txt.yview)
                txt['yscrollcommand'] = scrollb.set
                txt.grid(row=0, rowspan=3, columnspan=4, sticky='news')
                with codecs.open('song_lyrics.txt', 'r', 'utf-16') as f:
                    txt.insert(INSERT, f.read())
                txt.tag_add("center", "1.0", "end")
                txt.config(state=DISABLED)
                root.update()
            else:
                pass
        else:
            # Print to the GUI 'Spotify is currently not playing any tracks.'
            with open('song_lyrics.txt', 'w+', encoding='utf-16') as lyrics_file:
                lyrics_file.write(f'Spotify is currently not playing any tracks.')
            root.update()
        time.sleep(10)


# Thread 1: Establishing and Maintaining Spotify OAuth Connection
token_response = SpotiAuth.SpotiAuth.initializer()
first_start = True
threading.Thread(target=SpotiAuth.SpotiAuth.recursive_reinit,
                 args=[token_response, first_start], daemon=True).start()

# Creating the Window for the GUI
root = Tk()
root.title("Spotify Lyrics Plugin")
root.configure(background='#0066CC')
root.minsize(420, 220)
root.maxsize(880, 920)
root.rowconfigure([0, 1, 2], minsize=60, weight=1)
root.columnconfigure([0, 1, 2], minsize=75, weight=1)
root.rowconfigure([3], minsize=60, weight=0)
btn_quit = Button(root, text="Quit", width=12, bg='#0080FF', fg='white', command=root.destroy) \
    .grid(row=3, column=1, sticky='s', padx=5, pady=5)

# Thread 2: Backend Script
threading.Thread(target=backend_script, daemon=True).start()

# Thread 3 (Main Thread): Start GUI
root.mainloop()
