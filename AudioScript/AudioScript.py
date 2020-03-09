import urllib.request
import urllib.parse
import re

import youtube_dl
import keyboard

import subprocess
import ctypes
import threading

import time
import os


# Properties:

game_dir = "PUT GAME DIRECTORY HERE"
# Example: "C:\\Users\\IDidNineEleven\\Desktop\\Audiosurf2\\Audiosurf2.exe"
ffmpeg_dir = "PUT FFMPEG BIN DIRECTORY HERE"
# Example: "C:\\Users\\IDidNineEleven\\Desktop\\Audiosurf2\\ffmpeg_source\\bin"

handling_delay = 2  # Requires more on slow computers but if you're not on a toaster it should be fine.
max_handle_tries = 3  # Set to -1 for infinite tries
game_window_mode = True
window_reset = True

hotkey = "F5"  # Full list here: https://github.com/boppreh/keyboard/blob/master/keyboard/_canonical_names.py

language = "en_US"  # Youtube downloader will be in english (Unchangeable)


# Program:

kernel32 = ctypes.WinDLL('kernel32')
user32 = ctypes.WinDLL('user32')

lang = {'pt_PT': ('Pesquisa do Youtube: ',
                  '\nPressiona qualquer outra tecla para repetir...\n',
                  'Número do vídeo: ',
                  'Concluído!\n'),
        'en_US': ('Youtube search: ',
                  '\nPress anything else to retry...\n',
                  'Video number: ',
                  'Successful!\n')
        }


def wait_onclose():
    try:
        print("Initializing...\n")
        game = subprocess.Popen(game_dir)

        global game_window
        global script_window

        tries = 0
        while 'script_window' not in globals() or (game_window_mode and 'game_window' not in globals()):
            if game_window_mode or tries > 0:
                time.sleep(handling_delay)

            if 'script_window' not in globals():
                script_window = kernel32.GetConsoleWindow()

            if game_window_mode and 'game_window' not in globals():
                game_window = user32.GetForegroundWindow()

            if tries == max_handle_tries:
                error(2)
            elif tries > 0:
                print("Error configuring handles\nRetrying...\n")
            tries += 1

        game.wait()

    except:
        error(2)


def window_handler(reset=False):
    try:

        if (window_reset and reset) or user32.GetForegroundWindow() == script_window:
            user32.ShowWindow(script_window, 6)
            user32.ShowWindow(script_window, 0)
            if game_window_mode:
                user32.SetForegroundWindow(game_window)
        else:
            user32.ShowWindow(script_window, 6)
            user32.ShowWindow(script_window, 9)

    except:
        error(3)


def daemon_cycler(exception_error=False):

    if not exception_error:
        while (game_window_mode and 'game_window' not in globals()) or 'script_window' not in globals():
            time.sleep(handling_delay)
        user32.ShowWindow(script_window, 0)

    while True:
        window_handler(reset=download_yt(search_output()))


def search_output():
    word_search = input(lang[language][0])

    try:
        number_results = 5
        if ":" * 3 in word_search:  # For dev use; Should be fomated [string]:::[two digit number] eg.Imagine Dragons:::09
            number_results = int(word_search[-2:])
            word_search = word_search[:-5]
    except:
        error(4)

    try:
        query_string = urllib.parse.urlencode({"search_query": word_search})
        html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string + "&sp=EgIQAQ%253D%253D").read().decode()
        title_search_results = re.findall(r'" {2}title="(.*)" aria-describedby="', html_content)[:number_results]
        url_search_results = list(dict.fromkeys(re.findall(r'href=\"/watch\?v=(.{11})', html_content)))[:number_results]

        result_number = 0
        for title in title_search_results:
            result_number += 1
            if title.endswith('" rel="spf-prefetch'): title = title[:-19]
            print(str(result_number) + ")", title)
        print(lang[language][1])

        try:
            video_number = int(input(lang[language][2])) - 1

            if video_number in range(number_results):
                return url_search_results[video_number]
            else:
                raise ValueError("Undefined Value")
        except ValueError:
            return None

    except:
        error(5)


def download_yt(url):
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
        if url is not None:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download(["http://www.youtube.com/watch?v=" + url])
            print(lang[language][3])
            return False

        return True

    except:
        error(5)


def error(error_level=420):  # Inefficient but it works
    if error_level == 0:
        error_text = "opening ffmpeg... Please check if ffmpeg is configured"
    elif error_level == 1:
        error_text = "threading functions..."
    elif error_level == 2:
        error_text = "configuring window handles..."
    elif error_level == 3:
        error_text = "managing windows..."
    elif error_level == 4:
        error_text = "using devs function. Please don't put ::: in your search criteria"
    elif error_level == 5:
        error_text = "accessing youtube... Please check your internet connection"
    else:
        error_text = "Good news everyone!"
        error_level = "CRITICAL ERROR!"

    print("\n\nAn error ocurred while", error_text, "\nError code:", error_level, "\nPress enter to continue...")
    input()

    try:
        if error_level > 3:
            print()
            daemon_cycler(exception_error=True)
        else:
            raise TypeError

    except TypeError:
        raise SystemExit


def main():

    if not os.path.exists(ffmpeg_dir):
        error(0)

    if os.path.exists("setup.py"):
        os.remove("setup.py")

    try:
        threading.Thread(target=wait_onclose).start()  # Done
        threading.Thread(target=daemon_cycler, daemon=True).start()  # To be changed
        keyboard.add_hotkey(hotkey, window_handler, suppress=True)  # Working on it
    except:
        error(1)


if __name__ == '__main__':
    main()
