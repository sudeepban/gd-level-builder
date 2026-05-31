"""
tools/render_level.py — render a .gmd file as a 2D side-view PNG.

Usage:
    python tools/render_level.py output/PrismRun.gmd
    python tools/render_level.py output/EmberFalls.gmd
"""
import sys
sys.path.insert(0, ".")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from pathlib import Path
from gmdkit import Level
from gmdkit.mappings import obj_prop
from gmdkit.mappings.obj_prop import trigger as trig_prop

BLOCK      = 30
GROUND_Y   = 105   # GD internal y baseline
X_OFFSET   = 195

def to_grid(x_gd, y_gd):
    return (x_gd - X_OFFSET) / BLOCK, (y_gd - GROUND_Y) / BLOCK

# ── object renderers ─────────────────────────────────────────────────────────

def draw_block(ax, gx, gy, color="#5a5a5a"):
    ax.add_patch(patches.Rectangle(
        (gx - 0.5, gy - 0.5), 1, 1,
        linewidth=0.3, edgecolor="#333", facecolor=color, zorder=2))

def draw_spike(ax, gx, gy, rot=0):
    # Default spike points up; rot=180 → upside-down
    if rot == 180:
        pts = [(gx - 0.42, gy + 0.45), (gx + 0.42, gy + 0.45), (gx, gy - 0.4)]
    else:
        pts = [(gx - 0.42, gy - 0.45), (gx + 0.42, gy - 0.45), (gx, gy + 0.4)]
    ax.add_patch(plt.Polygon(pts, facecolor="#ff3333", edgecolor="#cc1111",
                              linewidth=0.5, zorder=4))

def draw_sawblade(ax, gx, gy):
    # Star with 8 teeth
    n_teeth = 8
    angles = np.linspace(0, 2 * np.pi, n_teeth * 2, endpoint=False)
    radii  = [0.42 if i % 2 == 0 else 0.24 for i in range(n_teeth * 2)]
    xs = [r * np.cos(a) + gx for r, a in zip(radii, angles)]
    ys = [r * np.sin(a) + gy for r, a in zip(radii, angles)]
    ax.add_patch(plt.Polygon(list(zip(xs, ys)),
                              facecolor="#ff8800", edgecolor="#cc5500",
                              linewidth=0.5, zorder=4))
    ax.add_patch(plt.Circle((gx, gy), 0.10, color="#1a0800", zorder=5))

def draw_orb(ax, gx, gy, color):
    ax.add_patch(plt.Circle((gx, gy), 0.38, color=color, alpha=0.9, zorder=4))
    ax.add_patch(plt.Circle((gx - 0.1, gy + 0.1), 0.1,
                              color="white", alpha=0.5, zorder=5))

def draw_pad(ax, gx, gy, color):
    ax.add_patch(patches.FancyBboxPatch(
        (gx - 0.42, gy - 0.18), 0.84, 0.3,
        boxstyle="round,pad=0.05",
        facecolor=color, edgecolor="white", linewidth=0.5, zorder=4))

def draw_coin(ax, gx, gy):
    ax.add_patch(plt.Circle((gx, gy), 0.28, color="#ffcc00",
                              edgecolor="#aa8800", linewidth=0.5, zorder=4))
    ax.text(gx, gy, "★", ha="center", va="center",
            fontsize=5, color="#7a5500", zorder=5)

# ── color zone background shading ────────────────────────────────────────────

def get_zone_color(triggers, gx):
    """Return the object (1004) color active at grid x position."""
    obj_triggers = sorted(
        [(tx, (r/255, g/255, b/255)) for tx, ch, r, g, b in triggers if ch == 1004],
        key=lambda t: t[0]
    )
    if not obj_triggers:
        return (0.35, 0.35, 0.35)
    color = obj_triggers[0][1]
    for tx, col in obj_triggers:
        if tx <= gx:
            color = col
    return color


def draw_color_zones(ax, triggers, x_min, x_max):
    """Shade vertical bands using a brightened version of the bg color."""
    bg_triggers = sorted(
        [(gx, (r/255, g/255, b/255)) for gx, ch, r, g, b in triggers if ch == 1000],
        key=lambda t: t[0]
    )
    if not bg_triggers:
        return
    all_zones = bg_triggers + [(x_max + 5, bg_triggers[-1][1])]
    for i in range(len(all_zones) - 1):
        x0, col = all_zones[i]
        x1, _   = all_zones[i + 1]
        # brighten the dark bg color significantly so it shows in the render
        bright = tuple(min(1.0, c * 6 + 0.06) for c in col)
        ax.axvspan(x0, x1, ymin=0, ymax=1,
                   facecolor=bright, alpha=0.12, zorder=0)

# ── main render ──────────────────────────────────────────────────────────────

def render(gmd_path: str, output_path: str):
    lvl = Level.from_file(gmd_path)
    lvl.load()

    title = Path(gmd_path).stem

    # Collect color triggers for zone shading
    color_triggers = []
    for obj in lvl.objects:
        if obj[obj_prop.ID] == 899:
            gx, _ = to_grid(obj[obj_prop.X], obj[obj_prop.Y])
            ch = obj.get(23, 0)        # CHANNEL = 23
            r  = int(obj.get(7,  0))   # RED
            g  = int(obj.get(8,  0))   # GREEN
            b  = int(obj.get(9,  0))   # BLUE
            color_triggers.append((gx, ch, r, g, b))

    # Build per-block channel color map from kS38 in the start object
    channel_colors = {}
    try:
        for color in lvl.start.get('kS38', []):
            channel_colors[color.channel] = (
                color.red / 255.0,
                color.green / 255.0,
                color.blue / 255.0,
            )
    except Exception:
        pass

    # Figure out x extent
    xs = [to_grid(o[obj_prop.X], o[obj_prop.Y])[0]
          for o in lvl.objects if o[obj_prop.ID] != 899]
    x_min = min(xs) - 1 if xs else -2
    x_max = max(xs) + 2 if xs else 30

    fig, ax = plt.subplots(figsize=(max(16, (x_max - x_min) * 0.18), 5))
    dark_bg = "#0d0d0d"
    ax.set_facecolor(dark_bg)
    fig.patch.set_facecolor(dark_bg)

    draw_color_zones(ax, color_triggers, x_min, x_max)

    # Draw objects
    for obj in lvl.objects:
        oid = obj[obj_prop.ID]
        gx, gy = to_grid(obj[obj_prop.X], obj[obj_prop.Y])
        rot = obj.get(obj_prop.ROTATION, 0) or 0

        # Determine block color: per-block channel assignment takes priority,
        # then fall back to zone-trigger interpolation, then default gray.
        # ID=207 (solid box): fill is COLOR_2; others: fill is COLOR_1.
        if oid == 207:
            per_block_ch = obj.get(obj_prop.COLOR_2)
        else:
            per_block_ch = obj.get(obj_prop.COLOR_1)
        if per_block_ch and per_block_ch in channel_colors:
            rgb = channel_colors[per_block_ch]
            block_color = "#{:02x}{:02x}{:02x}".format(
                int(rgb[0] * 235), int(rgb[1] * 235), int(rgb[2] * 235))
        else:
            zone_rgb = get_zone_color(color_triggers, gx)
            block_color = "#{:02x}{:02x}{:02x}".format(
                int(zone_rgb[0] * 180 + 20),
                int(zone_rgb[1] * 180 + 20),
                int(zone_rgb[2] * 180 + 20),
            )

        if oid in (1, 207): draw_block(ax, gx, gy, color=block_color)
        elif oid == 3:      draw_block(ax, gx, gy, color="#4a4a4a")
        elif oid == 8:  draw_spike(ax, gx, gy, rot=rot)
        elif oid == 21: draw_sawblade(ax, gx, gy)
        elif oid == 36: draw_orb(ax, gx, gy, "#ffe000")
        elif oid == 141:draw_orb(ax, gx, gy, "#ff66cc")
        elif oid == 35: draw_pad(ax, gx, gy, "#ffe000")
        elif oid == 140:draw_pad(ax, gx, gy, "#ff66cc")
        elif oid == 142:draw_coin(ax, gx, gy)
        # triggers and glow lights are invisible — skip

    # Axes styling
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(-4.8, 5.5)
    ax.set_aspect("equal")
    ax.set_title(title, color="white", fontsize=13, pad=8)
    ax.set_xlabel("grid x →", color="#888", fontsize=8)
    ax.tick_params(colors="#666", labelsize=7)
    for spine in ax.spines.values():
        spine.set_color("#333")

    # Ground reference line
    ax.axhline(-2.5, color="#555", lw=0.6, ls="--", alpha=0.5, zorder=1)

    # Legend
    legend_items = [
        patches.Patch(color="#5a5a5a", label="block"),
        patches.Patch(color="#ff3333", label="spike"),
        patches.Patch(color="#ff8800", label="sawblade"),
        patches.Patch(color="#ffe000", label="yellow orb/pad"),
        patches.Patch(color="#ff66cc", label="pink orb/pad"),
        patches.Patch(color="#ffcc00", label="coin"),
    ]
    ax.legend(handles=legend_items, loc="upper right",
              facecolor="#1a1a1a", edgecolor="#444",
              labelcolor="white", fontsize=7, framealpha=0.8)

    plt.tight_layout()
    plt.savefig(output_path, dpi=160, bbox_inches="tight",
                facecolor=dark_bg)
    plt.close()
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tools/render_level.py <path/to/level.gmd>")
        sys.exit(1)
    gmd = sys.argv[1]
    out = gmd.replace(".gmd", ".png")
    render(gmd, out)
