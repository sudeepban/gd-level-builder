"""
Ember Falls — volcanic Hard level.
Ground-focused. Pink orbs only — keeps player close to the lava floor.
Thermal color journey: deep crimson → dark red → orange → amber → white-gold → ash grey.
Song: Cycles (song_id=8)
"""
import sys
sys.path.insert(0, ".")
from gd_lib import *

reset()

# ── TERRAIN ──────────────────────────────────────────────────────────────────
ground(0, 15)                  # section 1
ground(16, 19)                 # section 2 approach
raised(20, 23, h=1)            # lava pillar 1 — 4-wide, spike near far end
ground(24, 28)                 # after pillar, before gap
# 2-block gap: x=29, 30
ground(31, 55)                 # sections 3 & 4 base
raised(35, 38, h=1)            # lava pillar 2 — 4-wide, spike at far end
raised(46, 49, h=1)            # lava pillar 3 — 4-wide, spike at far end
ground(56, 95)                 # sections 5 & 6
ground(96, 106)                # outro

# ── SECTION 1: DEEP CRIMSON — Hard opening (x=0–15) ─────────────────────────
# Triple spike right at the start: Hard difficulty, no warmup
sp(2); sp(3); sp(4)            # triple spike
sp(9); sp(10)                  # double spike (4 clear: 5–8 ✓)
sp(14)                         # single spike  (3 clear: 11–13 ✓)

# ── SECTION 2: DARK RED — Lava pillar + pink orb gap (x=16–34) ──────────────
# 4-wide pillar — player has room to land, then spike near the far end
sp_on(22, G+1)                 # spike near far end of pillar 1 (player lands at 20,21 first ✓)
pink_orb(28)                   # orb — hops the 2-block gap ahead
# gap: x=29, 30  (2 blocks, validator limit 3 ✓)
sp(33)                         # single spike after landing (2 clear: 31,32 ✓)

# ── SECTION 3: ORANGE — Double-pillar run (x=35–55) ─────────────────────────
# Two 4-wide pillars, spike at far end of each; single spikes between them
sp_on(37, G+1)                 # spike near far end of pillar 2 (player lands at 35,36 ✓)
sp(42); sp(43)                 # double spike on ground (3 clear from pillar end: 39,40,41 ✓)
sp_on(48, G+1)                 # spike near far end of pillar 3 (player lands at 46,47 ✓)
sp(53)                         # single spike after pillar 3  (3 clear: 50,51,52 ✓)

# ── SECTION 4: AMBER — Steady double-spike run (x=56–72) ────────────────────
# Double spikes with consistent 3-block recovery — Hard but readable rhythm
sp(57); sp(58)                 # double spike (3 clear from sp(53): 54,55,56 ✓)
sp(62); sp(63)                 # double spike (3 clear: 59,60,61 ✓)
sp(67); sp(68)                 # double spike (3 clear: 64,65,66 ✓)
sp(72)                         # single spike  (3 clear: 69,70,71 ✓)

# ── SECTION 5: HOT AMBER — Sawblade gauntlet (x=73–85) ──────────────────────
saw(75)                        # sawblade (3 above ground, 2-block clearance)
sp(77)                         # spike  (4 clear from sp(72): 73,74,75,76 ✓)
saw(80)                        # sawblade
sp(82); sp(83)                 # double spike (4 clear from sp(77): 78,79,80,81 ✓)

# ── SECTION 6: WHITE-GOLD CLIMAX — Triple spike finale (x=86–96) ────────────
# One big climax moment — 4 clear blocks of runway, then the hardest hit
sp(88); sp(89); sp(90)         # TRIPLE SPIKE (4 clear from sp(83): 84,85,86,87 ✓)
sp(94); sp(95)                 # double spike aftermath (3 clear: 91,92,93 ✓)

# ── SECTION 7: ASH GREY — Cooling outro (x=97–106) ──────────────────────────
sp(99)                         # single spike (3 clear: 96,97,98 ✓)
sp(103)                        # final spike   (3 clear: 100,101,102 ✓)

# ── THERMAL COLOR JOURNEY ────────────────────────────────────────────────────
# Channels: 1004 = objects, 1001 = ground texture, 1000 = background

# DEEP CRIMSON — instant snap
color_trigger(-2, 1004, r=180, g_=20,  b=20,  duration=0.0, blending=True)
color_trigger(-2, 1001, r=100, g_=15,  b=15,  duration=0.0)
color_trigger(-2, 1000, r=20,  g_=2,   b=2,   duration=0.0)

# DARK RED — entering section 2
color_trigger(14, 1004, r=200, g_=35,  b=10,  duration=1.0, blending=True)
color_trigger(14, 1001, r=130, g_=22,  b=8,   duration=1.0)
color_trigger(14, 1000, r=22,  g_=4,   b=2,   duration=1.0)

# ORANGE — lava glow intensifies, section 3
color_trigger(30, 1004, r=215, g_=100, b=10,  duration=1.0, blending=True)
color_trigger(30, 1001, r=155, g_=65,  b=8,   duration=1.0)
color_trigger(30, 1000, r=24,  g_=10,  b=2,   duration=1.0)

# AMBER — molten core, section 4
color_trigger(53, 1004, r=225, g_=165, b=20,  duration=1.0, blending=True)
color_trigger(53, 1001, r=170, g_=120, b=15,  duration=1.0)
color_trigger(53, 1000, r=22,  g_=17,  b=4,   duration=1.0)

# HOT AMBER — near the source, sawblade section
color_trigger(70, 1004, r=245, g_=205, b=40,  duration=1.0, blending=True)
color_trigger(70, 1001, r=195, g_=158, b=28,  duration=1.0)
color_trigger(70, 1000, r=22,  g_=18,  b=6,   duration=1.0)

# WHITE-GOLD — peak heat, climax
color_trigger(85, 1004, r=255, g_=245, b=185, duration=1.0, blending=True)
color_trigger(85, 1001, r=225, g_=205, b=125, duration=1.0)
color_trigger(85, 1000, r=18,  g_=15,  b=6,   duration=1.0)

# ASH GREY — cooling, resolution
color_trigger(94, 1004, r=125, g_=115, b=105, duration=1.5, blending=True)
color_trigger(94, 1001, r=90,  g_=82,  b=78,  duration=1.5)
color_trigger(94, 1000, r=14,  g_=14,  b=16,  duration=1.5)

# ── GLOW LIGHTS ──────────────────────────────────────────────────────────────
glow_light(-1, r=180, g_=30,  b=10)    # deep crimson ember at start
glow_light(55, r=220, g_=140, b=20)    # amber glow mid-level
glow_light(86, r=255, g_=230, b=150)   # white-gold blaze at climax

# ── VALIDATE & EXPORT ────────────────────────────────────────────────────────
validate()
lvl = build("Ember Falls", song_id=8, description="Into the volcanic abyss.", version=1)
lvl.to_file("output/EmberFalls.gmd")
print("Exported output/EmberFalls.gmd")
