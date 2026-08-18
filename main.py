from slideshow import Slideshow
import time
from wallpaper import Wallpaper

folder=input ("Enter wallpaper folder: ")

try:
    interval=float(input("Enter interval in seconds: "))
except ValueError:
    print("Invalid interval")
    exit()

try:
    slideshow=Slideshow(folder)
    wallpaper=Wallpaper()
except Exception as e:
    print("Error:",e)
    exit()

print("\n---Slideshow started---")
print("Press ctrl+c to stop\n")

try:
    while True:
        image=slideshow.getNext()
        print("showing:",image)

        if not wallpaper.setWallpaper(image):
            print("Failed to change wallpaper")
        time.sleep(interval)
except KeyboardInterrupt:
    print("\nslideshow stopped")