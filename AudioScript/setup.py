import sys
import os
import zipfile

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

def main():
    folder_dir = sys.argv[1]
    song_folder = sys.argv[2]
    ffmpeg_path = folder_dir + "\\" + song_folder + "\\ffmpeg-4.2.2-win" + sys.argv[5] + "-static"

    with zipfile.ZipFile(ffmpeg_path + ".zip", 'r') as zip:
        zip.extractall(folder_dir + "\\" + song_folder)
    os.remove(ffmpeg_path + ".zip")

    propertyWriter("AS2Game.cmd", ["cd songs\n","ping www.google.com -n 1 -w 1000 > NUL\n"], ["cd "+ song_folder +"\n","ping " + sys.argv[4] + " -n 1 -w 1000 > NUL"])
    propertyWriter("AudioScript.py", ['game_dir = "PUT GAME DIRECTORY HERE"\n','ffmpeg_dir = "PUT FFMPEG BIN DIRECTORY HERE"\n'], ['game_dir = "' + folder_dir + "\\" + sys.argv[3] + '"\n','ffmpeg_dir = "'+ ffmpeg_path + '\\bin"\n'])


if __name__ == '__main__':
    main()