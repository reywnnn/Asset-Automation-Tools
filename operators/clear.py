# SPDX-License-Identifier: GPL-3.0-or-later
# Author: Pavel Círus



import bpy

from ..core.generator import MODIFIER_NAME, find_generator_modifier



# Operator that removes the Geometry Nodes preset modifier from the input mesh
class SAT_OT_CLEAR(bpy.types.Operator):
    bl_idname = "sat.clear"
    bl_label = "Clear Generator"
    bl_description = "Remove the generator applied by SCS Asset Toolkit"
    bl_options = {'REGISTER', 'UNDO'}

    # Returns a dynamic tooltip explaining why the button may be disabled
    @classmethod
    def description(cls, context, properties):
        sat = context.scene.sat
        if sat.input_mesh is None:
            return "Select an input mesh first"
        mod = find_generator_modifier(sat.input_mesh)
        if mod:
            return f"Remove '{MODIFIER_NAME}' from '{sat.input_mesh.name}'"
        return "No generator to remove"

    # Disables the button if no mesh is selected or preset is not applied
    @classmethod
    def poll(cls, context):
        sat = context.scene.sat
        if sat.input_mesh is None:
            return False
        return find_generator_modifier(sat.input_mesh) is not None

    # Removes the matching Geometry Nodes modifier from the input mesh
    def execute(self, context):
        sat = context.scene.sat
        obj = sat.input_mesh
        mod = find_generator_modifier(obj)

        if mod:
            obj.modifiers.remove(mod)
            self.report({'INFO'}, f"Removed '{MODIFIER_NAME}' from '{obj.name}'")
            return {'FINISHED'}

        self.report({'WARNING'}, "No matching generator found")
        return {'CANCELLED'}
