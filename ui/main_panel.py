# SPDX-License-Identifier: GPL-3.0-or-later
# Author: Pavel Círus



import bpy

from ..core.generator import find_generator_modifier, find_lod_input, find_menu_switch_input



# Main sidebar panel in the 3D Viewport for the Asset Automation Tools
class AAT_PT_MAIN(bpy.types.Panel):
    bl_label = "Asset Automation Tools"
    bl_idname = "AAT_PT_MAIN"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Asset Automation Tools"

    # Draws the UI and its function elements
    def draw(self, context):
        layout = self.layout

        SCALE_Y = 1.2

        box = layout.box()
        row = box.row(align=True)
        row.scale_y = SCALE_Y
        op = row.operator("aat.open_url", text="Docs", icon='HELP')
        op.url = (
            "https://scssoft.atlassian.net/wiki/spaces/"
            "~712020097edec4c2844607944fbd1e723e72ab/"
            "pages/2002845757/Documentation"
        )
        op.tooltip = "Open the Asset Automation Tools documentation"
        op = row.operator("aat.open_url", text="Report", icon='CURRENT_FILE')
        op.url = (
            "https://miro.com/app/board/uXjVGu_mvoU=/"
            "?moveToWidget=3458764664537798733&cot=10"
        )
        op.tooltip = "Report an issue or provide feedback"

        box = layout.box()
        row = box.row(align=True)
        row.label(text="Input Mesh:")
        row.prop(context.scene.aat, "input_mesh", text="")

        row = box.row(align=True)
        row.label(text="Preset:")
        row.prop(context.scene.aat, "preset", text="")

        aat = context.scene.aat

        if aat.input_mesh and aat.preset != 'NONE':
            mod = find_generator_modifier(aat.input_mesh)
            if mod and find_menu_switch_input(mod, aat.preset):
                row = box.row(align=True)
                row.label(text="Preview:")
                row.prop(aat, "geometry_type", text="")

        if aat.input_mesh is None:
            box.label(text="Select an Input Mesh to continue.", icon='INFO')
        if aat.preset == 'NONE':
            box.label(text="Select a Preset to continue.", icon='INFO')

        row = box.row(align=True)
        row.scale_y = SCALE_Y
        row.operator("aat.initialize", icon='MODIFIER')
        row = box.row(align=True)
        row.scale_y = SCALE_Y
        row.operator("aat.clear", icon='TRASH')

        if aat.input_mesh and aat.preset != 'NONE':
            mod = find_generator_modifier(aat.input_mesh)
            if mod and find_lod_input(mod, aat.preset):
                box = layout.box()
                row = box.row(align=True)
                row.scale_y = SCALE_Y
                row.label(text="Level of Detail:")
                sub = row.row(align=True)
                sub.prop(aat, "lod_level", text="")

                row = box.row(align=True)
                row.scale_y = SCALE_Y
                row.operator("aat.bake", icon='OBJECT_DATA')
