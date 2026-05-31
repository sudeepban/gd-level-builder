# Geometry Dash .gmd File Creation Process
*Technical reference — how to go from level design to importable .gmd file*

---

## Dependencies

```bash
pip install gmdkit --break-system-packages
```

That's the only dependency. `gmdkit` handles all encoding internally.

---

## Imports

```python
from gmdkit import Level, Object
from gmdkit.mappings import obj_prop, lvl_prop
```

---

## Coordinate System

| Property | Value |
|---|---|
| 1 block | 30 units |
| Ground (natural GD floor) | grid y = -3 ✓ confirmed |
| X origin offset | +195 units added to all objects |
| Y origin | GROUND_Y_GD = 105 (GD internal baseline) |

**Converting grid coords to GD units:**
```python
GROUND_Y_GD = 105
BLOCK = 30

x_gd = gx * BLOCK + 195
y_gd = gy * BLOCK + GROUND_Y_GD
```

---

## Creating Objects

```python
o = Object({
    obj_prop.ID: 1,          # object type (e.g. 1 = block, 8 = spike)
    obj_prop.X: float(x_gd),
    obj_prop.Y: float(y_gd),
})

# Optional rotation (e.g. 180 = upside down spike)
o[obj_prop.ROTATION] = 180.0
```

**All X and Y values must be floats, not ints.**

---

## Key Object IDs

| Object | ID |
|---|---|
| Block | 1 |
| Thin Platform | 3 |
| Spike | 8 |
| Sawblade | 21 |
| Yellow Pad | 35 |
| Yellow Orb | 36 |
| Half Spike (avoid — off-grid anchor) | 39 |
| Blue Orb | 84 |
| Pink Pad | 140 |
| Pink Orb | 141 |
| Coin | 142 |
| Color Trigger | 899 |
| Pulse/Glow Light (decoration) | 1006 |

**ID 1006 — Confirmed Decoration (Pulse/Glow Light)**
Seen in Ex_1_Cave_of_Glow. Placed at y=255 (well above the level), uses color channels and blending. Safe to use as atmospheric lighting. Properties observed:
- `51`: group ID (e.g. 2)
- `47`: fade duration (e.g. 0.3)
- `210`: unknown flag (1)
- `7`, `8`, `9`: RGB color (e.g. 244, 206, 0 = warm amber glow)
- `36`: blending flag (1 = on)

**ID 39 — Half Spike**
Confirmed: a smaller half-sized spike. Placed at a slightly off-grid y position (y≈-3.3 rather than a clean grid value), which suggests its anchor point doesn't align neatly with the grid. Avoid using — placement is unpredictable and a full spike (ID 8) is cleaner and more reliable.

---

## Placement Rules (Quick Reference)

| Object | Placement |
|---|---|
| Ground block | grid y = -3 |
| Spike on ground | grid y = -2 |
| Spike on raised surface at y=N | grid y = N+1 |
| Pad on ground | grid y = -2 (one above surface) |
| Pad on raised surface at y=N | grid y = N+1 (one above surface) |
| Orb (reachable from ground) | grid y = -1 (1 block above ground surface) |
| Sawblade (safe to walk under) | grid y = 0 (3 above ground = 2 block clearance) |

---

## Recommended Helper Functions

```python
GROUND_Y_GD = 105
BLOCK = 30
G = -3  # effective ground grid y

objects = []

def add(id, gx, gy, rot=None):
    x = gx * BLOCK + 195
    y = gy * BLOCK + GROUND_Y_GD
    o = Object({obj_prop.ID: id, obj_prop.X: float(x), obj_prop.Y: float(y)})
    if rot is not None:
        o[obj_prop.ROTATION] = float(rot)
    objects.append(o)

def ground(sx, ex):
    # Single layer ground — no chunk fill needed, GD renders floor below automatically
    for x in range(sx, ex+1):
        add(1, x, G)

def raised(sx, ex, h=1):
    # Solid raised platform h blocks above ground, filled down to G
    for x in range(sx, ex+1):
        for y in range(G, G+h+1):
            add(1, x, y)

def sp(x, rot=None):
    add(8, x, G+1, rot)  # spike on ground

def sp_on(x, surface_y, rot=None):
    add(8, x, surface_y+1, rot)  # spike on raised surface

def orb(x):
    add(36, x, G+2)  # yellow orb, 1 block above ground surface

def pad(x):
    add(35, x, G+1)  # yellow pad, 1 above ground surface (appears grounded)

def saw(x):
    add(21, x, G+3)  # sawblade, 3 above ground = 2 block walking clearance

def coin(x, y):
    add(142, x, y)
```

---

## Building the Level

```python
lvl = Level.default("My Level Name")
lvl[lvl_prop.NAME] = "My Level Name"
lvl[lvl_prop.DESCRIPTION] = "Level description here"
lvl[lvl_prop.OFFICIAL_SONG_ID] = 1  # 1 = Stereo Madness, safe default
lvl[lvl_prop.VERSION] = 1

lvl.load()
lvl.objects.clear()
for o in objects:
    lvl.objects.append(o)

lvl.to_file("MyLevel.gmd")
```

`to_file()` handles GZip compression and Base64 encoding automatically. Output is a valid plist XML `.gmd` file.

---

## Importing via GDShare

1. Install **Geode** mod loader for Geometry Dash
2. Install **GDShare** mod via Geode
3. Place the `.gmd` file in the GDShare import folder (or use the in-game import button)
4. Open GD → My Levels → Import
5. Level appears ready to play or edit

**Note:** `.gmd` is the original GDShare text-based plist format. `.gmd2` is the newer binary ZIP format. Both are supported by current GDShare — always output `.gmd` for maximum compatibility.

---

## Common Mistakes & Fixes

| Mistake | Fix |
|---|---|
| Objects floating above ground | Ground is at grid y=-3, not y=0 |
| Chunk fill creates floating island | Use single-layer ground blocks only — GD renders floor texture below automatically |
| Pad appears to hover | Pad goes at surface_y + 1, not surface_y |
| Spike on raised platform at wrong height | Spike goes at surface_y + 1, matching platform level |
| X/Y values passed as int instead of float | Always cast: `float(x)`, `float(y)` |
| Level appears empty after import | Call `lvl.load()` before clearing/appending objects |

---

## Full Minimal Working Example

```python
from gmdkit import Level, Object
from gmdkit.mappings import obj_prop, lvl_prop

GROUND_Y_GD = 105
BLOCK = 30
G = -3

objects = []

def add(id, gx, gy, rot=None):
    x = gx * BLOCK + 195
    y = gy * BLOCK + GROUND_Y_GD
    o = Object({obj_prop.ID: id, obj_prop.X: float(x), obj_prop.Y: float(y)})
    if rot is not None:
        o[obj_prop.ROTATION] = float(rot)
    objects.append(o)

# Simple level: ground with one spike
for x in range(0, 20):
    add(1, x, G)          # ground blocks
add(8, 5, G+1)            # spike on ground
add(35, 10, G+1)          # yellow pad on ground

lvl = Level.default("Test Level")
lvl[lvl_prop.NAME] = "Test Level"
lvl[lvl_prop.DESCRIPTION] = "Minimal test"
lvl[lvl_prop.OFFICIAL_SONG_ID] = 1
lvl[lvl_prop.VERSION] = 1

lvl.load()
lvl.objects.clear()
for o in objects:
    lvl.objects.append(o)

lvl.to_file("TestLevel.gmd")
print(f"Done — {len(objects)} objects")
```
