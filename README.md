# SCS Asset Toolkit

Blender add-on for automated game asset optimization.

**SCS Asset Toolkit** is a procedural toolkit built for Blender that automates creation of:

- Level of Detail meshes
- **Shadow Meshes**
- **Collision Meshes**
- Validation / debug checks before generation

The goal is simple:

> **Turn high-quality source meshes into optimized in-game assets with minimal manual work, while preserving shading, topology integrity, and asset-specific requirements.**

---

## Features

### Automated LOD Generation
Generate multiple optimization levels directly from a source mesh:

- LOD1
- LOD2
- LOD3
- LOD4

---

### Shadow Mesh Generation
Automatically generates simplified shadow casting geometry:

- preserves silhouette where needed
- removes unnecessary detail
- optimized for runtime rendering

---

### Collision Mesh Generation
Creates gameplay / physics collision meshes:

- simplified topology

---

### Validation & Debug
Toolkit validates source geometry before generation:

Checks include:

- non-manifold geometry
- mesh errors
- invalid topology
- problematic shading situations
- unsupported input conditions

Generation is blocked until critical issues are resolved.

---

### Preview Mode
Compare:

**Before → After**

---

## Workflow

1. Select **Input Mesh**
2. Choose **Category**
3. Choose **Preset**
4. Set **Reduction Level**
5. Generate meshes
6. Review results
7. Export

---

## Design Philosophy

This is **not** intended to be one universal reduction tool.

Instead, it uses **specialized generation trees** tailored for different mesh types.

Presets:

- hard surface: (e.g vehicles, props, architecture)
- organic: (e.g rocks, vegetation, terrain)

**It is planned to add sub-categories under preset logic.**

Each preset uses different logic for:

- UV preservation
- edge handling
- topology reduction
- shading preservation

---

## Technology

Built with:

- **Blender Python API**
- **Geometry Nodes**
- **Modifiers**
- automated background processing

The user only interacts with a clean UI layer (technical complexity stays under the hood).

---

## Goals

- faster asset production
- consistent optimization quality
- reduced manual cleanup
- predictable results
- artist-friendly workflow

---

## Status

**In Development**

Core systems currently under active R&D.

---

## License

GPL-3.0-or-later
