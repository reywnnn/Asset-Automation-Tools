# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (C) 2026 Pavel Círus, Jan Dvořáček
# Copyright (C) 1996-2026 SCS Software s.r.o.



import bpy

from .core.properties import SAT_PROPERTIES, on_depsgraph_update
from .operators.bake import SAT_OT_BAKE
from .operators.clear import SAT_OT_CLEAR
from .operators.initialize import SAT_OT_INITIALIZE
from .operators.open_url import SAT_OT_OPEN_URL
from .ui.main_panel import SAT_PT_MAIN
 
 
# All classes that need to be registered in Blender
classes = (
    SAT_PROPERTIES,
    SAT_OT_BAKE,
    SAT_OT_CLEAR,
    SAT_OT_INITIALIZE,
    SAT_OT_OPEN_URL,
    SAT_PT_MAIN,
)
 
 
# Registers all classes and creates scene properties
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.sat = bpy.props.PointerProperty(type=SAT_PROPERTIES)
    bpy.app.handlers.depsgraph_update_post.append(on_depsgraph_update)
 
 
# Unregisters all classes and removes scene properties
def unregister():
    for handler in list(bpy.app.handlers.depsgraph_update_post):
        if handler.__name__ == "on_depsgraph_update":
            bpy.app.handlers.depsgraph_update_post.remove(handler)
            break
    del bpy.types.Scene.sat
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)