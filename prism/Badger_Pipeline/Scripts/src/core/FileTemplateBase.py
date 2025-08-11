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
    def getMatchingProductsFromEntity(self, entity , formats, origin, filters = [ "Publish"] , onlyOne = False): 

        products = origin.core.products.getProductsFromEntity(entity)

        # Get the product that contains "ModL" and "Publish"
        foundProduct = []
        for product in products:
            productType = product["product"]
            # Check if the filter criteria are met
            if all(f in productType for f in filters):

                data = origin.core.products.getVersionsFromContext(product)
                latestVersion = origin.core.products.getLatestVersionFromVersions(data)
                path = origin.core.products.getPreferredFileFromVersion(latestVersion)

                # Check if the file has the right format
                if path is not None and any(path.endswith(fmt) for fmt in formats):
                    foundProduct.append(product)

                    if onlyOne:
                        break

        return foundProduct

    def getPreferedFilePathsFromProductList(self, productList, origin):
        paths = []
        for product in productList:
            data = origin.core.products.getVersionsFromContext(product)
            latestVersion = origin.core.products.getLatestVersionFromVersions(data)
            path = origin.core.products.getPreferredFileFromVersion(latestVersion)
            if path is not None:
                path = path.replace("\\", "/")  # Normalize path for consistency
                paths.append(path)
        return paths
