from src.core.USD_FileTemplate import USDFileTemplate
import os
import json


class USDUtils:

    def createUsdAsset(self, entity, parent):
        # If the asset is a char, item, or prop, create a new USD asset
        self.createUsdItem(entity, parent)


    def createUsdModule(self, entity, parent):
        parent.console.log("Creating USD module for: " + entity["asset"])
        """
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
        """

    def createUsdItem(self, entity, parent):
        try:
            from pxr import Usd, UsdGeom
        except ImportError as e:
            parent.console.log("Error importing pxr module: %s" % e)
            parent.console.showMessageBoxError("Import Error", "Could not import the 'pxr' module. Please ensure that the USD Python bindings are installed and accessible.")
            return
        
        # Create the USD Product where the USD asset will be created
        # usd_asset stores the path to the created USD asset
        usd_asset = parent.core.products.createProduct(entity, "USD_Asset", "global")

        # Get the path where the template items are stored.
        selfPath = os.path.dirname(__file__)
        itemTemplatePath = os.path.join(selfPath, "USD_TEMPLATES", "ITEM")

        
        # Create a publish for the modeling low geo
        master_path_low = self.createAssetModelingLow(entity, usd_asset, parent)

        # Create a publish for the modeling high geo
        master_path_high = self.createAssetModelingHigh(entity, usd_asset, parent)

        # Create a publish for the surfacing
        master_path_mtl = self.createAssetSurfacing(entity, usd_asset, parent)





        # Create the geo.usda
        geo_asset_path = self.createAssetGeo(entity, usd_asset, parent, master_path_low["usd_file"], master_path_high["usd_file"], subdirectory = "default")

        # Create the mtl.usda
        mtl_asset_path = self.createAssetMaterial(entity, usd_asset, parent, master_path_mtl["usd_file"], subdirectory = "default")


        # Create the asset.usda
        self.createAssetRoot(entity, usd_asset, parent)

        # Create the usd_info.json
        self.createAssetJsonDefinition([{"geometry_low" : master_path_low["product"] , "geometry_high" : master_path_high["product"], "surfacing" : master_path_mtl["product"]}], os.path.join(usd_asset, "usd_info.json")  )

        # Create the payload.usda
        payload_variants = [
            {
                "name": "variant_00",
                "geo": geo_asset_path,
                "mtl": mtl_asset_path
            },
            {
                "name": "variant_01",
                "geo": geo_asset_path,
                "mtl": mtl_asset_path
            }
        ]
        self.createAssetPayload(entity, usd_asset, parent , payload_variants)

        pass



    # Creates a root asset file (asset.usda)
    def createAssetRoot(self, entity, assetPath, parent):
        try:
            from pxr import Usd, UsdGeom, Kind, Sdf
        except ImportError as e:
            parent.console.log("Error importing pxr module: %s" % e)
            parent.console.showMessageBoxError("Import Error", "Could not import the 'pxr' module. Please ensure that the USD Python bindings are installed and accessible.")
            return

        # Create the USD Stage
        stage = Usd.Stage.CreateNew(os.path.join(assetPath, "asset.usda"))
        stage.SetFramesPerSecond(24)
        stage.SetTimeCodesPerSecond(24)
        stage.SetMetadata("metersPerUnit", 1)
        stage.SetMetadata("upAxis", "Y")

        # Create a xForm 
        prim = stage.DefinePrim("/" + entity["asset"], "Xform")
        prim.SetTypeName("Xform")

        # Apply the GeomModelAPI
        prim.ApplyAPI("GeomModelAPI") # Older USD versions: prim.ApplyAPI("UsdGeomModelAPI")

        # Add the asset information
        prim.SetAssetInfoByKey("name", entity["asset"])
        prim.SetAssetInfoByKey("thumbnail", Sdf.AssetPath("./thumbnail.png"))
        prim.SetAssetInfoByKey("identifier", Sdf.AssetPath("./" + entity["asset"] + ".usda"))

        # Set the kind to component
        model_API = Usd.ModelAPI(prim)
        model_API.SetKind(Kind.Tokens.component) # Set the kind to component

        # Add a payload to the payload.usda file
        prim.GetPayloads().AddPayload("./payload.usda")

        # Save the file
        stage.SetDefaultPrim(prim)
        stage.GetRootLayer().Save()

    # Creates a payload file (payload.usda)
    def createAssetPayload(self, entity, assetPath, parent , items = []):
        try:
            from pxr import Usd, UsdGeom, Kind, Sdf
        except ImportError as e:
            parent.console.log("Error importing pxr module: %s" % e)
            parent.console.showMessageBoxError("Import Error", "Could not import the 'pxr' module. Please ensure that the USD Python bindings are installed and accessible.")
            return
        
        # Create the USD Stage
        stage = Usd.Stage.CreateNew(os.path.join(assetPath, "payload.usda"))
        stage.SetFramesPerSecond(24)
        stage.SetTimeCodesPerSecond(24)
        stage.SetMetadata("metersPerUnit", 1)
        stage.SetMetadata("upAxis", "Y")

        # Create a simple primitive 
        prim = stage.DefinePrim("/" + entity["asset"])

        # Set the kind to component
        model_API = Usd.ModelAPI(prim)
        model_API.SetKind(Kind.Tokens.component) # Set the kind to component


        variant_sets_api = prim.GetVariantSets()

        variant_set_api = variant_sets_api.AddVariantSet("variant", position=Usd.ListPositionBackOfPrependList)
        


        # Iterate over the items and add the variants
        index = 0
        for item in items:
            name = item["name"]
            geo_path = item["geo"]
            mtl_path = item["mtl"]

            # Check if the items are not empty
            if geo_path == "" or mtl_path == "":
                continue
            variant_set_api.AddVariant(name)
            variant_set_api.SetVariantSelection(name)

            # Create a "Asset_root" 
            with variant_set_api.GetVariantEditContext():
                # Anything we write in the context, goes into the variant (prims and properties)
                rootVariant = stage.DefinePrim("/" + entity["asset"] + "/Asset_root")

                # Add the references, relative to the current directory
                relative_geo = os.path.relpath(geo_path, assetPath).replace("\\", "/")
                rootVariant.GetReferences().AddReference(relative_geo)
                print("Adding reference to: " + relative_geo + " for item " + name)

                relative_mtl = os.path.relpath(mtl_path, assetPath).replace("\\", "/")
                rootVariant.GetReferences().AddReference(relative_mtl)
                print("Adding reference to: " + relative_mtl + " for item " + name)

            index += 1


        # If there are item, set the variant selection to the first item's name
        if items:
            variant_set_api.SetVariantSelection(items[0]["name"])

        # Add references to the geo and the material
        # prim.GetReferences().AddReference("./geo.usda")
        # prim.GetReferences().AddReference("./mtl.usda")

        # Save the file
        stage.SetDefaultPrim(prim)
        stage.GetRootLayer().Save()

    def createAssetGeo(self, entity, assetPath, parent , geo_low_path, geo_high_path, subdirectory = ""):
        try:
            from pxr import Usd, UsdGeom, Kind, Sdf
        except ImportError as e:
            parent.console.log("Error importing pxr module: %s" % e)
            parent.console.showMessageBoxError("Import Error", "Could not import the 'pxr' module. Please ensure that the USD Python bindings are installed and accessible.")
            return
        
        directory = os.path.join(assetPath, subdirectory)
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Create the geo.usda
        stage = Usd.Stage.CreateNew(os.path.join(directory, "geo.usda"))
        stage.SetFramesPerSecond(24)
        stage.SetTimeCodesPerSecond(24)
        stage.SetMetadata("metersPerUnit", 1)
        stage.SetMetadata("upAxis", "Y")


        # Create a xform
        prim = stage.DefinePrim("/" + entity["asset"], "Xform")
        # Set the kind to component
        model_API = Usd.ModelAPI(prim)
        model_API.SetKind(Kind.Tokens.component)  # Set the kind to component


        ### Transform the component by 0.01 to convert from cm to m
        # Set local transform of leaf prim
        root_xformable = UsdGeom.Xformable(prim)
        scale_transform = root_xformable.AddScaleOp(opSuffix='cm_to_m')
        scale_transform.Set(value=(0.01, 0.01, 0.01))

        # Create a "geo" Scope in the root
        geo_scope = stage.DefinePrim("/" + entity["asset"] + "/geo", "Scope")
        # Apply the GeomModelAPI
        geo_scope.ApplyAPI("GeomModelAPI") # Older USD versions: prim.ApplyAPI("UsdGeomModelAPI")
        # Set the purpose to "default"
        #  UsdGeom.Tokens.render        UsdGeom.Tokens.proxy   UsdGeom.Tokens.default_    UsdGeom.Tokens.invisible
        imageable_API = UsdGeom.Imageable(geo_scope)
        purpose_attr = imageable_API.CreatePurposeAttr()
        purpose_attr.Set(UsdGeom.Tokens.default_)



        # Create a "proxy" scope inside the geo_scope
        proxy_scope = stage.DefinePrim("/" + entity["asset"] + "/geo/proxy", "Scope")
        # Set the purpose to "proxy"
        imageable_API = UsdGeom.Imageable(proxy_scope)
        purpose_attr = imageable_API.CreatePurposeAttr()
        purpose_attr.Set(UsdGeom.Tokens.proxy)
        # Add a reference to the geo_low
        relative_low = os.path.relpath(geo_low_path, directory).replace("\\", "/")
        proxy_scope.GetReferences().AddReference(relative_low)




        # Create a "render" scope inside the geo_scope
        render_scope = stage.DefinePrim("/" + entity["asset"] + "/geo/render", "Scope")
        # Set the purpose to "render"
        imageable_API = UsdGeom.Imageable(render_scope)
        purpose_attr = imageable_API.CreatePurposeAttr()
        purpose_attr.Set(UsdGeom.Tokens.render)
        imageable_API.SetProxyPrim(proxy_scope)
        # Add a reference to the geo_high
        relative_high = os.path.relpath(geo_high_path, directory).replace("\\", "/")
        render_scope.GetReferences().AddReference(relative_high)

        

        # Save the stage
        stage.SetDefaultPrim(prim)
        stage.GetRootLayer().Save()

        # Return the path of the created usd file
        return os.path.join(directory, "geo.usda")

    # Create the asset material
    def createAssetMaterial(self, entity, assetPath, parent, mtl_path , subdirectory = ""):
        try:
            from pxr import Usd, UsdGeom, Kind, Sdf
        except ImportError as e:
            parent.console.log("Error importing pxr module: %s" % e)
            parent.console.showMessageBoxError("Import Error", "Could not import the 'pxr' module. Please ensure that the USD Python bindings are installed and accessible.")
            return

        # Create a mtl.usda
        directory = os.path.join(assetPath, subdirectory)
        if not os.path.exists(directory):
            os.makedirs(directory)

        stage = Usd.Stage.CreateNew(os.path.join(directory, "mtl.usda"))
        stage.SetFramesPerSecond(24)
        stage.SetTimeCodesPerSecond(24)
        stage.SetMetadata("metersPerUnit", 1)
        stage.SetMetadata("upAxis", "Y")

        # Create a default material
        prim = stage.DefinePrim("/" + entity["asset"])

        # Add a reference to the material
        mtl_relative = os.path.relpath(mtl_path, directory).replace("\\", "/")
        prim.GetReferences().AddReference(mtl_relative)

        # Save the stage
        stage.SetDefaultPrim(prim)
        stage.GetRootLayer().Save()

        # Open the file with windows
        # os.startfile(os.path.join(assetPath, "mtl.usda"))

        # Return the path of the created usd file
        return os.path.join(directory, "mtl.usda")

    def createAssetModelingLow(self, entity, assetPath, parent, subdirectory = ""):
        try:
            from pxr import Usd, UsdGeom, Kind, Sdf
        except ImportError as e:
            parent.console.log("Error importing pxr module: %s" % e)
            parent.console.showMessageBoxError("Import Error", "Could not import the 'pxr' module. Please ensure that the USD Python bindings are installed and accessible.")
            return {"product": "", "usd_file": ""}
        

        # Create the product in prism
        product_path = parent.core.products.createProduct(entity, "ModL_Publish", "global")

        temp_geo_path = os.path.join(assetPath, "geo_low.usda")

        # Create a usd stage
        stage = Usd.Stage.CreateNew(temp_geo_path)
        stage.SetFramesPerSecond(24)
        stage.SetTimeCodesPerSecond(24)
        stage.SetMetadata("metersPerUnit", 1)
        stage.SetMetadata("upAxis", "Y")

        # Create a cube for now
        xformPrim = UsdGeom.Xform.Define(stage, '/Cube_Low')
        cubePrim = UsdGeom.Cube.Define(stage, '/Cube_Low/Cube_Prim')

        stage.SetDefaultPrim(xformPrim.GetPrim())
        stage.GetRootLayer().Save()


        result = parent.core.products.ingestProductVersion([temp_geo_path], entity ,"ModL_Publish")
        master_path_low = parent.core.products.updateMasterVersion(result["createdFiles"][0])

        # Delete the temporary geo file
        if os.path.exists(temp_geo_path):
            os.remove(temp_geo_path)

        return {"usd_file" : master_path_low , "product": product_path}

    def createAssetModelingHigh(self, entity, assetPath, parent):
        try:
            from pxr import Usd, UsdGeom, Kind, Sdf
        except ImportError as e:
            parent.console.log("Error importing pxr module: %s" % e)
            parent.console.showMessageBoxError("Import Error", "Could not import the 'pxr' module. Please ensure that the USD Python bindings are installed and accessible.")
            return {"product": "", "usd_file": ""}

        # Create the product in prism
        product_path = parent.core.products.createProduct(entity, "ModH_Publish", "global")

        # Create the high-resolution geometry
        temp_geo_path = os.path.join(assetPath, "geo_high.usda")

        # Create a usd stage
        stage = Usd.Stage.CreateNew(temp_geo_path)
        stage.SetFramesPerSecond(24)
        stage.SetTimeCodesPerSecond(24)
        stage.SetMetadata("metersPerUnit", 1)
        stage.SetMetadata("upAxis", "Y")

        # Create a sphere for now
        xformPrim = UsdGeom.Xform.Define(stage, '/Sphere_High')
        spherePrim = UsdGeom.Sphere.Define(stage, '/Sphere_High/Sphere_Prim')

        stage.SetDefaultPrim(xformPrim.GetPrim())
        stage.GetRootLayer().Save()


        result = parent.core.products.ingestProductVersion([temp_geo_path], entity ,"ModH_Publish")
        master_path_high = parent.core.products.updateMasterVersion(result["createdFiles"][0])

        # Delete the temporary geo file
        if os.path.exists(temp_geo_path):
            os.remove(temp_geo_path)

        return {"usd_file" : master_path_high , "product": product_path}

    def createAssetSurfacing(self, entity, assetPath, parent):
        try:
            from pxr import Usd, UsdGeom, Kind, Sdf, UsdShade
        except ImportError as e:
            parent.console.log("Error importing pxr module: %s" % e)
            parent.console.showMessageBoxError("Import Error", "Could not import the 'pxr' module. Please ensure that the USD Python bindings are installed and accessible.")
            return {"product": "", "usd_file": ""}
        
        # Create the product in Prism
        product_path = parent.core.products.createProduct(entity, "Surf_Publish", "global")



        # Create a temporary mtl.usda file
        mtl_temp_path = os.path.join(assetPath, "material.usda")

        # Create a usd stage
        stage = Usd.Stage.CreateNew(mtl_temp_path)
        stage.SetFramesPerSecond(24)
        stage.SetTimeCodesPerSecond(24)
        stage.SetMetadata("metersPerUnit", 1)
        stage.SetMetadata("upAxis", "Y")

        over_root = stage.OverridePrim('/' + entity["asset"]) # Override the Entity's asset 



        # Create a "material" scope inside the overridden root
        material_scope = stage.DefinePrim(over_root.GetPath().AppendChild("materials"), "Scope")

        # todo : Create a basic material
        material = UsdShade.Material.Define(stage, material_scope.GetPath().AppendChild("Mtl_Red"))

        pbrShader = UsdShade.Shader.Define(stage, material.GetPath().AppendChild("PBRShader_red"))
        pbrShader.CreateIdAttr("UsdPreviewSurface")
        pbrShader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set((1.0, 0.0, 0.0))
        pbrShader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.4)
        pbrShader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.0)

        material.CreateSurfaceOutput().ConnectToSource(pbrShader.ConnectableAPI(), "surface")



        # Bind materials via direct binding
        material = UsdShade.Material(material)



        # Create a override of the geo in the overriden root
        geo_override = stage.OverridePrim("/" + entity["asset"] + "/geo")

        # Create an override of the "proxy" in the overriden geo
        proxy_override = stage.OverridePrim(geo_override.GetPath().AppendChild("proxy"))
        proxy_override.ApplyAPI("MaterialBindingAPI")
        mat_bind_api = UsdShade.MaterialBindingAPI.Apply(proxy_override)  # Apply the material to the geo
        mat_bind_api.Bind(material)

        # Create an override of the "render" in the overridden geo
        render_override = stage.OverridePrim(geo_override.GetPath().AppendChild("render"))
        render_override.ApplyAPI("MaterialBindingAPI")
        mat_bind_api = UsdShade.MaterialBindingAPI.Apply(render_override) # Apply the material to the geo
        mat_bind_api.Bind(material)

        stage.SetDefaultPrim(over_root)
        stage.GetRootLayer().Save()


        result = parent.core.products.ingestProductVersion([mtl_temp_path], entity, "Surf_Publish")
        master_path_mtl = parent.core.products.updateMasterVersion(result["createdFiles"][0])

        # Delete the temporary mtl.usda file
        if os.path.exists(mtl_temp_path):
            os.remove(mtl_temp_path)

        return {"usd_file": master_path_mtl, "product": product_path}


    def createAssetJsonDefinition(self,assetPaths, savePath):

        variants = []

        if not assetPaths:
            variants = []
        else:
            for item in assetPaths:
                geometry_low = item.get("geometry_low")
                geometry_high = item.get("geometry_high")
                surfacing = item.get("surfacing")

                # Get the relative path from the save path to the geometry low
                relative_low = os.path.relpath(geometry_low, os.path.dirname(savePath))
                relative_high = os.path.relpath(geometry_high, os.path.dirname(savePath))
                relative_mtl = os.path.relpath(surfacing, os.path.dirname(savePath))

                relative_low = relative_low.replace("\\", "/")
                relative_high = relative_high.replace("\\", "/")
                relative_mtl = relative_mtl.replace("\\", "/")

                variants.append({
                    "geometry_low": relative_low if relative_low else geometry_low,
                    "geometry_high": relative_high if relative_high else geometry_high,
                    "surfacing": relative_mtl if relative_mtl else surfacing
                })
        
        result = {"variants" : variants}

        # Save into json
        # 1. Check if the containing folder exists and create it if necessary
        os.makedirs(os.path.dirname(savePath), exist_ok=True)
        # 2. Write the JSON data to the specified file
        with open(savePath, 'w') as json_file:
            json.dump(result, json_file, indent=4)

        return result
