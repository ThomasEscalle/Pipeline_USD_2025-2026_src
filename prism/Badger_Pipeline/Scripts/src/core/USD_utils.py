from src.core.USD_FileTemplate import USDFileTemplate
from src.core.URI_Helper import URI_Helper
from qtpy.QtWidgets import *

import os
import json
import shutil


class USDUtils:

    def createUsdAsset(self, entity, parent):
        # If the asset is a char, item, or prop, create a new USD asset
        self.createUsdItem(entity, parent)


    def createUsdModule(self, entity, parent):
        parent.console.log("Creating USD module for: " + entity["asset"])


        try:
            from pxr import Usd, UsdGeom, Kind, Sdf
        except ImportError as e:
            parent.console.log("Error importing pxr module: %s" % e)
            parent.console.showMessageBoxError("Import Error", "Could not import the 'pxr' module. Please ensure that the USD Python bindings are installed and accessible.")
            return
        
        # Create the USD Product where the USD asset will be created
        # usd_asset stores the path to the created USD asset
        usd_asset = parent.core.products.createProduct(entity, "USD_Asset", "global")


        # Create a publish for "Modu_Publish" with an empty usd file
        master_path_module = self.createEmptyModule(entity, usd_asset, parent.core)

        # Create the asset.usda in the USD_Asset folder, referencing the modu.usda
        self.createModuleAssetFile(entity, usd_asset, master_path_module["usd_file"], parent)




    def createUsdItem(self, entity, parent):
        
        try:
            from pxr import Usd, UsdGeom, Kind, Sdf
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
        master_path_low = self.createAssetModelingLow(entity, usd_asset, parent.core)

        # Create a publish for the modeling high geo
        master_path_high = self.createAssetModelingHigh(entity, usd_asset, parent.core)

        # Create a publish for the surfacing
        master_path_mtl = self.createAssetSurfacing(entity, usd_asset, parent.core)





        # Create the geo.usda
        geo_asset_path = self.createAssetGeo(entity, usd_asset, parent.core, master_path_low["usd_file"], master_path_high["usd_file"], subdirectory = "variant_0")

        # Create the mtl.usda
        mtl_asset_path = self.createAssetMaterial(entity, usd_asset, parent.core, master_path_mtl["usd_file"], subdirectory = "variant_0")


        # Create the asset.usda
        self.createAssetRoot(entity, usd_asset, parent)
        self.createAssetRootSurfacing(entity, usd_asset, parent)

        # Create the usd_info.json
        self.createDefaultAssetJsonDefinition(entity, os.path.join(usd_asset, "usd_info.json") , parent)

        # Create the payload.usda
        payload_variants = [
            {
                "name": "variant_0",
                "geo": geo_asset_path,
                "mtl": mtl_asset_path
            }
        ]
        self.createAssetPayload(entity, usd_asset, parent.core , payload_variants)
        self.createAssetPayloadSurfacing(entity, usd_asset, parent.core , payload_variants)

        pass

    # Create the asset.usda in the USD_Asset folder, referencing the modu.usda
    def createModuleAssetFile(self, entity, assetPath, modu_path , parent):
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

        # Add a reference to the modu.usda
        prim = stage.DefinePrim("/modu_" + entity["asset"])
        prim.GetReferences().AddReference(os.path.relpath(modu_path, assetPath).replace("\\", "/"),primPath="/modu_" + entity["asset"])
        stage.SetDefaultPrim(prim)

        # Save the file
        stage.GetRootLayer().Save()


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


    def createAssetRootSurfacing(self, entity, assetPath, parent):
        try:
            from pxr import Usd, UsdGeom, Kind, Sdf
        except ImportError as e:
            parent.console.log("Error importing pxr module: %s" % e)
            parent.console.showMessageBoxError("Import Error", "Could not import the 'pxr' module. Please ensure that the USD Python bindings are installed and accessible.")
            return

        # Create the USD Stage
        stage = Usd.Stage.CreateNew(os.path.join(assetPath, "asset_surf.usda"))
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
        prim.GetPayloads().AddPayload("./payload_surf.usda")

        # Save the file
        stage.SetDefaultPrim(prim)
        stage.GetRootLayer().Save()


    # Creates a payload file (payload.usda)
    def createAssetPayload(self, entity, assetPath, core , items = []):
        try:
            from pxr import Usd, UsdGeom, Kind, Sdf
        except ImportError as e:
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
                rootVariant.GetReferences().AddReference("./" + relative_geo)
                print("Adding reference to: " + relative_geo + " for item " + name)

                relative_mtl = os.path.relpath(mtl_path, assetPath).replace("\\", "/")
                rootVariant.GetReferences().AddReference("./" + relative_mtl)
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

    # Exactly like the createAssetPayload, but only adds the material reference
    # This is used to reference an asset that only has surfacing to apply the geometry again on an animation
    def createAssetPayloadSurfacing(self, entity, assetPath, core , items = []):
        try:
            from pxr import Usd, UsdGeom, Kind, Sdf
        except ImportError as e:
            return
        
        # Create the USD Stage
        stage = Usd.Stage.CreateNew(os.path.join(assetPath, "payload_surf.usda"))
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
                relative_mtl = os.path.relpath(mtl_path, assetPath).replace("\\", "/")
                rootVariant.GetReferences().AddReference("./" + relative_mtl)
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



    def createAssetGeo(self, entity, assetPath, core , geo_low_path, geo_high_path, subdirectory = ""):
        try:
            from pxr import Usd, UsdGeom, Kind, Sdf
        except ImportError as e:
            return
        
        directory = os.path.join(assetPath, subdirectory)
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Make sure the geo.usda is not in the cache
        path = os.path.join(directory, "geo.usda")
        layer = Sdf.Layer.Find(path)
        if layer:
            print(f"Reusing existing layer at {path}")
            layer.Clear()
            stage = None

        stage = Usd.Stage.CreateNew(path)


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
        # relative_low = os.path.relpath(geo_low_path, directory).replace("\\", "/")
        uri_path = URI_Helper.createFromPath(geo_low_path.replace("\\", "/"), latest_version=True).replace("\\", "/")
        proxy_scope.GetReferences().AddReference(uri_path)




        # Create a "render" scope inside the geo_scope
        render_scope = stage.DefinePrim("/" + entity["asset"] + "/geo/render", "Scope")
        # Set the purpose to "render"
        imageable_API = UsdGeom.Imageable(render_scope)
        purpose_attr = imageable_API.CreatePurposeAttr()
        purpose_attr.Set(UsdGeom.Tokens.render)
        imageable_API.SetProxyPrim(proxy_scope)
        # Add a reference to the geo_high
        uri_path = URI_Helper.createFromPath(geo_high_path.replace("\\", "/"), latest_version=True).replace("\\", "/")
        render_scope.GetReferences().AddReference(uri_path)

        

        # Save the stage
        stage.SetDefaultPrim(prim)
        stage.GetRootLayer().Save()

        # Return the path of the created usd file
        return os.path.join(directory, "geo.usda")

    # Create the asset material
    def createAssetMaterial(self, entity, assetPath, core, mtl_path , subdirectory = ""):
        try:
            from pxr import Usd, UsdGeom, Kind, Sdf
        except ImportError as e:
            return

        # Create a mtl.usda
        directory = os.path.join(assetPath, subdirectory)
        if not os.path.exists(directory):
            os.makedirs(directory)


        # Make sure the mtl.usda is not in the cache
        path = os.path.join(directory, "mtl.usda")
        layer = Sdf.Layer.Find(path)
        if layer:
            print(f"Reusing existing layer at {path}")
            layer.Clear()
            stage = None
        stage = Usd.Stage.CreateNew(path)

        stage.SetFramesPerSecond(24)
        stage.SetTimeCodesPerSecond(24)
        stage.SetMetadata("metersPerUnit", 1)
        stage.SetMetadata("upAxis", "Y")

        # Create a default material
        prim = stage.DefinePrim("/" + entity["asset"])

        # Add a reference to the material
        mtl_uri_path = URI_Helper.createFromPath(mtl_path.replace("\\", "/"), latest_version=True).replace("\\", "/")
        mtl_relative = os.path.relpath(mtl_path, directory).replace("\\", "/")
        prim.GetReferences().AddReference(mtl_uri_path)

        # Save the stage
        stage.SetDefaultPrim(prim)
        stage.GetRootLayer().Save()

        # Open the file with windows
        # os.startfile(os.path.join(assetPath, "mtl.usda"))

        # Return the path of the created usd file
        return os.path.join(directory, "mtl.usda")


    # Create a publish for "Modu_Publish" with an empty usd file
    def createEmptyModule(self, entity, assetPath, core, subdirectory = ""):
        try:
            from pxr import Usd, UsdGeom, Kind, Sdf
        except ImportError as e:
            return {"product": "", "usd_file": ""}
        
        product_path = core.products.createProduct(entity, "Modu_Publish", "global")

        temp_modu_path = os.path.join(assetPath, "modu.usd")

        # Create a usd stage
        stage = Usd.Stage.CreateNew(temp_modu_path)
        stage.SetFramesPerSecond(24)
        stage.SetTimeCodesPerSecond(24)
        stage.SetMetadata("metersPerUnit", 1)
        stage.SetMetadata("upAxis", "Y")

        # Just create an empty xform prim
        xformPrim = UsdGeom.Xform.Define(stage, '/' + entity["asset"] + "_Module")
        stage.SetDefaultPrim(xformPrim.GetPrim())
        stage.GetRootLayer().Save()

        # Clear the stage to release file locks before deletion
        stage = None

        result = core.products.ingestProductVersion([temp_modu_path], entity ,"Modu_Publish")
        master_path_modu = core.products.updateMasterVersion(result["createdFiles"][0])

        # Delete the temporary modu file
        if os.path.exists(temp_modu_path):
            try:
                os.remove(temp_modu_path)
            except PermissionError as e:
                # If we can't delete the file, log a warning but don't fail
                print(f"Warning: Could not delete temporary file {temp_modu_path}: {e}")
            except Exception as e:
                print(f"Warning: Unexpected error deleting temporary file {temp_modu_path}: {e}")

        return {"usd_file" : master_path_modu , "product": product_path}


    def createAssetModelingLow(self, entity, assetPath, core, subdirectory = ""):
        try:
            from pxr import Usd, UsdGeom, Kind, Sdf
        except ImportError as e:
            return {"product": "", "usd_file": ""}
        

        # Create the product in prism
        product_path = core.products.createProduct(entity, "ModL_Publish", "global")

        temp_geo_path = os.path.join(assetPath, "geo_low.usd")
        temp_geo_path = temp_geo_path.replace("\\", "/")




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

        # Clear the stage to release file locks
        stage = None


        result = core.products.ingestProductVersion([temp_geo_path], entity ,"ModL_Publish")
        master_path_low = core.products.updateMasterVersion(result["createdFiles"][0])

        # Delete the temporary geo file
        if os.path.exists(temp_geo_path):
            try:
                os.remove(temp_geo_path)
            except PermissionError as e:
                # If we can't delete the file, log a warning but don't fail
                print(f"Warning: Could not delete temporary file {temp_geo_path}: {e}")
            except Exception as e:
                print(f"Warning: Unexpected error deleting temporary file {temp_geo_path}: {e}")

        return {"usd_file" : master_path_low , "product": product_path}

    def createAssetModelingHigh(self, entity, assetPath, core):
        try:
            from pxr import Usd, UsdGeom, Kind, Sdf
        except ImportError as e:
            return {"product": "", "usd_file": ""}

        # Create the product in prism
        product_path = core.products.createProduct(entity, "ModH_Publish", "global")

        # Create the high-resolution geometry
        temp_geo_path = os.path.join(assetPath, "geo_high.usd")
        temp_geo_path = temp_geo_path.replace("\\", "/")

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

        # Clear the stage to release file locks
        stage = None

        result = core.products.ingestProductVersion([temp_geo_path], entity ,"ModH_Publish")
        master_path_high = core.products.updateMasterVersion(result["createdFiles"][0])

        # Delete the temporary geo file
        if os.path.exists(temp_geo_path):
            try:
                os.remove(temp_geo_path)
            except PermissionError as e:
                # If we can't delete the file, log a warning but don't fail
                print(f"Warning: Could not delete temporary file {temp_geo_path}: {e}")
            except Exception as e:
                print(f"Warning: Unexpected error deleting temporary file {temp_geo_path}: {e}")

        return {"usd_file" : master_path_high , "product": product_path}

    def createAssetSurfacing(self, entity, assetPath, core):
        try:
            from pxr import Usd, UsdGeom, Kind, Sdf, UsdShade
        except ImportError as e:
            return {"product": "", "usd_file": ""}
        
        # Create the product in Prism
        product_path = core.products.createProduct(entity, "Surf_Publish", "global")



        # Create a temporary mtl.usda file
        mtl_temp_path = os.path.join(assetPath, "material.usd")

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

        # Clear the stage to release file locks before deletion
        stage = None

        result = core.products.ingestProductVersion([mtl_temp_path], entity, "Surf_Publish")
        master_path_mtl = core.products.updateMasterVersion(result["createdFiles"][0])

        # Delete the temporary mtl.usda file
        if os.path.exists(mtl_temp_path):
            try:
                os.remove(mtl_temp_path)
            except PermissionError as e:
                # If we can't delete the file, log a warning but don't fail
                print(f"Warning: Could not delete temporary file {mtl_temp_path}: {e}")
            except Exception as e:
                print(f"Warning: Unexpected error deleting temporary file {mtl_temp_path}: {e}")

        return {"usd_file": master_path_mtl, "product": product_path}


    def createDefaultAssetJsonDefinition(self,entity, savePath , parent):
        
        products = parent.core.products.getProductsFromEntity(entity)


        variants = []


        geometry_low = None
        geometry_high = None
        surfacing = None

        i = 0
        # Search for the right product
        for product in products:
            if product["product"] == "ModL_Publish":
                geometry_low = product
            elif product["product"] == "ModH_Publish":
                geometry_high = product
            elif product["product"] == "Surf_Publish":
                surfacing = product
        
        variants.append({
            "geometry_low": geometry_low ,
            "geometry_high": geometry_high ,
            "surfacing": surfacing
        })
        
        result = {"variants" : variants , "entity": entity}

        # Save into json
        # 1. Check if the containing folder exists and create it if necessary
        os.makedirs(os.path.dirname(savePath), exist_ok=True)
        # 2. Write the JSON data to the specified file
        with open(savePath, 'w') as json_file:
            json.dump(result, json_file, indent=4)

        return result
    
    def refreshUsdAssetFromJsonPath(self, jsonPath, core):

        json_file_parent_dir = os.path.dirname(jsonPath)

        data = None
        # Open the JSON file and load its content
        with open(jsonPath, 'r') as json_file:
            data = json.load(json_file)
        if not data:
            print("Error: Could not load JSON data from file: " + jsonPath)
            return
        
        # Get the variants
        variants = data.get("variants", [])
        if not variants:
            print("Error: No variants found in JSON data.")
            return

        # Get the entity
        entity = data.get("entity", None)
        if not entity:
            print("Error: No entity found in JSON data.")
            return


        # Cleaning phase.

        # Delete the payload.usda from the json_file_parent_dir
        payload_usda_path = os.path.join(json_file_parent_dir, "payload.usda")
        if os.path.exists(payload_usda_path):
            try:
                os.remove(payload_usda_path)
            except PermissionError as e:
                print(f"Warning: Could not delete payload file {payload_usda_path}: {e}")
            except Exception as e:
                print(f"Warning: Unexpected error deleting payload file {payload_usda_path}: {e}")

        payload_surf_usda_path = os.path.join(json_file_parent_dir, "payload_surf.usda")
        if os.path.exists(payload_surf_usda_path):
            try:
                os.remove(payload_surf_usda_path)
            except PermissionError as e:
                print(f"Warning: Could not delete payload file {payload_surf_usda_path}: {e}")
            except Exception as e:
                print(f"Warning: Unexpected error deleting payload file {payload_surf_usda_path}: {e}")

                
        # Delete all the subdirectories in the json_file_parent_dir
        for item in os.listdir(json_file_parent_dir):
            item_path = os.path.join(json_file_parent_dir, item)
            if os.path.isdir(item_path):
                # Delete the directory and its content
                shutil.rmtree(item_path)

        index = 0
        payload_variants = []
        for variant in variants:
            
            geo_low = variant.get("geometry_low", None)
            geo_high = variant.get("geometry_high", None)
            surfacing = variant.get("surfacing", None)

            # Check if we were able to find all of the variants
            if not geo_low or not geo_high or not surfacing:
                print("Error: Missing variant data.")
                continue
            

            # Get the prefered file for each component
            geo_low_versions = core.products.getVersionsFromContext(geo_low)
            latest_geo_low_versions = core.products.getLatestVersionFromVersions(geo_low_versions)
            file_geo_low = core.products.getPreferredFileFromVersion(latest_geo_low_versions) if latest_geo_low_versions else ""

            geo_high_versions = core.products.getVersionsFromContext(geo_high)
            latest_geo_high_versions = core.products.getLatestVersionFromVersions(geo_high_versions)
            file_geo_high = core.products.getPreferredFileFromVersion(latest_geo_high_versions) if latest_geo_high_versions else ""

            surfacing_versions = core.products.getVersionsFromContext(surfacing)
            latest_surfacing_versions = core.products.getLatestVersionFromVersions(surfacing_versions)
            file_surfacing = core.products.getPreferredFileFromVersion(latest_surfacing_versions) if latest_surfacing_versions else ""


            subdirectory_name = f"variant_{index}"

            # Create the geo.usda
            geo_asset_path = self.createAssetGeo(entity, json_file_parent_dir, core, file_geo_low, file_geo_high, subdirectory = subdirectory_name)

            # Create the mtl.usda
            mtl_asset_path = self.createAssetMaterial(entity, json_file_parent_dir, core, file_surfacing, subdirectory = subdirectory_name)
    
            payload_variants.append(
                {
                    "name": subdirectory_name,
                    "geo": geo_asset_path,
                    "mtl": mtl_asset_path
                }
            )

            index += 1


        self.createAssetPayload(entity, json_file_parent_dir, core , payload_variants)
        self.createAssetPayloadSurfacing(entity, json_file_parent_dir, core , payload_variants)

        pass
