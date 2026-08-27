# Random Wallpaper Slideshow

A Python-based Windows wallpaper slideshow that randomly displays wallpapers while ensuring that every image is shown once before any image is reused.

## Features

- Random wallpaper selection
- No repeated images within a cycle
- New random order for every cycle
- Prevents the last image of one cycle from being the first of the next
- Configurable slideshow interval
- Supports JPG, JPEG, PNG, BMP and WEBP
- Windows 11 desktop wallpaper integration

## Project Structure
```
.
├── main.py
├── slideshow.py
├── wallpaper.py
├── requirements.txt
├── README.md
└── .gitignore
```
## Technologies

- Python
- comtypes
- Windows IDesktopWallpaper API
- Object-Oriented Programming

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
python main.py
```
Enter the wallpaper folder and slideshow interval when prompted.

## Future Improvements

- Wallpaper scaling and orientation options
- GUI settings
- System tray support
- Start with Windows
- Pause/resume controls
- Multiple wallpaper folders

## Author

Yash Thakur
