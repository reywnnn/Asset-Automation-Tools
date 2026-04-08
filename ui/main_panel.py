# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (C) 2026 Pavel Círus, Jan Dvořáček
# Copyright (C) 1996-2026 SCS Software s.r.o.



import bpy

from ..operators.initialize import find_generator_modifier, find_lod_input

SCALE_Y = 1.2


# Main sidebar panel in the 3D Viewport for the SCS Asset Toolkit
class SAT_PT_MAIN(bpy.types.Panel):
    bl_label = "SCS Asset Toolkit"
    bl_idname = "SAT_PT_MAIN"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "SCS Asset Toolkit"

    # Draws the panel UI with links, input mesh selector, preset and initialize button
    def draw(self, context):
        layout = self.layout

        box = layout.box()
        row = box.row(align=True)
        row.scale_y = SCALE_Y
        op = row.operator("sat.open_url", text="Docs", icon='HELP')
        op.url = (
            "https://scssoft.atlassian.net/wiki/spaces/"
            "~712020097edec4c2844607944fbd1e723e72ab/"
            "pages/2002845757/Documentation"
        )
        op.tooltip = "Open the SCS Asset Toolkit documentation"
        op = row.operator("sat.open_url", text="Report", icon='CURRENT_FILE')
        op.url = (
            "https://miro.com/app/board/uXjVGu_mvoU=/"
            "?moveToWidget=3458764664537798733&cot=10"
        )
        op.tooltip = "Report an issue or provide feedback"

        box = layout.box()
        row = box.row(align=True)
        row.label(text="Input Mesh:")
        row.prop(context.scene.sat, "input_mesh", text="")

        row = box.row(align=True)
        row.label(text="Preset:")
        row.prop(context.scene.sat, "preset", text="")

        sat = context.scene.sat
        if sat.input_mesh is None:
            box.label(text="Select an Input Mesh to continue.", icon='INFO')
        if sat.preset == 'NONE':
            box.label(text="Select a Preset to continue.", icon='INFO')

        row = box.row(align=True)
        row.scale_y = SCALE_Y
        row.operator("sat.initialize", icon='MODIFIER')
        row = box.row(align=True)
        row.scale_y = SCALE_Y
        row.operator("sat.clear", icon='TRASH')

        # Show LOD slider and Bake button when generator modifier is applied
        if sat.input_mesh and sat.preset != 'NONE':
            mod = find_generator_modifier(sat.input_mesh)
            if mod and find_lod_input(mod, sat.preset):
                box = layout.box()
                row = box.row(align=True)
                row.scale_y = SCALE_Y
                row.label(text="Level of Detail:")
                sub = row.row(align=True)
                sub.prop(sat, "lod_level", text="")
                row = box.row(align=True)
                row.scale_y = SCALE_Y
                row.operator("sat.bake", icon='OBJECT_DATA')
