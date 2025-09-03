import os
import sys

core = None

def main():
    import sys
    args = sys.argv[1:]  # first arg is command, second is PRISMROOT
    if not args:
        return
    
    command = args[0]
    prism_root = args[1] if len(args) > 1 else None

    core = getPrismCore(prism_root)
    

def getPrismCore(prismRoot):
    global core
    if core is not None:
        return core
    
    scriptDir = os.path.join(prismRoot, "Scripts")
    if scriptDir not in sys.path:
        sys.path.append(scriptDir)

    import PrismCore
    import importlib
    importlib.reload(PrismCore)

    core = PrismCore.show(app="ZBrush", prismArgs=["loadProject", "noProjectBrowser"])

    return core


if __name__ == "__main__":
    main()


#"C:/Program Files/Prism2/Python311/python.exe" "C:/Mathieu/3D4/Pipe/plugin_zbrush/ZBrush/Scripts/Prism_ZBrush_MenuTools.py" Tools "C:/Program Files/Prism2"