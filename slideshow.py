import random
from pathlib import Path

class Slideshow:
    def __init__(self,folder):
        self.folder=Path(folder)
        self.extensions={".jpg",
            ".jpeg",
            ".png",
            ".bmp",
            ".webp"}
        self.wallpapers=[]
        self.remaining=[]
        self.lastShown=None

        self.loadWallpapers()

    def loadWallpapers(self):

        self.wallpapers=[file for file in self.folder.iterdir()
                         if file.is_file()
                         and file.suffix.lower() in self.extensions]

        if not self.wallpapers:
            raise ValueError("No supprted Wallpapers found")
        self.startNewCycle()

    def startNewCycle(self):
        self.remaining=self.wallpapers.copy()
        random.shuffle(self.remaining)

        if(self.lastShown is not None and 
           len(self.remaining)>1 and self.remaining[0]==self.lastShown):
            self.remaining[0],self.remaining[1]=(self.remaining[1],self.remaining[0])

    def getNext(self):
        if not self.remaining:
            self.startNewCycle()

        wallpaper=self.remaining.pop()
        self.lastShown=wallpaper
        
        return wallpaper