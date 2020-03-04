# set_viewport_color
Blender Script to Set the Viewport Color based on a nodetree

Select objects and search for "Set Viewport Color"

This takes any of the following nodes in the tree and averages their color input, then set the viewport color of the object to that new color. If a color input is connected, it is ignored. 
* BSDF in the name
* Specular
* Emission
* Ambient Occlusion
* Subsurface Scattering
* RGB

If none of these nodes exist in the tree, the color will be set as full white
