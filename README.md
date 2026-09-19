# OtterShare

A Windows screenshot-sharing experiment in Python. I wanted to build my own screenshot utility and explore Windows input hooks and `ctypes` along the way.

An older personal project exploring desktop tooling, image sharing, and native Windows APIs.

## What's here

- **Screen capture:** Win32 bitmap capture converted to PNG with Pillow.
- **Image sharing:** an Imgur upload function that copies the returned URL to the clipboard and records the URL and delete hash in `url_links.txt`.
- **Native input:** keyboard and mouse hooks built around Windows APIs and `ctypes`.
- **Desktop shell:** a wxPython window and tray icon, including a configuration reload action.
- **Configuration:** defaults in `Config.py`, persisted to `config.ini` in the working directory.

## Exploring the project

The entry point is [Main.py](Main.py). It imports wxPython, pywin32, Pillow, and Requests; dependencies are not version-pinned. Windows is required for the native APIs.

Read [Screenshot.py](Screenshot.py) for capture and PNG saving, [ImageUpload.py](ImageUpload.py) for uploads, and [InputManager.py](InputManager.py), [WinKeyboard.py](WinKeyboard.py), and [WinMouse.py](WinMouse.py) for the input experiments.

The configuration includes an Imgur `client_id`, a save directory, and a default screenshot shortcut of `ctrl+shift+e`. Uploading requires your own Imgur application ID. The save directory must exist.

## Project status

This is an unfinished experiment. The screenshot hotkey wiring and parts of the input, configuration, and shutdown handling need repair before the pieces work together as a complete utility.

Ideas for further exploration included area selection, active-window capture, file uploads, and image organization; these were not completed.
