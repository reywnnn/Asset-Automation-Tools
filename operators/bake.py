# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (C) 2026 Pavel Círus, Jan Dvořáček
# Copyright (C) 1996-2026 SCS Software s.r.o.



import bpy

from ..core.generator import find_generator_modifier


# Operator that bakes the output mesh from the generator modifier into a new collection
class SAT_OT_BAKE(bpy.types.Operator):
    bl_idname = "sat.bake"
    bl_label = "Bake Asset"
    bl_description = "Bake the generator output into a new mesh in the Output collection"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def description(cls, context, properties):
        sat = context.scene.sat
        if sat.input_mesh is None:
            return "Select an input mesh first"
        if sat.preset == 'NONE':
            return "Select a preset first"
        if find_generator_modifier(sat.input_mesh):
            return "Bake the generator output into a new mesh in the Output collection"
        return "Initialize the generator first"

    @classmethod
    def poll(cls, context):
        sat = context.scene.sat
        if sat.input_mesh is None:
            return False
        if sat.preset == 'NONE':
            return False
        return find_generator_modifier(sat.input_mesh) is not None

    def execute(self, context):
        sat = context.scene.sat
        obj = sat.input_mesh

        # Evaluate the mesh with all modifiers applied
        depsgraph = context.evaluated_depsgraph_get()
        eval_obj = obj.evaluated_get(depsgraph)
        mesh = bpy.data.meshes.new_from_object(eval_obj)

        baked_obj = bpy.data.objects.new(f"{obj.name}_vis_lod{sat.lod_level}", mesh)

        # Create Output collection hierarchy with color tags
        output_col = self._get_or_create_collection("Output", context.scene.collection)
        visual_col = self._get_or_create_collection("Visual", output_col, 'COLOR_02')
        self._get_or_create_collection("Shadow", output_col, 'COLOR_05')
        self._get_or_create_collection("Collision", output_col, 'COLOR_04')

        visual_col.objects.link(baked_obj)

        self.report({'INFO'}, f"Baked '{obj.name}' into Output / Visual")
        return {'FINISHED'}

    def _get_or_create_collection(self, name, parent, color_tag=None):
        for child in parent.children:
            if child.name == name:
                return child
        col = bpy.data.collections.new(name)
        if color_tag:
            col.color_tag = color_tag
        parent.children.link(col)
        return col
