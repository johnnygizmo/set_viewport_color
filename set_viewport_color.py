import bpy
import numpy
from bpy.types import Menu

bl_info = {
    "name": "Set Viewport Color",
    "description": "Set a viewport color based on materials",
    "author": "Johnny Matthews",
    "version": (1, 5),
    "blender": (2, 82, 0),
    "support": "COMMUNITY",
    "category": "Object"
}



        
class WM_OT_button_context_setviewportcolor(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "wm.set_viewport_color"
    bl_label = "Set Viewport Color"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        for ob in context.selected_editable_objects:
            avg = 0
            ct = 0
            getColorInput = False
            getColorOutput = False
            
            for i in ob.material_slots:
                if i.material.use_nodes == True:
                    avg = 0
                    ct = 0
                    for n in i.material.node_tree.nodes:
                        
                        self.report({'INFO'},n.type)
                        getColorInput = False
                        getColorOutput = False
                        
                        #Nodes with inputs
                        if n.type.find("BSDF") != -1 and n.inputs[0].is_linked == False:
                            getColorInput = True
                        elif n.type == "AMBIENT_OCCLUSION" and n.inputs[0].is_linked == False:
                            self.report({'INFO'},"AA")
                            getColorInput = True                        
                        elif n.type.find("EMISSION") != -1 and n.inputs[0].is_linked == False:
                            getColorInput = True   
                        elif n.type.find("EEVEE_SPECULAR") != -1 and n.inputs[0].is_linked == False:
                            getColorInput = True  
                        elif n.type.find("SUBSURFACE_SCATTERING") != -1 and n.inputs[0].is_linked == False:
                            getColorInput = True      
                            
                        
                        if n.type == "BSDF_PRINCIPLED":
                            bpy.context.object.active_material.metallic = n.inputs["Metallic"].default_value
                            bpy.context.object.active_material.roughness = n.inputs["Roughness"].default_value
                        elif n.type == "BSDF_DIFFUSE":
                            bpy.context.object.active_material.metallic = 0
                            bpy.context.object.active_material.roughness = n.inputs[1].default_value
                        elif n.type == "BSDF_GLASS":
                            bpy.context.object.active_material.metallic = 0
                            bpy.context.object.active_material.roughness = n.inputs[1].default_value
                        elif n.type == "BSDF_GLOSSY":
                            bpy.context.object.active_material.metallic = 0
                            bpy.context.object.active_material.roughness = n.inputs[1].default_value
                        elif n.type == "BSDF_REFRACTION":
                            bpy.context.object.active_material.metallic = 0
                            bpy.context.object.active_material.roughness = n.inputs[1].default_value
                        elif n.type == "EEVEE_SPECULAR":
                            bpy.context.object.active_material.metallic = 0
                            bpy.context.object.active_material.roughness = n.inputs[2].default_value
                        
                                                                                                             
                        #nodes with outputs        
                        if n.type == "RGB":
                            getColorOutput = True     
                            
                        if getColorInput == True:
                            if isinstance(avg,list):
                                avg = n.inputs[0].default_value
                            else:
                                avg = numpy.add(avg,n.inputs[0].default_value)
                                ct = ct + 1                         
                        if getColorOutput == True:
                            if isinstance(avg,list):
                                avg = n.inputs[0].default_value
                            else:
                                avg = numpy.add(avg,n.outputs[0].default_value)
                                ct = ct + 1             
                        
                    if ct == 0:
                        avg = [1,1,1,1]
                    else:
                        avg = numpy.divide(avg,ct)  
                              
                    ob.active_material.diffuse_color = avg
        return {'FINISHED'}    



def draw_menu(self, context):
    layout = self.layout
    layout.separator()
    layout.operator("wm.set_viewport_color",text="Set Viewport Color")


def register():
    bpy.utils.register_class(WM_OT_button_context_setviewportcolor)
    bpy.types.VIEW3D_MT_object_context_menu.append(draw_menu)


def unregister():
    bpy.utils.unregister_class(WM_OT_button_context_setviewportcolor)
    bpy.types.VIEW3D_MT_object_context_menu.remove(draw_menu)


if __name__ == "__main__":
    register()


