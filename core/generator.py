# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (C) 2026 Pavel Círus, Jan Dvořáček
# Copyright (C) 1996-2026 SCS Software s.r.o.



import os



ASSET_BLEND_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "assets", "scs_asset_toolkit.blend",
)


MODIFIER_NAME = "Generator"


NODE_GROUP_NAME = "Presets"


# Format: (index, display_name, description, node_tree_name)
PRESETS = {
    'HARDSURFACE':  (0, "Hardsurface",  "LOD, Shadow & Collision for Hardsurface Assets",   "Preset: Hardsurface"),
    'ORGANIC':      (1, "Organic",      "LOD, Shadow & Collision for Organic Assets",       "Preset: Organic"),
}


# Format: (display_name, suffix, socket_name, color_tag)
GEOMETRY_TYPES = {
    'VISUAL':    ("Visual",    "vis",  "Visual",    'COLOR_02'),
    'SHADOW':    ("Shadow",    "shw",  "Shadow",    'COLOR_05'),
    'COLLISION': ("Collision", "coll", "Collision", 'COLOR_04'),
}


# Maps each LOD level to the geometry types that should be baked for it.
LOD_BAKE_MAP = {
    0: ['VISUAL', 'SHADOW', 'COLLISION'],
    1: ['VISUAL', 'SHADOW'],
    2: ['VISUAL', 'SHADOW'],
}


# Returns preset index (first value) from PRESETS dict by key, or None if not found
def get_preset_index(preset_key):
    entry = PRESETS.get(preset_key)
    return entry[0] if entry else None


# Sets preset index on Geometry Nodes modifier (Index Switch), or disables modifier if preset is invalid
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


# Finds and returns the Geometry Nodes modifier with the specified node group, or None if not found
def find_generator_modifier(obj):
    if obj is None:
        return None
    for mod in obj.modifiers:
        if mod.type == 'NODES' and mod.node_group and mod.node_group.name == NODE_GROUP_NAME:
            return mod
    return None


# Finds and returns the LOD level input socket in the Geometry Nodes modifier for the specified preset, or None if not found
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


# Finds and returns the menu switch input socket in the Geometry Nodes modifier for the specified preset, or None if not found
def find_menu_switch_input(mod, preset_key):
    entry = PRESETS.get(preset_key)
    if entry is None or mod is None or mod.node_group is None:
        return None
    node_tree_name = entry[3]
    for node in mod.node_group.nodes:
        if node.type == 'GROUP' and node.node_tree and node.node_tree.name == node_tree_name:
            for inner_node in node.node_tree.nodes:
                if inner_node.bl_idname == 'GeometryNodeMenuSwitch':
                    return inner_node.inputs[0]
    return None
