# SPDX-License-Identifier: GPL-3.0-or-later
# Author: Pavel Círus



import bpy

from .core.properties import AAT_PROPERTIES, on_depsgraph_update
from .operators.bake import AAT_OT_BAKE
from .operators.clear import AAT_OT_CLEAR
from .operators.initialize import AAT_OT_INITIALIZE
from .operators.misc.open_url import AAT_OT_OPEN_URL
from .ui.main_panel import AAT_PT_MAIN
 
 
 
# All classes that need to be registered in Blender
classes = (
    AAT_PROPERTIES,
    AAT_OT_BAKE,
    AAT_OT_CLEAR,
    AAT_OT_INITIALIZE,
    AAT_OT_OPEN_URL,
    AAT_PT_MAIN,
)
 
 
# Registers all classes and creates scene properties
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.aat = bpy.props.PointerProperty(type=AAT_PROPERTIES)
    bpy.app.handlers.depsgraph_update_post.append(on_depsgraph_update)
 
 
# Unregisters all classes and removes scene properties
def unregister():
    for handler in list(bpy.app.handlers.depsgraph_update_post):
        if handler.__name__ == "on_depsgraph_update":
            bpy.app.handlers.depsgraph_update_post.remove(handler)
            break
    del bpy.types.Scene.aat
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)