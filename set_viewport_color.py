import bpy
import numpy

bl_info = {
    "name": "Set Viewport Color",
    "description": "Set a viewport color based on materials",
    "author": "Johnny Matthews",
    "version": (1, 1),
    "blender": (2, 82, 0),
    "support": "COMMUNITY",
    "category": "Object"
}


def main(context):
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
                    print(n.name)
                    
                    getColorInput = False
                    getColorOutput = False
                    
                    if n.name.find("BSDF") != -1:
                        getColorInput = True
                    if n.name == "RGB":
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
        
class SetViewportColor(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.set_viewport_color"
    bl_label = "Set Viewport Color"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(SetViewportColor)


def unregister():
    bpy.utils.unregister_class(SetViewportColor)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.set_viewport_color()
