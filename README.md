# Random Wallpaper Slideshow

A Python-based Windows wallpaper slideshow that randomly displays wallpapers while ensuring that every image is shown once before any image is reused.

## Features

- Random wallpaper selection
- No repeated images within a cycle
- Configurable slideshow interval
- Dynamic wallpaper folder updates
- Wallpaper position options
- GUI settings and controls
- Start and stop slideshow from the GUI
- Saves configuration settings
- Supports JPG, JPEG, PNG, BMP and WEBP

## Project Structure
```
.
├── main.py
├── gui.py
├── slideshow.py
├── wallpaper.py
├── config.py
├── config.json
├── requirements.txt
├── README.md
└── .gitignore
```
## Technologies

- Python
- comtypes
- Windows IDesktopWallpaper API
- Object-Oriented Programming
- Tkinter
- ctypes

## How It Works
```
Wallpaper Folder
       ↓
Find Images
       ↓
Shuffle
       ↓
Show Each Image Once
       ↓
New Random Order
       ↓
Repeat
```
## Requirements

- Python 3
- Windows 11
- comtypes

## Run
```bash
pip install -r requirements.txt
python gui.py
```
Use the GUI to select the wallpaper folder, set the interval and position, and control the slideshow.

## Future Improvements

- System tray support
- Start with Windows
- Pause/resume controls
- Multiple wallpaper folders
- Executable distribution

## Author

Yash Thakur
