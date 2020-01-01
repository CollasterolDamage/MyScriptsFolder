import urllib.request
import urllib.parse
import re

import youtube_dl

import keyboard
import subprocess
import threading

import os

# Properties:
is_flushing = False  # For testing purposes


game_dir = "C:\\Users\\Miguel\\Desktop\\IGG-Audiosu2\\Audiosurf2.exe"
ffmpeg_dir = os.getcwd() + "\\ffmpeg_dir\\bin"

#Tester version
#ffmpeg_dir = "C:\\Users\\Miguel\\Desktop\\IGG-Audiosu2\\ffmpeg_source\\bin"

language = "en_US"  # Do not change! New version upcomming

lang = {'pt_PT': ('Pesquisa do Youtube: ',
                  '\nPressiona 0 para cancelar\nPressiona qualquer outra tecla para repetir...\n',
                  'Número do vídeo: ',
                  'CONCLUÍDO!\n'),
        'en_US': ('Youtube search: ',
                  '\nPress 0 to cancel\nPress anything else to retry...\n',
                  'Video number: ',
                  'DONE!\n')
        }

hotkey = "F5"  # Full list here: https://github.com/boppreh/keyboard/blob/master/keyboard/_canonical_names.py


def wait_onclose():
    try:
        print("Initializing...\n")
        subprocess.Popen(game_dir).wait()
    except:
        error(1)
    killer()


def wait_onkey(retry=False):
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


def search_output():
    try:
        word_search = input(lang[language][0])

        number_results = 5
        if ":"*3 in word_search:  # For dev use; Should be fomated [string]:::[two digit number] eg.Imagine Dragons:::09
            number_results = int(word_search[-2:])
            word_search = word_search[:-5]

        query_string = urllib.parse.urlencode({"search_query": word_search})
        html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string + "&sp=EgIQAQ%253D%253D").read().decode()
        title_search_results = re.findall(r'" {2}title="(.*)" aria-describedby="', html_content)[:number_results]
        url_search_results = list(dict.fromkeys(re.findall(r'href=\"/watch\?v=(.{11})', html_content)))[:number_results]

    except:
        url_search_results = None
        title_search_results = None
        number_results = None
        error(3)

    try:
        result_number = 0
        for title in title_search_results:
            result_number += 1
            if title.endswith('" rel="spf-prefetch'): title = title[:-19]
            print(str(result_number) + ")", title)
        print(lang[language][1])

        try:
            video_number = int(input(lang[language][2])) - 1
            if video_number not in range(number_results):
                print()
                if video_number == -1:
                    keyboard.send("alt+tab")
                    wait_onkey()
                else:
                    wait_onkey(True)
            else:
                return url_search_results[video_number]
        except:
            print()
            wait_onkey(True)
    except:
        error(4)


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

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(["http://www.youtube.com/watch?v=" + url])
        print(lang[language][3])
    except:
        error(5)


def error(error_type=420):
    if error_type == 0:
        error_text = "threading functions..."
    elif error_type == 1:
        error_text = "handling the applications..."
    elif error_type == 2:
        error_text = "running hotkey function..."
    elif error_type == 3:
        error_text = "accessing youtube... Please check your internet connection"
    elif error_type == 4:
        error_text = "scrapping html file..."
    elif error_type == 5:
        error_text = "downloading file... Please check your internet connection"
    else:
        error_type = "WE'RE ALL GONNA DIE!"
        error_text = "CRITICAL ERROR!"

    print("An error ocurred while", error_text, "\nError code:", error_type)
    input("Press enter to continue...")
    
    if error_type > 2:
        wait_onkey(True)
    else:
        killer()


def killer():
    os._exit(0)


def main():

    if is_flushing:
        import sys
        sys.exit()

    try:
        threading.Thread(target=wait_onclose).start()
        wait_onkey()
    except:
        error(0)


if __name__ == '__main__':
    main()
