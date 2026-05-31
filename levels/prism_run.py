"""
Prism Run — Rainbow-spectrum Normal-difficulty level.
The world shifts through every color of the rainbow as you run.
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
# RAINBOW COLOR JOURNEY
# Triggers fire 2–4 blocks before each section so the shift is visually
# "arriving" as the player enters new territory.
# Channel 1004 = objects/blocks, Channel 1001 = ground, Channel 1000 = background
# ──────────────────────────────────────────────────────────────────────────────

# RED — instant at level start (fires before player position = 0)
color_trigger(-2, 1004, r=230, g_=40,  b=40,  duration=0.0, blending=True)
color_trigger(-2, 1001, r=180, g_=20,  b=20,  duration=0.0)
color_trigger(-2, 1000, r=25,  g_=3,   b=3,   duration=0.0)

# ORANGE — fade in before section 2
color_trigger(12, 1004, r=230, g_=120, b=10,  duration=1.0, blending=True)
color_trigger(12, 1001, r=180, g_=80,  b=5,   duration=1.0)
color_trigger(12, 1000, r=28,  g_=12,  b=2,   duration=1.0)

# YELLOW — bright and warm, before section 3
color_trigger(27, 1004, r=240, g_=220, b=20,  duration=1.0, blending=True)
color_trigger(27, 1001, r=190, g_=170, b=10,  duration=1.0)
color_trigger(27, 1000, r=22,  g_=20,  b=4,   duration=1.0)

# GREEN — before section 4
color_trigger(42, 1004, r=40,  g_=210, b=70,  duration=1.0, blending=True)
color_trigger(42, 1001, r=20,  g_=160, b=40,  duration=1.0)
color_trigger(42, 1000, r=4,   g_=20,  b=9,   duration=1.0)

# CYAN — before section 5
color_trigger(56, 1004, r=20,  g_=210, b=220, duration=1.0, blending=True)
color_trigger(56, 1001, r=10,  g_=160, b=170, duration=1.0)
color_trigger(56, 1000, r=4,   g_=22,  b=24,  duration=1.0)

# INDIGO — deeper blue, intensity building before section 6
color_trigger(69, 1004, r=60,  g_=80,  b=240, duration=1.0, blending=True)
color_trigger(69, 1001, r=30,  g_=40,  b=190, duration=1.0)
color_trigger(69, 1000, r=4,   g_=6,   b=28,  duration=1.0)

# VIOLET — rich purple before climax section 7
color_trigger(83, 1004, r=180, g_=30,  b=235, duration=1.0, blending=True)
color_trigger(83, 1001, r=130, g_=15,  b=180, duration=1.0)
color_trigger(83, 1000, r=18,  g_=3,   b=28,  duration=1.0)

# WHITE FINALE — bright and triumphant before outro
color_trigger(94, 1004, r=245, g_=245, b=255, duration=1.5, blending=True)
color_trigger(94, 1001, r=200, g_=200, b=230, duration=1.5)
color_trigger(94, 1000, r=12,  g_=8,   b=22,  duration=1.5)

# ──────────────────────────────────────────────────────────────────────────────
# GLOW LIGHTS — atmospheric (placed at y=255, well above level, invisible)
# ──────────────────────────────────────────────────────────────────────────────
glow_light(-1, r=200, g_=50,  b=50)    # warm red glow at the start
glow_light(44, r=50,  g_=200, b=80)    # cool green glow mid-level
glow_light(96, r=180, g_=100, b=235)   # violet-white glow at the finale

# ──────────────────────────────────────────────────────────────────────────────
# VALIDATE & EXPORT
# ──────────────────────────────────────────────────────────────────────────────
validate()
lvl = build("Prism Run", song_id=6, description="Race through the rainbow!", version=1)
lvl.to_file("output/PrismRun.gmd")
print("Exported output/PrismRun.gmd")
