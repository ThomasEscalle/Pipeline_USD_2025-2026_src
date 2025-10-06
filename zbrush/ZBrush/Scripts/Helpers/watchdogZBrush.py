import ctypes
import time
import os

FindWindowW = ctypes.windll.user32.FindWindowW

file_to_delete = os.path.dirname(os.path.abspath(__file__)) + os.sep + "ZBrushTmp" + os.sep + "currentFileName.json"
file_to_delete = file_to_delete.replace("\\Helpers", "")

def zbrush_running():
    hwnd = FindWindowW(None, "ZBrush")
    return hwnd != 0

print("Watching for ZBrush...")
while zbrush_running():
    time.sleep(2)

if os.path.exists(file_to_delete):
    os.remove(file_to_delete)
    print(f"Deleted: {file_to_delete}")
