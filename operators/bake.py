# SPDX-License-Identifier: GPL-3.0-or-later
# Author: Pavel Círus



import bpy

from ..core.generator import (
    GEOMETRY_TYPES, LOD_BAKE_MAP,
    find_generator_modifier, find_menu_switch_input,
)



# Operator that bakes all geometry outputs for the selected LOD into named collections.
class AAT_OT_BAKE(bpy.types.Operator):
    bl_idname = "aat.bake"
    bl_label = "Bake Asset"
    bl_description = "Bake all geometry outputs for the selected LOD into named collections"
    bl_options = {'REGISTER', 'UNDO'}

    # Returns a dynamic tooltip explaining why the button may be disabled
    @classmethod
    def description(cls, context, properties):
        aat = context.scene.aat
        if aat.input_mesh is None:
            return "Select an input mesh first"
        if aat.preset == 'NONE':
            return "Select a preset first"
        if find_generator_modifier(aat.input_mesh):
            return "Bake all geometry outputs for the selected LOD"
        return "Initialize the generator first"

    # Disables the button if no mesh is selected, preset is not selected, or preset is not applied
    @classmethod
    def poll(cls, context):
        aat = context.scene.aat
        if aat.input_mesh is None:
            return False
        if aat.preset == 'NONE':
            return False
        return find_generator_modifier(aat.input_mesh) is not None

    # Executes the bake process, iterates through geometry types for the selected LOD
    def execute(self, context):
        aat = context.scene.aat
        obj = aat.input_mesh
        lod = aat.lod_level
        mod = find_generator_modifier(obj)

        menu_input = find_menu_switch_input(mod, aat.preset)
        if menu_input is None:
            self.report({'ERROR'}, "Menu Switch input not found on preset node")
            return {'CANCELLED'}

        original_menu_value = menu_input.default_value

        output_col = self._get_or_create_collection("Output", context.scene.collection)

        types_to_bake = LOD_BAKE_MAP.get(lod, [])
        baked_names = []

        for type_key in types_to_bake:
            menu_value, suffix, col_name, color_tag = GEOMETRY_TYPES[type_key]

            menu_input.default_value = menu_value
            obj.update_tag()
            context.view_layer.update()

            depsgraph = context.evaluated_depsgraph_get()
            eval_obj = obj.evaluated_get(depsgraph)
            mesh = bpy.data.meshes.new_from_object(eval_obj)

            if mesh is None or len(mesh.vertices) == 0:
                if mesh:
                    bpy.data.meshes.remove(mesh)
                continue
            
            expected_attr = f"lod_{lod}_{suffix}"
            if expected_attr not in mesh.attributes:
                bpy.data.meshes.remove(mesh)
                self.report({'WARNING'}, f"Attribute '{expected_attr}' not found, skipping")
                continue

            baked_name = f"{obj.name}_{lod}_{suffix}"
            baked_obj = bpy.data.objects.new(baked_name, mesh)
            baked_obj.matrix_world = obj.matrix_world.copy()

            target_col = self._get_or_create_collection(col_name, output_col, color_tag)
            target_col.objects.link(baked_obj)

            baked_names.append(baked_name)

        menu_input.default_value = original_menu_value
        obj.update_tag()
        context.view_layer.update()

        if baked_names:
            self.report({'INFO'}, f"Baked LOD {lod}: {', '.join(baked_names)}")
        else:
            self.report({'WARNING'}, "No geometry was baked")

        return {'FINISHED'} if baked_names else {'CANCELLED'}

    # Helper method to get or create a collection with the specified name under the given parent collection
    def _get_or_create_collection(self, name, parent, color_tag=None):
        for child in parent.children:
            if child.name == name:
                return child
        col = bpy.data.collections.new(name)
        if color_tag:
            col.color_tag = color_tag
        parent.children.link(col)
        return col
