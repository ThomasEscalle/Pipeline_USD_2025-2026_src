import ctypes
import time
import os

FindWindowW = ctypes.windll.user32.FindWindowW

file_to_delete = "C:/Mathieu/3D4/Pipe/repository/Pipeline_USD_2025-2026_src/zbrush/ZBrush/Scripts/ZBrushTmp/currentFileName.json"

def zbrush_running():
    hwnd = FindWindowW(None, "ZBrush")
    return hwnd != 0

print("Watching for ZBrush...")
while zbrush_running():
    time.sleep(2)

if os.path.exists(file_to_delete):
    os.remove(file_to_delete)
    print(f"Deleted: {file_to_delete}")
