import os


def load_stylesheet():
    sFile = os.path.dirname(__file__) + "/ZBrush.qss"
    if not os.path.exists(sFile):
        return ""

    with open(sFile, "r") as f:
        stylesheet = f.read()

    ssheetDir = os.path.dirname(__file__)
    ssheetDir = ssheetDir.replace("\\", "/") + "/"

    repl = {
        "qss:": ssheetDir,
        "@mainBackground1": "rgb(41, 41, 41)",
        "@borders": "rgb(10, 10, 10)",
        "@tableHeader": "rgb(35, 35, 35)",
        "@selectionBackgroundColor": "rgb(255, 144, 38)",
        "@selectionColor": "rgb(10, 10, 10)",
        "@menuhoverbackground": "rgb(62, 62, 62)",
        "@buttonBackgroundDefault": "rgb(62, 62, 62)",
        "@buttonBackgroundDisabled": "rgb(50, 50, 50)",
        "@buttonBackgroundHover": "rgb(70, 70, 70)",
        "@buttonBackgroundBright1": "rgb(80, 80, 80)",
        "@white": "rgb(235, 235, 235)",
        "@tableBackground": "rgb(49, 49, 49)",
        "@test": "rgb(200, 49, 49)",
        "@lightgrey": "rgb(190, 190, 190)",
        "@disabledText": "rgb(120, 120, 120)",
    }

    for key in repl:
        stylesheet = stylesheet.replace(key, repl[key])

    return stylesheet
