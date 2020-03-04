import sys
import os
import zipfile

#Properties:

#I got exe name, folder dir, game dir, song folder
#ffmpeg is on song folder
# I need song folder, game dir

folder_dir = sys.argv[1]
exe_name = sys.argv[2]
ping_server = sys.argv[3] #cmd
song_folder = sys.argv[4] #cmd
ffmpeg_dir = folder_dir + "\\" + song_folder + "\\"
game_dir = folder_dir + "\\" + exe_name

#None


def propertyWriter(file, to_replace, replace):
    temp_file = []
    with open(file, 'r') as fin:
        for line in fin:
            temp_file.append(line)

    with open(file, 'w') as fout:
        for line in temp_file:
            for n in range(len(replace)):
                if line == to_replace[n]:
                    line = replace[n]
            fout.write(line)



def ffmpegSetup(folder_dir):
    #ffmpeg_path = folder_dir +
    with zipfile.ZipFile(run_dir, 'r') as zip:
        zip.extractall(game_dir)
    path = ""
    return path

def main():
    #folder_dir = sys.argv[1]
    #exe_name = sys.argv[2]
    #ffmpeg_path = ffmpegSetup(folder_dir)
    propertyWriter("AS2Game.cmd", ["cd songs\n","ping www.google.com -n 1 -w 1000 > NUL\n"], ["cd "+ song_folder +"\n","ping " + ping_server + " -n 1 -w 1000 > NUL"])
    propertyWriter("AudioScript.py", ['game_dir = "PUT GAME DIRECTORY HERE"\n','ffmpeg_dir = "PUT FFMPEG BIN DIRECTORY HERE"\n'], ['game_dir = "'+ game_dir +'"\n','ffmpeg_dir = "'+ ffmpeg_path +'"\n'])


if __name__ == '__main__':
    main()