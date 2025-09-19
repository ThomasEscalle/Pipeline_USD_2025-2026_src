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
    
    # Retourne le master shot de l'entitée "Current"
    def getCurrentShotMaster(self, entity, origin):
        # Check if the entity has a sequence
        if "sequence" not in entity or entity["sequence"] is None:
            return None

        # Ici, on vas recuperer tous les shots de la sequence.
        all_shots_in_sequence = origin.core.entities.getShotsFromSequence(entity["sequence"])

        # Trouve le shot qui correspond a l'entitée "Current"
        for shot in all_shots_in_sequence:
            if shot["shot"].lower() == "master":
                return shot

        return None


    # Retourne tous les shots depuis la sequence de l'entitée "Current"
    # Retourne un objet comme celui-ci:
    # {
    #     "shots": [list of shots],
    #     "total_frames": total_frames_in_sequence
    #     "number_of_shots": current_entity
    # }
    def getAllShotsFromCurrentSequence(self, entity, origin , includeMaster = False , excludeCurrent = True):
        
        # Check if the entity has a sequence
        if "sequence" not in entity or entity["sequence"] is None:
            return {
                "shots": [],
                "total_frames": 0,
                "number_of_shots": 0
            }

        # Ici, on vas recuperer tous les shots de la sequence.
        all_shots_in_sequence = origin.core.entities.getShotsFromSequence(entity["sequence"])
        shots_in_sequence = []

        # Si on ne veux pas include le master 
        for shot in all_shots_in_sequence:
            if not includeMaster and shot["shot"].lower() == "master":
                continue
            if excludeCurrent and shot["shot"].lower() == entity["shot"].lower():
                continue

            shots_in_sequence.append(shot)



        # Store the total frames of the sequence
        total_frames = 0

        # Get the range and length of each shot and add it to the shot dict
        for shot in shots_in_sequence:
            range = origin.core.entities.getShotRange(shot)
            shot["range"] = range

            length = range[1] - range[0] + 1 # +1 to include the last frame (because the range is inclusive and we start at 1)
            shot["length"] = length
            total_frames += length

            metadata = origin.core.entities.getMetaData(shot)
            shot["metadata"] = metadata
        
        return {
            "shots": shots_in_sequence,
            "total_frames": total_frames,
            "number_of_shots": len(shots_in_sequence)
        }


    # Function to get the details of a shot 
    def getShotDetails(self, entity, origin):
        
        # Get the range of the shot
        range = origin.core.entities.getShotRange(entity)

        # Get the metadata of the shot
        metadata = origin.core.entities.getMetaData(entity)

        # Calculate the length of the shot
        length = range[1] - range[0] + 1  # +1 to include the last frame (because the range is inclusive and we start at 1)

        return {
            "range": range,
            "length": length,
            "metadata": metadata
        }