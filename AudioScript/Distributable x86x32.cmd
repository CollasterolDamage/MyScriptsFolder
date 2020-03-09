@echo off
title AudioScript Setup
mode con: cols=59 lines=35
echo                     _ _       _____           _       _
echo      /\            ^| (_)     / ____^|         (_)     ^| ^|
echo     /  \  _   _  __^| ^|_  ___^| (___   ___ _ __ _ _ __ ^| ^|_
echo    / /\ \^| ^| ^| ^|/ _` ^| ^|/ _ \\___ \ / __^| '__^| ^| '_ \^| __^|
echo   / ____ \ ^|_^| ^| (_^| ^| ^| (_) ^|___) ^| (__^| ^|  ^| ^| ^|_) ^| ^|_
echo  /_/    \_\__,_^|\__,_^|_^|\___/_____/ \___^|_^|  ^|_^| .__/ \__^|
echo                     __           _             ^| ^|__
echo                    / /          ^| ^|            ^|_^|\ \
echo                   ^| ^|   ___  ___^| ^|_ _   _ _ __    ^| ^|
echo                   ^| ^|  / __^|/ _ \ __^| ^| ^| ^| '_ \   ^| ^|
echo                   ^| ^|  \__ \  __/ ^|_^| ^|_^| ^| ^|_) ^|  ^| ^|
echo                   ^| ^|  ^|___/\___^|\__^|\__,_^| .__/   ^| ^|
echo                    \_\                    ^| ^|     /_/
echo                                           ^|_^|
echo(
echo Initializing...
echo(

:: Properties:

set "dev=false"
set "song_folder=songs"
set "ping_server=www.google.com"

:: Program:

ping %ping_server% -n 1 -w 1000 > NUL
if errorlevel 1 goto noconnection

if %dev%==true (
set "song_folder=SourceFiles"
set "folder_dir=%cd%\SourceFiles"
set "exe_name=DEVTEST.exe"
goto dev
)

setlocal EnableDelayedExpansion

echo Example: C:\Users\IDidNineEleven\Desktop\Audiosurf2\Audiosurf2.exe
set /p game_dir=Game directory:

set "i=0"
:nextchar
set c=!game_dir:~%i%,1!
if "%c%" == "" goto endloop
if "%c%" == "\" set pos=%i%
set /a i+=1
goto nextchar
:endloop
set folder_dir=!game_dir:~0,%pos%!
set exe_name=!game_dir:%folder_dir%\=!

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
del /q get-pip.py

pip install keyboard
pip install youtube_dl

cd "%folder_dir%"
curl -L https://raw.githubusercontent.com/CollasterolDamage/MyScriptsFolder/master/AudioScript/AS2Game.cmd -o AS2Game.cmd

:dev

md %song_folder%
cd %song_folder%
curl -L https://raw.githubusercontent.com/CollasterolDamage/MyScriptsFolder/master/AudioScript/README.txt -o README.txt
curl -L https://raw.githubusercontent.com/CollasterolDamage/MyScriptsFolder/master/AudioScript/AudioScript.py -o AudioScript.py
curl -L https://raw.githubusercontent.com/CollasterolDamage/MyScriptsFolder/master/AudioScript/setup.py -o setup.py

if exist "%ProgramFiles(x86)%" (
set "system_type=64"
curl https://ffmpeg.zeranoe.com/builds/win64/static/ffmpeg-4.2.2-win64-static.zip -o ffmpeg-4.2.2-win64-static.zip
) else (
set "system_type=32"
curl https://ffmpeg.zeranoe.com/builds/win32/static/ffmpeg-4.2.2-win32-static.zip -o ffmpeg-4.2.2-win32-static.zip
)

if %dev%==true (
curl -L https://raw.githubusercontent.com/CollasterolDamage/MyScriptsFolder/master/AudioScript/AS2Game.cmd -o AS2Game.cmd
echo python setup.py "%folder_dir%" "%song_folder%" "%exe_name%" "%ping_server%" "%system_type%">SETUPTEST.bat
goto end
)

python setup.py "%folder_dir%" "%song_folder%" "%exe_name%" "%ping_server%" "%system_type%"

goto end

:noconnection
echo Make sure you have a internet connection!
pause

:end
exit