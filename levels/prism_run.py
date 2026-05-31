"""
Prism Run — Rainbow-spectrum Normal-difficulty level.
Every block has its own intrinsic color forming a continuous rainbow gradient
from red (start) to violet (end) — no color triggers needed.
Each section introduces a new mechanic before testing it.
Song: Jumper (official song 6)
"""
import sys
sys.path.insert(0, ".")
from gd_lib import *

reset()

# ──────────────────────────────────────────────────────────────────────────────
# SECTION 1: RED — Warmup (x=0–13)
# Three single spikes with comfortable 4–5 block spacing.
# ──────────────────────────────────────────────────────────────────────────────
ground(0, 13)
sp(3)
sp(8)
sp(12)

# ──────────────────────────────────────────────────────────────────────────────
# SECTION 2: ORANGE — First gap + raised step (x=14–28)
# Easy 2-block gap, then a 1-block raised platform with a spike to jump.
# ──────────────────────────────────────────────────────────────────────────────
ground(14, 16)
# 2-block gap: x=17, 18
ground(19, 21)
raised(22, 24, h=1)      # solid 1-block-high step (surface at G+1)
sp_on(23, G + 1)         # spike on top of raised step → placed at G+2
ground(25, 28)
sp(27)                   # single spike after landing from step

# ──────────────────────────────────────────────────────────────────────────────
# SECTION 3: YELLOW — Yellow pad big launch (x=29–43)
# Pad fires you 4.5 blocks into the air; coin floats at peak height as a treat.
# ──────────────────────────────────────────────────────────────────────────────
ground(29, 32)
yellow_pad(32)           # big launch — ~6 blocks forward, 4.5 blocks high
coin(34, G + 3)          # 3-block-high coin inside gap — only reachable at pad peak
# 3-block gap: x=33, 34, 35  (pad easily crosses; validator limit = 3 without orb ✓)
ground(36, 43)
sp(42)                   # spike 10 blocks after pad — well past post-pad clear zone ✓

# ──────────────────────────────────────────────────────────────────────────────
# SECTION 4: GREEN — Yellow orb gap (x=44–57)
# Jump + click yellow orb at its peak to rocket over a 4-block gap.
# Coin reward on the far side.
# ──────────────────────────────────────────────────────────────────────────────
ground(44, 46)
yellow_orb(46)           # click at jump peak → flies over 4-block gap
# 4-block gap: x=47, 48, 49, 50  (max safe with yellow orb ✓)
ground(51, 57)
coin(54, G + 2)          # floating coin (reachable at normal jump peak)
sp(56)                   # spike after reward zone

# ──────────────────────────────────────────────────────────────────────────────
# SECTION 5: CYAN — Sawblade gauntlet (x=58–70)
# Continuous ground; player runs under sawblades and jumps over ground spikes.
# ──────────────────────────────────────────────────────────────────────────────
ground(58, 70)
saw(61)                  # sawblade — 3 blocks above ground, safe to walk under
sp(63)                   # spike to jump (player has already cleared the saw)
saw(66)                  # second sawblade
sp(68)                   # spike to jump again

# ──────────────────────────────────────────────────────────────────────────────
# SECTION 6: INDIGO — Double spike challenge (x=71–84)
# Double-wide spikes (2 blocks wide) — harder but clearable. Introduces the
# mechanic cleanly before the violet climax reuses it.
# ──────────────────────────────────────────────────────────────────────────────
ground(71, 84)
sp(73); sp(74)           # double spike  (comfortable approach from x=71)
sp(79)                   # single spike  (4 clear blocks: 75–78 ✓)
sp(83)                   # single spike  (3 clear blocks: 80–82 ✓)

# ──────────────────────────────────────────────────────────────────────────────
# SECTION 7: VIOLET — Pink orb gap + double spike climax (x=85–95)
# Pink orb hops a 2-block gap, then a final double spike before the clear outro.
# ──────────────────────────────────────────────────────────────────────────────
ground(85, 87)
pink_orb(87)             # small boost over 2-block gap
# 2-block gap: x=88, 89
ground(90, 95)
sp(92); sp(93)           # double spike — player now knows the mechanic from section 6 ✓

# ──────────────────────────────────────────────────────────────────────────────
# OUTRO: WHITE — Triumphant resolution (x=96–106)
# Easy ground, two celebration coins.
# ──────────────────────────────────────────────────────────────────────────────
ground(96, 106)
coin(100, G + 2)         # coin — grab with a normal jump
coin(103, G + 2)         # second coin reward

# ──────────────────────────────────────────────────────────────────────────────
# RAINBOW BLOCK COLORS
# Each block gets its own intrinsic color — a smooth gradient from red to violet
# spanning the full level width. No triggers needed.
# ──────────────────────────────────────────────────────────────────────────────
color_blocks_rainbow(width=107, saturation=1.0, value=0.92, hue_range=285,
                     solid_box=True, border_hue_offset=180)

# ──────────────────────────────────────────────────────────────────────────────
# VALIDATE & EXPORT
# ──────────────────────────────────────────────────────────────────────────────
validate()
lvl = build("Prism Run", song_id=6, description="Race through the rainbow!", version=1)
lvl.to_file("output/PrismRun.gmd")
print("Exported output/PrismRun.gmd")
