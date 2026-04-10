# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (C) 2026 Pavel Círus, Jan Dvořáček
# Copyright (C) 1996-2026 SCS Software s.r.o.



import bpy

from .generator import (
    PRESETS,
    find_generator_modifier, find_lod_input, set_preset_index,
)


# Filter function that only allows mesh objects linked to the scene
def mesh_poll(self, object):
    return object.type == 'MESH' and object.name in bpy.context.scene.objects


# Syncs lod_level property value to the Geometry Nodes modifier socket
def lod_level_update(self, context):
    obj = self.input_mesh
    if obj is None:
        return
    mod = find_generator_modifier(obj)
    if mod is None:
        return
    lod_input = find_lod_input(mod, self.preset)
    if lod_input:
        lod_input.default_value = self.lod_level
        obj.update_tag()


# Switches the active preset on the Index Switch node when the user changes selection
def preset_update(self, context):
    obj = self.input_mesh
    if obj is None:
        return
    set_preset_index(obj, self.preset)


# Syncs modifier socket value back to lod_level property on depsgraph updates
def on_depsgraph_update(scene, depsgraph):
    sat = scene.sat
    obj = sat.input_mesh
    if obj is None:
        return
    mod = find_generator_modifier(obj)
    if mod is None:
        return
    lod_input = find_lod_input(mod, sat.preset)
    if lod_input:
        val = int(lod_input.default_value)
        if sat.lod_level != val:
            sat["lod_level"] = val


# Stores all addon properties accessible via context.scene.sat
class SAT_PROPERTIES(bpy.types.PropertyGroup):
    input_mesh: bpy.props.PointerProperty(
        type=bpy.types.Object,
        name="Input Mesh",
        description="Select a mesh object",
        poll=mesh_poll,
    ) # type: ignore

    preset: bpy.props.EnumProperty(
        name="Preset",
        description="Select a Generator Preset",
        items=[
            ('NONE', "None", "No preset selected"),
        ] + [(key, val[1], val[2]) for key, val in PRESETS.items()],
        default='NONE',
        update=preset_update,
    ) # type: ignore

    lod_level: bpy.props.IntProperty(
        name="Level of Detail",
        description="Move slider to change Level of Detail",
        default=0,
        min=0,
        max=2,
        update=lod_level_update,
    ) # type: ignore
