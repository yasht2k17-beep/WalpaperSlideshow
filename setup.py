from config import Config
from pathlib import Path

configManager=Config()
config=configManager.load()

print("\n--- Wallpaper Slideshow Setup ---\n")

while(True):
    folder=input("Wallpaper Folder:")
    if folder and Config().path.parent.exists():
        if Path(folder).is_dir():
            break
    print("Invalid Folder")

while (True):
    try:
        interval=float(input("Interval in seconds:"))
        if interval>0:
            break

    except ValueError:
        pass
    print("Invalid Interval")

while(True):
    position=input("Position(center/tile/stretch/fit/fill):").lower()

    if position in configManager.validPositions:
        break
    print("Invalid Position")

config={
    "folder":folder,
    "interval":interval,
    "position":position
}
configManager.save(config)

print("\nConfiguration saved.")