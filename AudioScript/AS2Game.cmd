@echo off
cd songs
title AudioScript.py
mode con: cols=59 lines=35
echo                     _ _       _____           _       _
echo      /\            ^| (_)     / ____^|         (_)     ^| ^|
echo     /  \  _   _  __^| ^|_  ___^| (___   ___ _ __ _ _ __ ^| ^|_
echo    / /\ \^| ^| ^| ^|/ _` ^| ^|/ _ \\___ \ / __^| '__^| ^| '_ \^| __^|
echo   / ____ \ ^|_^| ^| (_^| ^| ^| (_) ^|___) ^| (__^| ^|  ^| ^| ^|_) ^| ^|_
echo  /_/    \_\__,_^|\__,_^|_^|\___/_____/ \___^|_^|  ^|_^| .__/ \__^|
echo                                                ^| ^|
echo                                                ^|_^|
echo(

ping www.google.com -n 1 -w 1000 > NUL
if errorlevel 1 echo Warning: No internet connection & echo(

python AudioScript.py
exit