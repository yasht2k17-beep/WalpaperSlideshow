import tkinter as tk
from tkinter import ttk,filedialog,messagebox
from pathlib import Path
import subprocess
import sys
import ctypes
from ctypes import wintypes

from config import Config

PID_FILE=Path(".slideshow.pid")
MUTEX_NAME="RandomWallpaperSlideshow_GUI"
PROCESS_QUERY_LIMITED_INFORMATION=0x1000
PROCESS_TERMINATE=0x0001
STILL_ACTIVE=259

class WallpaperGUI:
    def __init__(self):
        self.mutex=ctypes.windll.kernel32.CreateMutexW(
            None,False,MUTEX_NAME
        )
        if ctypes.windll.kernel32.GetLastError()==183:
            messagebox.showinfo(
                "Random Wallpaper Slideshow",
                "GUI already running"
            )
            sys.exit()

        self.configManager=Config()
        self.config=self.configManager.load()
        self.process=self.findSlideshowProcess()

        self.root=tk.Tk()
        self.root.title("Random Wallpaper Slideshow")
        self.root.geometry("520x450")
        self.root.resizable(False,False)

        self.buildUI()
        self.updateStatus()

    def buildUI(self):
        padding={"padx":15,"pady":8}
        title=tk.Label(self.root,text="Random Wallpaper Slideshow",font=("Segoe UI",16,"bold"))
        title.pack(pady=15)

        frame=tk.Frame(self.root)
        frame.pack(fill="x")

        tk.Label(
                    frame,text="Wallpaper Folder"
                ).grid(row=0,column=0,sticky="w",**padding)
        
        self.folderVar=tk.StringVar(value=self.config["folder"])

        tk.Entry(
                    frame,textvariable=self.folderVar,width=45
                ).grid(row=1,column=0,**padding)

        tk.Button(
                    frame,text="Browse",command=self.browseFolder
                ).grid(row=1,column=1,padx=5)

        tk.Label(
                    frame,text="Interval(seconds)"
                ).grid(row=2,column=0,sticky="w",**padding)
        
        self.intervalVar=tk.StringVar(value=str(self.config["interval"]))

        tk.Entry(
                    frame,textvariable=self.intervalVar,width=15
                ).grid(row=3,column=0,sticky="w",**padding)

        tk.Label(
                    frame,text="Position"
                ).grid(row=4,column=0,sticky="w",**padding)
        
        self.positionVar=tk.StringVar(value=self.config["position"])

        ttk.Combobox(
                        frame,textvariable=self.positionVar,
                        values=["center","tile","stretch","fit","fill"],
                        state="readonly",width=12
                    ).grid(row=5,column=0,sticky="w",**padding)

        self.statusVar=tk.StringVar()
        tk.Label(self.root,textvariable=self.statusVar,font=("Segoe UI",10)).pack(pady=5)
        
        buttonFrame=tk.Frame(self.root)
        buttonFrame.pack(pady=20)

        tk.Button(buttonFrame,text="Save Settings",command=self.saveSettings,width=16).pack(side="left",padx=5)

        tk.Button(buttonFrame,text="Start Slideshow",command=self.startSlideshow,width=16).pack(side="left",padx=5)
        
        tk.Button(buttonFrame,text="Stop Slideshow",command=self.stopSlideshow,width=16).pack(side="left",padx=5)
        
        tk.Button(self.root,text="Close",command=self.root.destroy,width=16).pack()

    def browseFolder(self):
        folder=filedialog.askdirectory()
        if folder:
            self.folderVar.set(folder)

    def findSlideshowProcess(self):
        if not PID_FILE.exists():
            return None

        try:
            pid=int(PID_FILE.read_text().strip())

        except (ValueError,OSError):
            PID_FILE.unlink(missing_ok=True)
            return None

        if self.isProcessRunning(pid):
            return pid

        PID_FILE.unlink(missing_ok=True)
        return None

    def isSlideshowRunning(self):
        if self.process is None:
            return False

        if self.isProcessRunning(self.process):
            return True

        self.process = None

        try:
            PID_FILE.unlink()
        except FileNotFoundError:
            pass
        return False

    def updateStatus(self):
        if self.isSlideshowRunning():
            self.statusVar.set("Status: Slideshow Running")
        else:
            self.statusVar.set("Status: Slideshow Stopped")

    def saveSettings(self):

        folder = self.folderVar.get().strip()

        if not Path(folder).is_dir():
            messagebox.showerror(
                "Invalid Folder",
                "Please select a valid wallpaper folder."
            )
            return False

        try:
            interval = float(self.intervalVar.get())

            if interval <= 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid Interval",
                "Interval must be greater than 0"
            )
            return False

        position = self.positionVar.get()

        if not position:
            messagebox.showerror(
                "Invalid Position",
                "Please select a wallpaper position"
            )
            return False

        wasRunning = self.isSlideshowRunning()

        if wasRunning:
            self.stopSlideshow(showMessage=False)

        self.config = {
            "folder": folder,
            "interval": interval,
            "position": position
        }

        self.configManager.save(self.config)

        if wasRunning:
            self.startSlideshow(showMessage=False)

        messagebox.showinfo(
            "Settings Saved",
            "Settings saved successfully."
        )

        return True
    
    def startSlideshow(self,showMessage=True):

        if self.isSlideshowRunning():
            if showMessage:
                messagebox.showinfo(
                    "Slideshow","Slideshow is already Running"
                )
            return

        process=subprocess.Popen(
            [sys.executable,"main.py"],
            cwd=Path(__file__).parent
        )

        self.process=process.pid

        PID_FILE.write_text(str(self.process))

        self.updateStatus()

        if showMessage:
            messagebox.showinfo(
                "Slideshow", "Slideshow Started"
            )

    def stopSlideshow(self,showMessage=True):

        if not self.isSlideshowRunning():
            if showMessage:
                messagebox.showinfo(
                    "Slideshow",
                    "No slideshow process is being tracked."
                )
            return

        if self.terminateProcess(self.process):

            self.process = None

            PID_FILE.unlink(missing_ok=True)

            self.updateStatus()

            if showMessage:
                messagebox.showinfo(
                    "Slideshow",
                    "Slideshow Stopped"

                )

        else:

            messagebox.showerror(
                "Slideshow",
                "Failed to stop slideshow."
        )

    def isProcessRunning(self, pid):

        kernel32 = ctypes.windll.kernel32

        kernel32.OpenProcess.argtypes = [
            wintypes.DWORD,
            wintypes.BOOL,
            wintypes.DWORD
        ]
        kernel32.OpenProcess.restype = wintypes.HANDLE

        kernel32.GetExitCodeProcess.argtypes = [
            wintypes.HANDLE,
            ctypes.POINTER(wintypes.DWORD)
        ]
        kernel32.GetExitCodeProcess.restype = wintypes.BOOL

        kernel32.CloseHandle.argtypes = [
            wintypes.HANDLE
        ]
        kernel32.CloseHandle.restype = wintypes.BOOL

        handle = kernel32.OpenProcess(
            PROCESS_QUERY_LIMITED_INFORMATION,
            False,
            int(pid)
        )

        if not handle:
            return False

        exitCode = wintypes.DWORD()

        result = kernel32.GetExitCodeProcess(
            handle,
            ctypes.byref(exitCode)
        )

        kernel32.CloseHandle(handle)

        if not result:
            return False

        return exitCode.value == STILL_ACTIVE

    def terminateProcess(self,pid):
        kernel32=ctypes.windll.kernel32

        handle=kernel32.OpenProcess(
            PROCESS_TERMINATE,False,pid
        )

        if not handle:
            return False

        result=kernel32.TerminateProcess(handle,0)

        kernel32.CloseHandle(handle)

        return bool(result)    
    def run(self):
        self.root.mainloop()

if __name__=="__main__":
    app=WallpaperGUI()
    app.run()