@echo off
chcp 65001 >nul
py -3.13 -m pip install pyinstaller
if errorlevel 1 pause & exit /b 1
py -3.13 -m PyInstaller --onefile --windowed --name CustomGPTRunner desktop_app\runner.py
pause
