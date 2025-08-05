from src.core.USD_FileTemplate import USDFileTemplate
import os
import json


class USDUtils:

    def createUsdAsset(self, entity, assetPath, parent):
        # Entity contains : {'type': 'asset', 'asset_path': 'Chars/zqdqz', 'asset': 'zqdqz', 'project_path': 'E:\\3D\\PIPELINE\\USD_Uptight_2025_v001\\00_Template\\Uptight', 'project_name': 'Uptight'}

        # If the asset is a char, item, or prop, create a new USD asset
        if "char" in entity["asset_path"].lower() or "item" in entity["asset_path"].lower() or "prop" in entity["asset_path"].lower():
            self.createUsdItem(entity, assetPath, parent)


    def createUsdModule(self, entity, assetPath, parent):
        parent.console.log("Creating USD module for: " + entity["asset"])

        selfPath = os.path.dirname(__file__)
        itemTemplatePath = os.path.join(selfPath, "USD_TEMPLATES", "MODULE")

        # Create a publish for the modu.usda file
        parent.core.products.createProduct(entity, "Modu_Publish", "global")
        # Ingest the new version into prism
        modu_template_path = os.path.join(itemTemplatePath, "modu.usda")
        result = parent.core.products.ingestProductVersion([modu_template_path], entity, "Modu_Publish")
        # Path
        path = result["createdFiles"][0]
        # Open the file, and replace the $$ITEM_NAME$$ with the asset name
        with open(path, "r") as file:
            content = file.read()
        content = content.replace("$$ITEM_NAME$$", entity["asset"])
        # Save the file
        with open(path, "w") as file:
            file.write(content)
        # Update the master version
        master_path = parent.core.products.updateMasterVersion(result["createdFiles"][0])
        parent.console.log("Ingested new version: " + master_path)


        # Create the module.usda
        module = USDFileTemplate(os.path.join(itemTemplatePath, "module.usda"))
        module.replace("$$ITEM_NAME$$", entity["asset"])
        module.replace("$$MODU_PATH$$", master_path.replace("\\", "/"))
        module.save(os.path.join(assetPath, entity["asset"] + ".usda"))

        # Create a "usd_info.txt" file with the asset information
        object = {
            "type": "module",
            "entry_file": entity["asset"] + ".usda"
        }
        strObject = json.dumps(object, indent=4)
        strObject = strObject.replace("'", "\"")
        with open(os.path.join(assetPath, "usd_info.txt"), "w") as info_file:
            info_file.write(strObject)

    def createUsdItem(self, entity, assetPath, parent):
        # Create a new USD item
        
        selfPath = os.path.dirname(__file__)
        itemTemplatePath = os.path.join(selfPath, "USD_TEMPLATES", "ITEM")



        # Create a publish for the modeling low geo
        # Create a new product in Prism
        parent.core.products.createProduct(entity, "ModL_Publish", "global")
        # Ingest the new version into prism
        geo_low_template_path = os.path.join(itemTemplatePath, "geo_low.abc")
        result = parent.core.products.ingestProductVersion([geo_low_template_path], entity ,"ModL_Publish")
        # Path
        path = result["createdFiles"][0]
        # Update the master version
        master_path_low = parent.core.products.updateMasterVersion(result["createdFiles"][0])
        parent.console.log("Ingested new version: " + master_path_low)



        # Create a publish for the modeling high geo
        # Create a new product in Prism
        parent.core.products.createProduct(entity, "ModH_Publish", "global")
        # Ingest the new version into prism
        geo_high_template_path = os.path.join(itemTemplatePath, "geo_high.abc")
        result = parent.core.products.ingestProductVersion([geo_high_template_path], entity, "ModH_Publish")
        # Path
        path = result["createdFiles"][0]
        # Update the master version
        master_path_high = parent.core.products.updateMasterVersion(result["createdFiles"][0])
        parent.console.log("Ingested new version: " + master_path_high)


        # Create a publish for the mtl.usda file
        parent.core.products.createProduct(entity, "Surf_Publish_v001", "global")
        # ingest the new version into prism
        mtl_template_path = os.path.join(itemTemplatePath, "mtl.usda")
        result = parent.core.products.ingestProductVersion([mtl_template_path], entity, "Surf_Publish_v001")
        # Path
        path = result["createdFiles"][0]
        # Open the file, and replace the $$ITEM_NAME$$ with the asset name
        with open(path, "r") as file:
            content = file.read()
        content = content.replace("$$ITEM_NAME$$", entity["asset"])
        # Save the file
        with open(path, "w") as file:
            file.write(content)

        master_path_mtl = parent.core.products.updateMasterVersion(result["createdFiles"][0])
        parent.console.log("Ingested new version: " + master_path_mtl)






        # Create the asset.usda
        asset = USDFileTemplate(os.path.join(itemTemplatePath, "asset.usda"))
        asset.replace("$$ITEM_NAME$$", entity["asset"])
        asset.save(os.path.join(assetPath, entity["asset"] + ".usda"))

        # Create the payload.usda
        payload = USDFileTemplate(os.path.join(itemTemplatePath, "payload.usda"))
        payload.replace("$$ITEM_NAME$$", entity["asset"])
        payload.replace("$$MTL_PATH$$", master_path_mtl.replace("\\", "/"))
        payload.save(os.path.join(assetPath, "payload.usda"))

        # Create the geo.usda
        geo = USDFileTemplate(os.path.join(itemTemplatePath, "geo.usda"))
        geo.replace("$$GEO_LOW_PATH$$", master_path_low)
        geo.replace("$$GEO_HIGH_PATH$$", master_path_high)
        geo.replace("$$ITEM_NAME$$", entity["asset"])

        geo.save(os.path.join(assetPath, "geo.usda"))

        # Create a "usd_info.txt" file with the asset information
        object = {
            "type": "asset",
            "entry_file": entity["asset"] + ".usda"
        }
        strObject = json.dumps(object, indent=4)
        strObject = strObject.replace("'", "\"")  # Replace single quotes with double quotes for JSON compatibility
        with open(os.path.join(assetPath, "usd_info.txt"), "w") as info_file:
            info_file.write(strObject)

        pass

