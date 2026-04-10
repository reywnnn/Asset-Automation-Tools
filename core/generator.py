# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (C) 2026 Pavel Círus, Jan Dvořáček
# Copyright (C) 1996-2026 SCS Software s.r.o.



import os


# Path to the .blend file containing Geometry Nodes presets
ASSET_BLEND_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "assets", "scs_asset_toolkit.blend",
)

# Name of the modifier applied to the object
MODIFIER_NAME = "Generator"

# Node tree datablock loaded from the asset file and assigned to the modifier
NODE_GROUP_NAME = "Presets"

# Preset definitions: 'ENUM_ID': (switch_index, "UI Label", "Description", "Sub-node name")
# switch_index corresponds to the Index Switch node inside the Presets node tree
PRESETS = {
    'HARDSURFACE':  (0, "Hardsurface", "LOD, Shadow & Collision for Hardsurface Assets", "Preset: Hardsurface"),
    'ORGANIC':  (1, "Organic", "LOD, Shadow & Collision for Organic Assets", "Preset: Organic"),
}


# Return the Index Switch value for a preset, or None.
def get_preset_index(preset_key):
    entry = PRESETS.get(preset_key)
    return entry[0] if entry else None


# Set the Index Switch node value in the Presets node tree.
# When preset is NONE, disables the modifier in viewport.
def set_preset_index(obj, preset_key):
    mod = find_generator_modifier(obj)
    if mod is None:
        return
    index = get_preset_index(preset_key)
    if index is None:
        mod.show_viewport = False
        obj.update_tag()
        return
    mod.show_viewport = True
    if mod.node_group is None:
        return
    for node in mod.node_group.nodes:
        if node.bl_idname == 'GeometryNodeIndexSwitch':
            node.inputs[0].default_value = index
            obj.update_tag()
            return


# Return the Generator modifier on obj, or None.
def find_generator_modifier(obj):
    if obj is None:
        return None
    for mod in obj.modifiers:
        if mod.type == 'NODES' and mod.node_group and mod.node_group.name == NODE_GROUP_NAME:
            return mod
    return None


# Find the 'Level of Detail:' input on the preset sub-node within Presets.
def find_lod_input(mod, preset_key):
    entry = PRESETS.get(preset_key)
    if entry is None or mod is None or mod.node_group is None:
        return None
    node_tree_name = entry[3]
    for node in mod.node_group.nodes:
        if node.type == 'GROUP' and node.node_tree and node.node_tree.name == node_tree_name:
            for inp in node.inputs:
                if inp.name == "Level of Detail:":
                    return inp
    return None
