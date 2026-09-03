from slideshow import Slideshow
import time
from wallpaper import Wallpaper
from config import Config

def run():
    configManager=Config()
    config=configManager.load()

    folder=config["folder"]
    interval=config["interval"]
    position=config["position"]

    if not folder:
        print("No folder configured")
        print("Edit config.json and add wallpaper folder")
        return

    try:
        slideshow=Slideshow(folder)
        wallpaper=Wallpaper()
    except Exception as e:
        print("Error:",e)
        return

    if not wallpaper.setPosition(position):
        print("Invalid Position")
        return

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

if __name__=="__main__":
    run()