import os
import subprocess
from src.core.PathHelper import getHythonPath

# This is a class to call houdini from a standalone script
class StandaloneScriptHoudini:
    def __init__(self, script=None, parent=None):
        self.script = script
        
        folder = os.path.dirname(__file__)
        folder = os.path.join(folder, "StandaloneScripts")
        parent.console.log(f"Folder: {folder}")
        if not os.path.exists(folder):
            os.makedirs(folder)

        pythonPath = os.path.join(folder, script)

        # Check if the script exists
        if not os.path.exists(pythonPath):
            parent.console.log(f"Script {pythonPath} not found")
            return
        
        # Copy the script and rename it to SCRIPT.py
        self.scriptPath = os.path.join(folder, "SCRIPT.py")
        content = ""
        with open(pythonPath, 'r') as original_file:
            content = original_file.read()

        with open(self.scriptPath, 'w') as new_file:
            new_file.write(content)

        


    def replaceVariable(self, variable, value):
        # Replace the variable in the script with the value
        with open(self.scriptPath, 'r') as file:
            content = file.read()
        
        content = content.replace(variable, value)
        
        with open(self.scriptPath, 'w') as file:
            file.write(content)

    def run(self):
        # Run the script in mayapy.exe
        hythonPath = getHythonPath()
        if not os.path.exists(hythonPath):
            raise FileNotFoundError(f"hython.exe not found in {hythonPath}")

        print(f"Running script: {self.scriptPath} with {hythonPath}")
        # Disable the usd plugins loading
        # This is important to be able to load the mayaUsdPlugin
        cenv = os.environ.copy()
        cenv["PYTHONPATH"] = ""
        cenv["PATH"] = ""

        # Run the script
        subprocess.run([hythonPath, self.scriptPath], check=True, env=cenv)
