"""
gd_lib.py — shared helpers for programmatic GD level building.

Usage in a level script:
    from gd_lib import *
    ground(0, 30)
    sp(5)
    lvl = build("My Level", song_id=1, description="...", version=1)
    lvl.to_file("output/MyLevel.gmd")
"""

from gmdkit import Level, Object
from gmdkit.mappings import obj_prop, lvl_prop
from gmdkit.mappings.obj_prop import trigger as trig_prop

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

BLOCK = 30
GROUND_Y_GD = 105
G = -3          # ground grid y
X_OFFSET = 195  # GD internal x origin offset

# Object IDs
ID_BLOCK       = 1
ID_THIN_PLAT   = 3
ID_SPIKE       = 8
ID_SAWBLADE    = 21
ID_YELLOW_PAD  = 35
ID_YELLOW_ORB  = 36
ID_PINK_PAD    = 140
ID_PINK_ORB    = 141
ID_COIN        = 142
ID_COLOR_TRIG  = 899
ID_GLOW_LIGHT  = 1006

# ---------------------------------------------------------------------------
# Internal state
# ---------------------------------------------------------------------------

_objects: list = []


def reset():
    """Clear the object list — call at the top of each level script."""
    _objects.clear()


# ---------------------------------------------------------------------------
# Core placement
# ---------------------------------------------------------------------------

def add(id, gx, gy, rot=None):
    x = gx * BLOCK + X_OFFSET
    y = gy * BLOCK + GROUND_Y_GD
    o = Object({obj_prop.ID: id, obj_prop.X: float(x), obj_prop.Y: float(y)})
    if rot is not None:
        o[obj_prop.ROTATION] = float(rot)
    _objects.append(o)


# ---------------------------------------------------------------------------
# Terrain
# ---------------------------------------------------------------------------

def ground(sx, ex):
    """Single-layer ground from grid x=sx to x=ex (inclusive)."""
    for x in range(sx, ex + 1):
        add(ID_BLOCK, x, G)


def raised(sx, ex, h=1):
    """Solid raised platform h blocks above ground, filled down to ground."""
    for x in range(sx, ex + 1):
        for y in range(G, G + h + 1):
            add(ID_BLOCK, x, y)


def platform(sx, ex, gy):
    """Thin platform at an arbitrary grid y (no fill below)."""
    for x in range(sx, ex + 1):
        add(ID_BLOCK, x, gy)


# ---------------------------------------------------------------------------
# Hazards
# ---------------------------------------------------------------------------

def sp(x, rot=None):
    """Spike on ground."""
    add(ID_SPIKE, x, G + 1, rot)


def sp_on(x, surface_y, rot=None):
    """Spike on a raised surface at grid y=surface_y."""
    add(ID_SPIKE, x, surface_y + 1, rot)


def saw(x, gy=None):
    """Sawblade. Default: 3 above ground (2-block walking clearance)."""
    if gy is None:
        gy = G + 3
    add(ID_SAWBLADE, x, gy)


# ---------------------------------------------------------------------------
# Orbs & pads
# ---------------------------------------------------------------------------

def yellow_orb(x, gy=None):
    """Yellow orb. Default: 1 block above ground surface (reachable from ground)."""
    if gy is None:
        gy = G + 2
    add(ID_YELLOW_ORB, x, gy)


def pink_orb(x, gy=None):
    """Pink orb. Default: 1 block above ground surface."""
    if gy is None:
        gy = G + 2
    add(ID_PINK_ORB, x, gy)


def yellow_pad(x, surface_y=None):
    """Yellow pad. Default: on ground surface."""
    if surface_y is None:
        surface_y = G
    add(ID_YELLOW_PAD, x, surface_y + 1)


def pink_pad(x, surface_y=None):
    """Pink pad. Default: on ground surface."""
    if surface_y is None:
        surface_y = G
    add(ID_PINK_PAD, x, surface_y + 1)


# Short aliases matching existing level scripts
def orb(x, gy=None):
    yellow_orb(x, gy)

def pad(x, surface_y=None):
    yellow_pad(x, surface_y)


# ---------------------------------------------------------------------------
# Collectibles & decoration
# ---------------------------------------------------------------------------

def coin(x, gy):
    add(ID_COIN, x, gy)


def glow_light(x, r=244, g_=206, b=0, gy=255):
    """Atmospheric glow light placed well above the level (invisible to player)."""
    o_x = float(x * BLOCK + X_OFFSET)
    o_y = float(gy * BLOCK + GROUND_Y_GD)
    o = Object({
        obj_prop.ID: ID_GLOW_LIGHT,
        obj_prop.X: o_x,
        obj_prop.Y: o_y,
        7: float(r),
        8: float(g_),
        9: float(b),
        36: 1,   # blending on
    })
    _objects.append(o)


# ---------------------------------------------------------------------------
# Color triggers
# ---------------------------------------------------------------------------

def color_trigger(gx, channel, r, g_, b, duration=0.0, blending=False):
    """
    Place a color trigger at grid x=gx targeting color channel.

    channel: 1, 2, 3, 4, or 1000 (background)
    duration: seconds for transition (0 = instant snap)
    blending: True for glow/blending channels
    """
    x = float(gx * BLOCK + X_OFFSET)
    y = float(G * BLOCK + GROUND_Y_GD)  # placed at ground level (off-screen is fine)
    o = Object({
        obj_prop.ID: ID_COLOR_TRIG,
        obj_prop.X: x,
        obj_prop.Y: y,
        trig_prop.color.CHANNEL:  channel,
        trig_prop.color.RED:      float(r),
        trig_prop.color.GREEN:    float(g_),
        trig_prop.color.BLUE:     float(b),
        trig_prop.color.DURATION: float(duration),
        trig_prop.color.BLENDING: 1 if blending else 0,
    })
    _objects.append(o)


# ---------------------------------------------------------------------------
# Build & export
# ---------------------------------------------------------------------------

def build(name, song_id=1, description="", version=1) -> Level:
    """
    Assemble and return a Level from the current object list.
    Call lvl.to_file("output/Name.gmd") on the result.
    """
    lvl = Level.default(name)
    lvl[lvl_prop.NAME] = name
    lvl[lvl_prop.DESCRIPTION] = description
    lvl[lvl_prop.OFFICIAL_SONG_ID] = song_id
    lvl[lvl_prop.VERSION] = version
    lvl.load()
    lvl.objects.clear()
    for o in _objects:
        lvl.objects.append(o)
    return lvl


# ---------------------------------------------------------------------------
# Validator
# ---------------------------------------------------------------------------

def validate():
    """
    Scan the current object list for common design rule violations.
    Prints warnings but does not block export.
    Returns True if no issues found.
    """
    issues = []
    spikes = [(o[obj_prop.X], o[obj_prop.Y]) for o in _objects if o[obj_prop.ID] == ID_SPIKE]
    orbs_yellow = [(o[obj_prop.X], o[obj_prop.Y]) for o in _objects if o[obj_prop.ID] == ID_YELLOW_ORB]

    spike_xs = sorted(set(x for x, y in spikes))

    # Double-stacked spikes: two spikes at same x, consecutive y values
    spike_positions = set(spikes)
    for x, y in spikes:
        if (x, y + BLOCK) in spike_positions:
            gx = round((x - X_OFFSET) / BLOCK)
            issues.append(f"  [SPIKE] Double-stacked spike at grid x={gx} — not clearable")

    # Yellow orb ceiling clearance: warn if no ground info available
    for ox, oy in orbs_yellow:
        orb_gy = round((oy - GROUND_Y_GD) / BLOCK)
        peak_gy = orb_gy + 3.5  # yellow orb adds ~3.5 blocks of height
        if peak_gy > 3:          # rough check: needs 6 blocks from ground
            pass  # would need ceiling info to validate precisely

    # Gap detection: find gaps in ground blocks and check width
    ground_blocks = sorted(set(
        round((o[obj_prop.X] - X_OFFSET) / BLOCK)
        for o in _objects
        if o[obj_prop.ID] == ID_BLOCK
        and round((o[obj_prop.Y] - GROUND_Y_GD) / BLOCK) == G
    ))

    if ground_blocks:
        for i in range(len(ground_blocks) - 1):
            gap = ground_blocks[i + 1] - ground_blocks[i] - 1
            if gap > 3:
                # Check if a yellow orb precedes the gap
                gap_start_x = ground_blocks[i] + 1
                nearby_orb = any(
                    abs(round((ox - X_OFFSET) / BLOCK) - ground_blocks[i]) <= 3
                    for ox, _ in orbs_yellow
                )
                max_gap = 4 if nearby_orb else 3
                if gap > max_gap:
                    issues.append(
                        f"  [GAP] {gap}-block gap starting at grid x={gap_start_x} "
                        f"(max {'4 with yellow orb' if nearby_orb else '3 without orb'})"
                    )

    if issues:
        print(f"Validator found {len(issues)} issue(s):")
        for msg in issues:
            print(msg)
        return False
    else:
        print("Validator: no issues found.")
        return True
