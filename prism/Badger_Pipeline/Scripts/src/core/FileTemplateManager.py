from src.core.FileTemplates.Template_ModLow_Maya import FileTemplateModelingLowMaya
from src.core.FileTemplates.Template_ModHigh_Maya import FileTemplateModelingHighMaya
from src.core.FileTemplates.Template_ModHigh_Houdini import FileTemplateModelingHighHoudini
from src.core.FileTemplates.Template_ModLow_Houdini import FileTemplateModelingLowHoudini
from src.core.FileTemplates.Template_RigLow_Maya import FileTemplateRigLowMaya
from src.core.FileTemplates.Template_RigHigh_Maya import FileTemplateRigHighMaya
from src.core.FileTemplates.Template_Modu_Houdini import FileTemplateModulesHoudini
from src.core.FileTemplates.Template_SetD_Houdini import FileTemplateSetDressHoudini
from src.core.FileTemplates.Template_Surf_Houdini import FileTemplateSurfHoudini
from src.core.FileTemplates.Template_MasterLight_Houdini import FileTemplateMasterLightHoudini
from src.core.FileTemplates.Template_Assembly_Houdini import FileTemplateAssemblyHoudini
from src.core.FileTemplates.Template_Light_Houdini import FileTemplateLightHoudini
from src.core.FileTemplates.Template_TLO_Houdini import FileTemplateTLOHoudini
from src.core.FileTemplates.Template_RLO_Maya import FileTemplateRLOMaya
from src.core.FileTemplates.Template_FLO_Maya import FileTemplateFLOMaya
from src.core.FileTemplates.Template_Anim_Maya import FileTemplateAnimMaya

from src.core.FileTemplates.Template_Autorig_RigLow_01_Maya import FileTemplateAutorigRigLow01Maya
from src.core.FileTemplates.Template_Autorig_RigHigh_01_Maya import FileTemplateAutorigRigHigh01Maya

from src.core.FileTemplateBase import FileTemplateBase

templates = {
            "ModL/Maya" : FileTemplateModelingLowMaya(),
            "ModH/Maya" : FileTemplateModelingHighMaya(),
            "ModL/Houdini" : FileTemplateModelingLowHoudini(),
            "ModH/Houdini" : FileTemplateModelingHighHoudini(),
            "RigL/Maya" : FileTemplateRigLowMaya(),
            "RigH/Maya" : FileTemplateRigHighMaya(),
            "Mod/Houdini" : FileTemplateModulesHoudini(),
            "SetD/Houdini" : FileTemplateSetDressHoudini(),
            "Surf/Houdini" : FileTemplateSurfHoudini(),
            "MLgt/Houdini" : FileTemplateMasterLightHoudini(),
            "rlo/Maya" : FileTemplateRLOMaya(),
            "flo/Maya" : FileTemplateFLOMaya(),
            "anim/Maya" : FileTemplateAnimMaya(), 
            "abl/Houdini" : FileTemplateAssemblyHoudini(),
            "lgt/Houdini" : FileTemplateLightHoudini(),
            "tlo/Houdini" : FileTemplateTLOHoudini(),
            "Surf/Substance" : FileTemplateBase(),  ### <-- TODO,

            "AutorigRigL01/Maya" : FileTemplateAutorigRigLow01Maya(),
            "AutorigRigH01/Maya" : FileTemplateAutorigRigHigh01Maya(),

        }

# Manager for file templates
# This class manages the file templates for different software and types
class FileTemplateManager:

    def getTemplate(self, template_name: str):
        """
        Get the file template by name.
        """
        if template_name in templates:
            return templates[template_name]
        else:
            return None


