@echo off
pyinstaller.exe .\src\main.py --add-data "src\res;res" -n ArcheoSiteNamer -F --noconfirm
Pause
