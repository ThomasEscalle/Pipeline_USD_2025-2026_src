import sys


def start_plugin():
    prismInit()


def close_plugin():
    global pcore
    if pcore.appPlugin:
        pcore.appPlugin.unregister()

def prismInit():
    prismRoot = os.getenv("PRISM_ROOT")
    if not prismRoot:
        prismRoot = "C:/Program Files/Prism2"

    scriptDir = os.path.join(prismRoot, "Scripts")

    if scriptDir not in sys.path:
        sys.path.append(scriptDir)

    import PrismCore
    import importlib
    importlib.reload(PrismCore)
    global pcore
    pcore = PrismCore.PrismCore(app="SubstancePainter_tester")
    return pcore


