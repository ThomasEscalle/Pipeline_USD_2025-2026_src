import os

# Base class for file templates
class FileTemplateBase:

    def __init__(self):
        self.template_name = None
        self.template_software = None

    def construct(self, parent, path, origin):
        parent.console.log(f"Constructing the wrong template"
                          f" at path: {path}")
        pass

    # Get the path of a specified entity's master file based on formats and filters
    def getMasterPathFromEntity(self, entity , formats, origin, filters = [ "Publish"]): 

        products = origin.core.products.getProductsFromEntity(entity)

        
        # Get the product that contains "ModL" and "Publish"
        foundProduct = None
        for product in products:
            productType = product["product"]
            # Check if the filter criteria are met
            if all(f in productType for f in filters):
                foundProduct = product
                break

        if foundProduct is not None:
            path = foundProduct["path"]
            exportPath = os.path.join(path, "master")
            exportPath = exportPath.replace("\\", "/")

            # Check if the export path exists
            if os.path.exists(exportPath):
                # Check if there is an abc file in the directory
                abcFiles = [f for f in os.listdir(exportPath) if f.endswith(formats)]

                if abcFiles:
                    # Get the first abc file in the directory
                    ReferenceFile = os.path.join(exportPath, abcFiles[0])
                    ReferenceFile = ReferenceFile.replace("\\", "/")
                    ImportReference = True

        if not ImportReference:
            ImportReference = False
            ReferenceFile = ""

        return ReferenceFile
