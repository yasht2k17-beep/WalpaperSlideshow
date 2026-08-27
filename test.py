from wallpaper import Wallpaper


wallpaper = Wallpaper()

path = input("Enter image path: ")

if wallpaper.setWallpaper(path):
    print("Wallpaper changed successfully.")
else:
    print("Failed to change wallpaper.")


position = input(
    "Enter position (center/tile/stretch/fit/fill): "
).lower()

if wallpaper.setPosition(position):
    print("Position changed successfully.")
else:
    print("Invalid position or failed to change position.")