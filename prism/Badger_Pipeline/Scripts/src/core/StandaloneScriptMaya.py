import os
import subprocess
from src.core.PathHelper import getMayaPyPath

# This is a class to call maya from a standalone script
class StandaloneScriptMaya:
    def __init__(self, script=None):
        self.script = script
        
        folder = os.path.dirname(__file__)
        folder = os.path.join(folder, "StandaloneScripts")
        
        if not os.path.exists(folder):
            os.makedirs(folder)

        pythonPath = os.path.join(folder, script)

        # Check if the script exists
        if not os.path.exists(pythonPath):
            raise FileNotFoundError(f"The script {script} does not exist in {folder}")
        
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
        mayapyPath = getMayaPyPath()

        if mayapyPath is None:
            raise FileNotFoundError("mayapy.exe not found. Please ensure Maya is installed and the path is set correctly.")

        if not os.path.exists(mayapyPath):
            raise FileNotFoundError(f"mayapy.exe not found in {mayapyPath}")
        
        # Disable the usd plugins loading
        # This is important to be able to load the mayaUsdPlugin
        cenv = os.environ.copy()
        cenv["PYTHONPATH"] = ""
        cenv["PATH"] = ""

        

        # Run the script
        returnvalue = subprocess.run([mayapyPath, self.scriptPath], check=True, env=cenv)

