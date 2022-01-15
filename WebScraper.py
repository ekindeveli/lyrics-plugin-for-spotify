import requests
import time
import os
from bs4 import BeautifulSoup

"""
Websites used for lyrics retrieval:
    1- azlyrics.com
    2- songlyrics.com
    3- genius.com
    4- lyricsdb.co
    5- lyricsmania.com      // this one fails to deliver lyrics correctly, always fist paragraph missing..
    
"""


class WebScraper:
    def __init__(self):
        pass

    @staticmethod
    def lyrics_method_iterator(song, artist):
        lyrics = WebScraper.get_lyrics_songlyrics_soup(song, artist)
        source = "songlyrics.com"
        if len(lyrics) < 2:
            # lyrics string is empty, try another method
            lyrics = WebScraper.get_lyrics_genius_soup(song, artist)
            source = "genius.com"
            if len(lyrics) < 2:
                # lyrics string is empty, try another method
                lyrics = WebScraper.get_lyrics_az_soup(song, artist)
                source = "azlyrics.com"
                if len(lyrics) < 2:
                    # lyrics string is empty, try another method
                    lyrics = WebScraper.get_lyrics_lyricsdb_soup(song, artist)
                    source = "lyricsdb.co"
                    if len(lyrics) < 2:
                        # lyrics string is empty, try another method
                        lyrics = WebScraper.get_lyrics_lyricsmania_soup(song, artist)
                        source = "lyricsmania.com"
                        if len(lyrics) < 2:
                            # it's ok, just give up
                            lyrics = f"Could not find lyrics."
                            source = "N/A"
        retrieved_song = song
        return lyrics, source, retrieved_song

    @staticmethod
    def get_lyrics_genius_soup(song_name2, artist_name2):
        songname = song_name2.split(' - ')[0]
        query = artist_name2 + ' ' + songname
        query1 = WebScraper.query_cleaner(query)
        query2 = query1.replace(' ', '-').lower()
        url = f"https://genius.com/{query2}-lyrics"
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                     "Chrome/90.0.4430.212 Safari/537.36"
        headers = {'user-agent': user_agent}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        time.sleep(2)
        try:
            result = soup.body.find('div', class_='lyrics')
            lyrics = result.p.text.strip()
        except AttributeError:
            lyrics = ""
        return lyrics

    @staticmethod
    def get_lyrics_songlyrics_soup(song_name2, artist_name2):
        try:
            song_name2 = song_name2.split(' - ')[0]
            if " & " in song_name2:
                song_name2.replace(" & ", "")
            if " & " in artist_name2:
                artist_name2.replace(" & ", "")
            artist_name = WebScraper.query_cleaner(artist_name2)
            songname3 = WebScraper.query_cleaner(song_name2)
            songname_final = songname3.replace(' ', '-').lower()
            artistname_final = artist_name.replace(' ', '-').lower()

            url = f"http://www.songlyrics.com/{artistname_final}/{songname_final}-lyrics/"
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                         "Chrome/90.0.4430.212 Safari/537.36"
            headers = {'user-agent': user_agent}
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            lyrics = soup.find(id='songLyricsDiv').text.strip()
            if "do not have the lyrics for" in lyrics:
                lyrics = ""
            elif "Sorry, we have no" in lyrics:
                lyrics = ""
            return lyrics
        except AttributeError:
            lyrics = ""
            return lyrics

    @staticmethod
    def get_lyrics_lyricsdb_soup(song_name2, artist_name2):
        try:
            song_name2 = song_name2.split(' - ')[0]
            artist_name = WebScraper.query_cleaner(artist_name2)
            songname3 = WebScraper.query_cleaner(song_name2)
            songname_final = songname3.replace(' ', '+').lower()
            artistname_final = artist_name.replace(' ', '+').lower()
            url = f"http://www.lyricsdb.co/{artistname_final}/{songname_final}"
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                         "Chrome/90.0.4430.212 Safari/537.36"
            headers = {'user-agent': user_agent}
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            lyrics = soup.find(id='lyric').text.strip()
            with open('song_lyric.txt', 'w', encoding='utf-16') as txt_file:
                txt_file.write(lyrics)
            with open('song_lyric.txt', 'r', encoding='utf-16') as txt_file:
                lines = txt_file.readlines()
            with open('song_lyric.txt', 'w', encoding='utf-16') as txt_file:
                txt_file.writelines(lines[18:-25])
            with open('song_lyric.txt', 'r', encoding='utf-16') as txt_file:
                lyric = txt_file.readlines()
                lyrics = ""
                for line in lyric:
                    lyrics += line
            os.remove("song_lyric.txt")
        except AttributeError:
            lyrics = ""
        return lyrics

    @staticmethod
    def get_lyrics_lyricsmania_soup(song_name2, artist_name2):
        try:
            song_name2 = song_name2.split(' - ')[0]
            artist_name = WebScraper.query_cleaner(artist_name2)
            songname3 = WebScraper.query_cleaner(song_name2)
            songname_final = songname3.replace(' ', '_').lower()
            artistname_final = artist_name.replace(' ', '_').lower()
            url = f"http://www.lyricsmania.com/{songname_final}_lyrics_{artistname_final}.html"
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                         "Chrome/90.0.4430.212 Safari/537.36"
            headers = {'user-agent': user_agent}
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            lyrics = soup.find(class_='lyrics-body').text.strip()
        except AttributeError:
            lyrics = ""
        return lyrics

    @staticmethod
    def get_lyrics_az_soup(song_name2, artist_name2):
        try:
            song_name2 = song_name2.split(' - ')[0]
            artistname3 = WebScraper.query_cleaner(artist_name2)
            songname3 = WebScraper.query_cleaner(song_name2)
            songname3 = songname3.replace("+", "")
            artistname3 = artistname3.replace("+", "")
            songname_final = songname3.replace(" ", "").lower()
            artistname_final = artistname3.replace(" ", "").lower()
            url = f"http://www.azlyrics.com/lyrics/{artistname_final}/{songname_final}.html"
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                         "Chrome/90.0.4430.212 Safari/537.36"
            headers = {'user-agent': user_agent}
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            lyrics = soup.body.text.strip()
            with open('song_lyric.txt', 'w', encoding='utf-16') as txt_file:
                txt_file.write(lyrics)
            with open('song_lyric.txt', 'r', encoding='utf-16') as txt_file:
                lines = txt_file.readlines()
            with open('song_lyric.txt', 'w', encoding='utf-16') as txt_file:
                txt_file.writelines(lines[88:-102])
            with open('song_lyric.txt', 'r', encoding='utf-16') as txt_file:
                lyric = txt_file.readlines()
                for line in lyric:
                    if "Submit Corrections" in line:
                        with open('song_lyric.txt', 'w', encoding='utf-16') as txt_file2:
                            txt_file2.writelines(lyric[:-48])
            with open('song_lyric.txt', 'r', encoding='utf-16') as txt_file:
                lyric = txt_file.readlines()
                lyrics = ""
                for line in lyric:
                    lyrics += line
            os.remove("song_lyric.txt")
        except AttributeError:
            lyrics = ""
        return lyrics

    @staticmethod
    def query_cleaner(query1):
        if '/' in query1:
            query1 = query1.replace('/', ' ')
            if '   ' in query1:
                query1 = query1.replace('   ', ' ')
        if ',' in query1:
            query1 = query1.replace(',', '')
        if "'" in query1:
            query1 = query1.replace("'", '')
        if 'ó' in query1:
            query1 = query1.replace('ó', 'o')
        if 'ō' in query1:
            query1 = query1.replace('ō', 'o')
        if '&' in query1:
            query1 = query1.replace("&", 'and')
        if ':' in query1:
            query1 = query1.replace(":", '')
        if '.' in query1:
            query1 = query1.replace('.', '')
        if '(' in query1:
            query1 = query1.replace('(', '')
        if ')' in query1:
            query1 = query1.replace(')', '')
        if 'ü' in query1:
            query1 = query1.replace('ü', 'u')
        if 'ğ' in query1:
            query1 = query1.replace('ğ', 'g')
        if 'ö' in query1:
            query1 = query1.replace('ö', 'o')
        if 'ç' in query1:
            query1 = query1.replace('ç', 'c')
        if 'ş' in query1:
            query1 = query1.replace('ş', 's')
        if 'ı' in query1:
            query1 = query1.replace('ı', 'i')
        query1 = query1.strip()
        return query1
