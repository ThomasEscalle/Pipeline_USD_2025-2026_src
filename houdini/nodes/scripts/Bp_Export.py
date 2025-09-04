import PrismInit
import os
import json
from PySide2.QtCore import QStandardPaths
core = PrismInit.pcore


# Print a error message box
def printError(message):
    hou.ui.displayMessage(message, severity=hou.severityType.Error)


node = hou.pwd()              # <- Current node
stage = node.editableStage()  # <- Current stage

# Get the "USD_ROP" node from the current path
rop = node.parent().node("USD_ROP")
if not rop:
    printError("No 'USD_ROP' node found in the parent network.")
    raise hou.NodeError("No 'USD_ROP' node found in the parent network.")

# Get the current file name
currentFileName = core.getCurrentFileName()
if not currentFileName or currentFileName.strip() == "":
    printError("No current file name found. Please save your Houdini file first.")
    raise hou.NodeError("No current file name found. Please save your Houdini file first.")


# Get the params from the parent
productName = node.parent().parm("productName").eval()    # <- The name of the product we want to publish
comment = node.parent().parm("comment").eval()            # <- The comment we want to add to the version
nextVersion = node.parent().parm("nextVersion").eval()    # <- Boolean if we want to save as a automatic next version
version = node.parent().parm("version").eval()            # <- The version we want to save to (if the nextVersion is False)
updateMaster = node.parent().parm("updateMaster").eval()  # <- Boolean if we want to update the master version
format = node.parent().parm("format").eval()              # <- The format we want to save to (0 = usd , 1 = usda , 2 = usdc)

if not productName or productName.strip() == "":
    printError("No product name specified. Please enter a product name.")
    raise hou.NodeError("No product name specified. Please enter a product name.")




# Convert the format to string
if format == 1:
    format = ".usda"
elif format == 2:
    format = ".usdc"
else:
    format = ".usd"

# Load the entity from the json file
jsonPath = os.path.splitext(currentFileName)[0] + "versioninfo.json"
with open(jsonPath, "r") as f:
    entity = json.load(f)
entity["ProductName"] = productName


# Create the version string that we want to save to
versionSave = core.products.getNextAvailableVersion(entity, productName) #always Modeling because it's for sculpt
if nextVersion == False:
    versionSave = "v" + str(version).zfill(4)


# Generate the output path
exportPath = core.products.generateProductPath(
    task=productName,
    entity=entity,
    extension=format,
    comment=comment,
    version=versionSave,
    location="global",
)

# Get the directory path of the export path
exportPathInfo = os.path.dirname(exportPath)

# If the directory does not exist, create it
if not os.path.exists(exportPathInfo):
    os.makedirs(exportPathInfo)
# Otherwize, we remove all the files in the directory
else:
    files = os.listdir(exportPathInfo)
    for file in files:
        os.remove(exportPathInfo + "/" + file)

# Set the export path to the rop and execute it
node.parent().parm("lopoutput").set(exportPath)
node.parent().parm("execute").pressButton()


#save json info
productContext = entity
productContext["product"] = productName
productContext["version"] = versionSave
productContext["comment"] = comment
productContext["ProductName"] = productName
productContext["sourceScene"] = currentFileName
core.saveVersionInfo(exportPathInfo, productContext)


# Wait until the file is created
while not os.path.exists(exportPath):
    time.sleep(1)

# Update the product with the new version
core.products.updateMasterVersion(exportPath)


# Notify the user that the export is done
hou.ui.displayMessage("Exported USD to:\n" + exportPath, severity=hou.severityType.Message)

