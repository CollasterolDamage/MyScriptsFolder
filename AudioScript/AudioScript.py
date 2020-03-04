import time
import ctypes

import urllib.request
import urllib.parse
import re

import youtube_dl

import keyboard
import subprocess

import threading

import sys
import os


# Notes:
# Distribution incomplete
# Hotkey to Daemon
# FFMPEG CHECKER!

# Properties:

game_dir = "PUT GAME DIRECTORY HERE"
# Example: "C:\\Users\\IDidNineEleven\\Desktop\\Audiosurf2\\Audiosurf2.exe"
ffmpeg_dir = "PUT FFMPEG BIN DIRECTORY HERE"
# Example: "C:\\Users\\IDidNineEleven\\Desktop\\Audiosurf2\\ffmpeg_source\\bin"


game_start_seconds = 2  # Requires more on slow computers but if you're not playing on a toaster should be fine.
max_handle_tries = 3 # Set to -1 for infinite tries

hotkey = "F5"  # Full list here: https://github.com/boppreh/keyboard/blob/master/keyboard/_canonical_names.py

language = "en_US"  # Youtube downloader will be in english (Unchangeable)

# Program:

kernel32 = ctypes.WinDLL('kernel32')
user32 = ctypes.WinDLL('user32')

lang = {'pt_PT': ('Pesquisa do Youtube: ',
                  '\nPressiona 0 para cancelar\nPressiona qualquer outra tecla para repetir...\n',
                  'Número do vídeo: ',
                  'CONCLUÍDO!\n'),
        'en_US': ('Youtube search: ',
                  '\nPress 0 to cancel\nPress anything else to retry...\n',
                  'Video number: ',
                  'DONE!\n')
        }


# noinspection PyBroadException
def wait_onclose_old():
    try:
        print("Initializing...\n")
        subprocess.Popen(game_dir).wait()
    except:
        error(1)


# noinspection PyBroadException
def wait_onclose():
    try:
        print("Initializing...\n")
        game = subprocess.Popen(game_dir)

        global game_window
        global script_window
        print("TEST")
        tries = 0
        while 'game_window' not in globals() and 'script_window' not in globals():
            time.sleep(game_start_seconds)
            print("TEST2")

            if 'script_window' not in globals():
                script_window = kernel32.GetConsoleWindow()

            if 'game_window' not in globals():
                game_window = user32.GetForegroundWindow()

            if tries == max_handle_tries:
                error(1)
            elif tries > 0:
                print("Error configuring handles\nRetrying...\n")
            tries += 1

        print(game_window)
        print(script_window)
        game.wait()
    except:
        error(1)


# noinspection PyBroadException
def wait_onkey_old(retry=False):
    try:
        while True:
            if not retry:
                keyboard.wait(hotkey, suppress=True)
                keyboard.send("alt+tab")  # Window manipulation comming soon...
            retry = False
            download_yt(search_output())
            keyboard.send("alt+tab")
    except:
        error(2)

def window_handler_old():
    keyboard.send("alt+tab")

def window_handler():
    print(script_window)
    print(game_window)
    #current_window = user32.GetForegroundWindow()
    #if current_window ==

def daemon_cycler():
    # More stuff incomming
    # Any process to be executed that will be left in case program ends

    while True:
        if 'game_window' in globals() and 'script_window' in globals():
            download_yt(search_output())
        else:
            time.sleep(game_start_seconds)


# noinspection PyBroadException,PyBroadException,PyBroadException,PyBroadException
def search_output():
    word_search = input(lang[language][0])

    try:
        number_results = 5
        if ":" * 3 in word_search:  # For dev use; Should be fomated [string]:::[two digit number] eg.Imagine Dragons:::09
            number_results = int(word_search[-2:])
            word_search = word_search[:-5]
    except:
        number_results = None
        error(3)

    try:
        query_string = urllib.parse.urlencode({"search_query": word_search})
        html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string + "&sp=EgIQAQ%253D%253D").read().decode()
        title_search_results = re.findall(r'" {2}title="(.*)" aria-describedby="', html_content)[:number_results]
        url_search_results = list(dict.fromkeys(re.findall(r'href=\"/watch\?v=(.{11})', html_content)))[:number_results]

    except:
        url_search_results = None
        title_search_results = None
        number_results = None
        error(4)

    try:
        for title in title_search_results:
            if title.endswith('" rel="spf-prefetch'): title = title[:-19]
            print(str(title_search_results.index(title)+1) + ")", title)
        print(lang[language][1])


        video_number = int(input(lang[language][2])) - 1
        if video_number not in range(number_results):
            print()
            if video_number == -1:
                window_handler_old()
            else:
                wait_onkey_old(True)
        else:
            return url_search_results[video_number]
    except:
        error(4)


# noinspection PyBroadException,PyBroadException
def download_yt(url):
    # noinspection PyBroadException
    try:
        ydl_opts = {
            'format': 'bestaudio',
            'ffmpeg_location': ffmpeg_dir,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '0',
            }]
        }

        print()

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(["http://www.youtube.com/watch?v=" + url])
        print(lang[language][3])
    except:
        error(5)


def error(error_type=420):
    if error_type == 0:
        error_text = "threading functions..."
    elif error_type == 1:
        error_text = "creating the handle of the program"
    elif error_type == 2:
        error_text = "handling the application window..."
    elif error_type == 3:
        error_text = "using devs function. Please don't put ::: in your search criteria"
    elif error_type == 4:
        error_text = "accessing youtube... Please check your internet connection"
    elif error_type == 5:
        error_text = "scrapping html file..."
    elif error_type == 6:
        error_text = "downloading file... Please check your internet connection"
    else:
        error_type = "WE'RE ALL GONNA DIE!"
        error_text = "CRITICAL ERROR!"

    print("An error ocurred while", error_text, "\nError code:", error_type)
    input("Press enter to continue...")

    if error_type > 2:
        pass

    sys.exit()


# noinspection PyBroadException
def main():

    try:
        threading.Thread(target=wait_onclose).start() # Done
        threading.Thread(target=daemon_cycler, daemon=True).start() # To be changed
        keyboard.add_hotkey(hotkey, window_handler, suppress=True) # Working on it
    except:
        error(0)


if __name__ == '__main__':
    main()
