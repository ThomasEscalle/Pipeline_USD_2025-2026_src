import subprocess, time
import http.client, json, base64
import win32gui, win32con, win32process

assetName = "ASSET_NAME"
outputPath = "C:/Mathieu/3D4/prsim_test/Test/03_Production/Assets/CHAR/SlySam/SlySam/Scenefiles/surf/texturing/SlySam_texturing_v0002.spp"    #"OUTPUT_PATH"
typeAsset = "TYPE_ASSET"
importReferencePath = "C:/Mathieu/3D4/prsim_test/Test/03_Production/Assets/CHAR/Dakota/Dakota/Export/Modeling/master/Dakota_Modeling_master.obj"    #"REFERENCE_PATH"


# Launch Painter with remote scripting enabled
proc = subprocess.Popen([
    r"C:/Program Files/Adobe/Adobe Substance 3D Painter/Adobe Substance 3D Painter.exe",
    "--enable-remote-scripting"
])

# Find and hide Painter window
def hide_window(pid):
    def callback(hwnd, pid_to_hide):
        _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
        if found_pid == pid_to_hide:
            win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
    win32gui.EnumWindows(callback, pid)

# Give it some seconds to start fully and open the scripting port
time.sleep(7)

class RemotePainter:
    def __init__(self, host="localhost", port=60041):
        self.host = host
        self.port = port
        self.route = "/run.json"
        self.headers = {"Content-type": "application/json", "Accept": "application/json"}

    def exec_script(self, script_text: str, script_type="python"):
        b64 = base64.b64encode(script_text.encode("utf-8")).decode("utf-8")
        body = {"python": b64} if script_type == "python" else {"js": b64}
        body_bytes = json.dumps(body).encode("utf-8")
        conn = http.client.HTTPConnection(self.host, self.port, timeout=60)
        conn.request("POST", self.route, body_bytes, self.headers)
        resp = conn.getresponse()
        data = resp.read()
        conn.close()
        return data


def build_template():
    painter = RemotePainter()

    script = f"""
import substance_painter.project as project
import substance_painter.application as app
import sys
sys.path.append("C:/Program Files/Prism2/Scripts")

#get the existing prism instance
import PrismInit
core = PrismInit.pcore

# Start a new project with given mesh
project.create("{importReferencePath}")

# Save the project
project.save_as("{outputPath}")

#Resave it with prism API so it get all the prism metadata
try: 
    core.appPlugin.save()
except:
    pass
    
#close Painter
app.close()
"""
    painter.exec_script(script, "python")


if __name__ == "__main__":
    resp = build_template()
