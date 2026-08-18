from wallpaper import Wallpaper

wallpaper = Wallpaper()

path = input("Enter image path: ")

if wallpaper.setWallpaper(path):
    print("Wallpaper changed successfully.")
else:
    print("Failed to change wallpaper.")