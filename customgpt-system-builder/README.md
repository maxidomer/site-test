# Forge — CustomGPT System Builder

Static website prototype for GitHub Pages, plus a Windows Tkinter Python runner.

## Website
Open `index.html` or publish this folder with GitHub Pages. Functions are saved in browser localStorage and exported as JSON. The preview runs user JavaScript in an iframe with `sandbox="allow-scripts"`.

**Security limits:** this demo is not real server-side authentication. Browser storage is not synced across devices. Do not store API keys, passwords, or secrets. For production accounts use a backend and server-side authentication. Arbitrary JavaScript should only be run if trusted.

## Desktop runner
Requires the existing Python 3.13 installation on Windows. It scans imports and offers to install missing modules with pip, then runs the script as a subprocess. Python scripts have the current user's permissions; inspect code before running.

Build an EXE from this folder on Windows:

```bat
py -3.13 -m pip install pyinstaller
py -3.13 -m PyInstaller --onefile --windowed --name CustomGPTRunner desktop_app/runner.py
```

This environment has not built or tested a Windows EXE. This is a prototype, not a real ChatGPT plugin: connecting to ChatGPT or a model API requires a separate supported integration.
