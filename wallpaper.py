import ctypes
from ctypes import wintypes
from pathlib import Path
import comtypes
from comtypes import IUnknown,GUID,COMMETHOD

class IDesktopWallpaper(IUnknown):
    _iid_=GUID("{B92B56A9-8B55-4E14-9A89-0199BBB6F93B}")
    _methods_=[
        COMMETHOD([],
                  ctypes.HRESULT,"SetWallpaper",
                  (["in"],wintypes.LPCWSTR,"monitorID"),
                  (["in"],wintypes.LPCWSTR,"wallpaper")
                  ),
        COMMETHOD([],ctypes.HRESULT,
                  "GetWallpaper",
                  (["in"],wintypes.LPCWSTR,"monitorID"),
                  (["out"],ctypes.POINTER(wintypes.LPWSTR),"wallpaper")
                  ),
        COMMETHOD([],ctypes.HRESULT,
                  "GetMonitorDevicePathAt",
                  (["in"],wintypes.UINT,"monitorIndex"),
                  (
                      ["out"],ctypes.POINTER(wintypes.LPWSTR),"monitorID")
                 ),
        COMMETHOD(
            [], ctypes.HRESULT,
            "GetMonitorDevicePathCount",
            (
                ["out"],ctypes.POINTER(wintypes.UINT),"count"
            )
        )
    ]

    @classmethod
    def CoCreateInstance(cls):
        clsid=GUID("{C2CF3110-460E-4FC1-B9D0-8A1C0C9CC4BD}")

        return comtypes.CoCreateInstance(clsid,interface=cls)

class Wallpaper:
    def __init__(self):
        self.desktopWallpaper=(IDesktopWallpaper.CoCreateInstance())

    def setWallpaper(self,path):
        try:
            path=str(Path(path).resolve())
            self.desktopWallpaper.SetWallpaper(None,path)
            return True
        except Exception as e:
            print("Wallpaper error:",e)
            return False