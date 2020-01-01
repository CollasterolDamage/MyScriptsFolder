@echo off
cd /d %~dp0
echo Installer das merdas que precisas para rodar isto...
echo (Nao me apetece dar compile)
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
del get-pip.py
pip install keyboard
pip install youtube_dl
if exist "%ProgramFiles(x86)%" (
curl https://ffmpeg.zeranoe.com/builds/win64/static/ffmpeg-20200101-7b58702-win64-static.zip -o ffmpegcompacted.zip
) else (
curl https://ffmpeg.zeranoe.com/builds/win32/static/ffmpeg-20200101-7b58702-win32-static.zip -o ffmpegcompacted.zip
)

curl -L https://raw.githubusercontent.com/CollasterolDamage/MyScriptsFolder/master/AudioScript/AudioScript.py -o AudioScript.py

echo @echo off>AS2Game.bat
echo title AudioScript.py>>AS2Game.bat
echo mode con: cols=59 lines=35>>AS2Game.bat
echo echo                     _ _       _____           _       _>>AS2Game.bat
echo echo      /\            ^^^| (_)     / ____^^^|         (_)     ^^^| ^^^|>>AS2Game.bat
echo echo     /  \  _   _  __^^^| ^^^|_  ___^^^| (___   ___ _ __ _ _ __ ^^^| ^^^|_>>AS2Game.bat
echo echo    / /\ \^^^| ^^^| ^^^| ^^^|/ _` ^^^| ^^^|/ _ \\___ \ / __^^^| '__^^^| ^^^| '_ \^^^| __^^^|>>AS2Game.bat
echo echo   / ____ \ ^^^|_^^^| ^^^| (_^^^| ^^^| ^^^| (_) ^^^|___) ^^^| (__^^^| ^^^|  ^^^| ^^^| ^^^|_) ^^^| ^^^|_>>AS2Game.bat
echo echo  /_/    \_\__,_^^^|\__,_^^^|_^^^|\___/_____/ \___^^^|_^^^|  ^^^|_^^^| .__/ \__^^^|>>AS2Game.bat
echo echo                                                ^^^| ^^^|>>AS2Game.bat
echo echo                                                ^^^|_^^^|>>AS2Game.bat
echo echo(>>AS2Game.bat
echo python AudioScript.py>>AS2Game.bat
echo exit>>AS2Game.bat

echo @echo off>unpacker.bat
echo setlocal>>unpacker.bat
echo cd /d %%~dp0>>unpacker.bat
echo Call :UnZipFile "%~dp0ffmpeg_dir" "%~dp0ffmpegcompacted.zip">>unpacker.bat
echo exit /b>>unpacker.bat

echo :UnZipFile ^<ExtractTo^> ^<newzipfile^>>>unpacker.bat
echo set vbs="%%temp%%\_.vbs">>unpacker.bat
echo if exist %%vbs%% del /f /q %%vbs%%>>unpacker.bat
echo ^>%%vbs%%  echo Set fso = CreateObject("Scripting.FileSystemObject")>>unpacker.bat
echo ^>^>%%vbs%% echo If NOT fso.FolderExists(%%1) Then>>unpacker.bat
echo ^>^>%%vbs%% echo fso.CreateFolder(%%1)>>unpacker.bat
echo ^>^>%%vbs%% echo End If>>unpacker.bat
echo ^>^>%%vbs%% echo set objShell = CreateObject("Shell.Application")>>unpacker.bat
echo ^>^>%%vbs%% echo set FilesInZip=objShell.NameSpace(%%2).items>>unpacker.bat
echo ^>^>%%vbs%% echo objShell.NameSpace(%%1).CopyHere(FilesInZip)>>unpacker.bat
echo ^>^>%%vbs%% echo Set fso = Nothing>>unpacker.bat
echo ^>^>%%vbs%% echo Set objShell = Nothing>>unpacker.bat
echo cscript //nologo %%vbs%%>>unpacker.bat
echo if exist %%vbs%% del /f /q %%vbs%%>>unpacker.bat
::echo del ffmpegcompacted.zip>>unpacker.bat
call unpacker.bat
del unpacker.bat
