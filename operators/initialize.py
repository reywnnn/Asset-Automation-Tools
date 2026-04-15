# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (C) 2026 Pavel Círus, Jan Dvořáček
# Copyright (C) 1996-2026 SCS Software s.r.o.



import bpy

from ..core.generator import (
    ASSET_BLEND_PATH, MODIFIER_NAME, NODE_GROUP_NAME,
    find_generator_modifier, set_preset_index,
)



# Operator that loads and applies a Geometry Nodes preset to the input mesh
class SAT_OT_INITIALIZE(bpy.types.Operator):
    bl_idname = "sat.initialize"
    bl_label = "Initialize Generator"
    bl_description = "Apply generator from selected preset to the input mesh"
    bl_options = {'REGISTER', 'UNDO'}

    # Returns a dynamic tooltip explaining why the button may be disabled
    @classmethod
    def description(cls, context, properties):
        sat = context.scene.sat
        if sat.input_mesh is None:
            return "Select an input mesh first"
        if find_generator_modifier(sat.input_mesh):
            return "Generator is already applied on your input mesh"
        return "Apply generator from selected preset to the input mesh"

    # Disables the button if no mesh is selected or preset is already applied
    @classmethod
    def poll(cls, context):
        sat = context.scene.sat
        if sat.input_mesh is None:
            return False
        if sat.preset == 'NONE':
            return False
        if find_generator_modifier(sat.input_mesh):
            return False
        return True

    # Loads the node group from the .blend asset file and adds it as a modifier
    def execute(self, context):
        sat = context.scene.sat
        obj = sat.input_mesh

        if NODE_GROUP_NAME not in bpy.data.node_groups:
            with bpy.data.libraries.load(ASSET_BLEND_PATH) as (data_from, data_to):
                if NODE_GROUP_NAME in data_from.node_groups:
                    data_to.node_groups = [NODE_GROUP_NAME]
                else:
                    self.report({'ERROR'}, f"'{NODE_GROUP_NAME}' not found in asset file")
                    return {'CANCELLED'}

        node_group = bpy.data.node_groups[NODE_GROUP_NAME]

        modifier = obj.modifiers.new(name=MODIFIER_NAME, type='NODES')
        modifier.node_group = node_group

        set_preset_index(obj, sat.preset)

        self.report({'INFO'}, f"Applied '{MODIFIER_NAME}' to '{obj.name}'")
        return {'FINISHED'}
