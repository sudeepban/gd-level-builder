# Geometry Dash Level Design Notes
*Living document — updated as we learn more through playtesting*
*For technical .gmd creation process, see GD_GMD_PROCESS.md*

---

## Physics Model (Normal Speed, 60fps)

| Property | Value |
|---|---|
| Gravity | -0.876 units/frame² |
| FPS | 60 |
| Horizontal speed | ~5.18 units/frame (~10.4 blocks/sec) |
| Initial jump velocity | ~8.88 units/frame |
| Jump duration | ~20 frames (338ms) |
| **Max jump height** | **1.5 blocks** |
| **Max jump distance** | **3.5 blocks (pixel-perfect) / 3.0 blocks (safe)** |

---

## Boost Reference Table

| Boost Type | Height | Max Gap Crossable | Air Time |
|---|---|---|---|
| Normal jump | 1.5 blocks | 3.5 blocks (use 3.0 safe) | 338ms |
| Pink orb | 1.3 blocks | 3.3 blocks (use 3.0 safe) | 315ms |
| Pink pad | 1.8 blocks | 3.8 blocks (use 3.5 safe) | 370ms |
| Yellow orb | 3.5 blocks | 5.3 blocks (use 5.0 safe) | 516ms |
| Yellow pad | 4.5 blocks | 6.1 blocks (use 5.5 safe) | 585ms |
| Red orb | 6.0 blocks | 7.0 blocks (use 6.5 safe) | 676ms |
| Red pad | 8.0 blocks | 8.1 blocks (use 7.5 safe) | 780ms |

**Key insight:** Pink orb is weaker than a normal jump — NOT for crossing big gaps, use for small precise corrections. Yellow orb is the real gap-crosser (5+ blocks).

---

## Orb Placement Rules

- Player can only reach an orb within **1.5 blocks above their current surface**
- After yellow orb at y=1.0 above ground → player peaks at **4.5 blocks** above ground
- After yellow orb at y=1.5 above ground → player peaks at **5.0 blocks** above ground
- **Ceiling clearance after yellow orb: at least 5.5–6.0 blocks from ground**
- Yellow orb requires tall open space above — don't put it in enclosed corridors

---

## Hard Design Rules

Physical limits — violating these makes the level impossible.

- **Max gap (no orb): 3 blocks** (3.5 pixel-perfect, avoid)
- **Max gap (yellow orb): 4 blocks** (playtested safe limit — 5 felt too large in practice)
- **Minimum gap: 4 blocks** — anything under 4 is only acceptable as a deliberate timing challenge (land between spikes), not a standard jump gap
- **Max spike stack: 1 block high** — double-stacked spikes cannot be jumped
- **Ceiling clearance (normal jump): minimum 3 blocks** from floor
- **Ceiling clearance (after yellow orb): minimum 6 blocks** from floor
- **Staircase steps: max 1 block per step**
- **Raised platforms: max 1 block high** without orb/pad assist
- **Orb must be within 1.5 blocks above jump surface** to be reachable

---

## Orb & Pad Behavior

- **Pink orb**: 1.3 block boost — weaker than a normal jump. Small corrections only.
- **Yellow orb**: 3.5 block boost — main gap-crossing tool. Needs open vertical space.
- **Pink pad**: 1.8 block boost — slightly better than a normal jump.
- **Yellow pad**: 4.5 block boost — big launch, dramatic section transitions.
- **Red orb**: 6.0 block boost — extreme, huge open space required.
- **Blue orb**: flips gravity — do not use yet (complex).

---

## Sawblade Notes

- Place at **3 blocks above floor** minimum — gives 2 full blocks of walking clearance
- At 2 blocks above floor: only 1 block clearance — player clips, never use
- Route player *under* sawblades, not over them

---

## Gap Design Guide

| Gap Width | Boost Required | Difficulty |
|---|---|---|
| 1–2 blocks | None | Easy |
| 3 blocks | None | Standard |
| 3.5 blocks | None | Pixel-perfect, avoid |
| 4 blocks | Pink pad minimum | Needs assist |
| 5 blocks | Yellow orb | Standard orb gap |
| 6+ blocks | Yellow pad / Red orb | Dramatic only |

---

## Spike Rules

**Clearance:**
- Single spike (1 block): clearable with normal jump
- Double stacked spike: never use — not clearable
- Ceiling spikes: minimum 3 blocks from floor (normal), 6 blocks (after yellow orb)

**Spacing between spikes:**

| Clear blocks between spikes | Difficulty |
|---|---|
| 1 block | Near impossible — never use |
| 2 blocks | Very hard |
| 3 blocks | Medium |
| 4–5 blocks | Easy / comfortable |

**Default:** 4 clear blocks for normal sections, 3 for hard sections.

---

## Level Structure Principles

- **Alternate tension and relief** — hazard cluster → breathing room → hazard cluster
- **Introduce before testing** — show a safe version of a mechanic before requiring precision
- **Sections should build** — don't introduce a new mechanic cold in the finale
- **One gap at a time** — player can't descend fast enough after one gap to immediately jump another. Always put solid recovery ground between gaps.
- **Post-pad recovery space** — after a yellow pad, leave 7+ clear blocks before any hazard
- **Raised platform gaps** — spikes must be at platform surface height on BOTH sides of every gap, no exceptions. Without spikes, the player can walk off and bypass the gap entirely.
- **Triple spikes (3 wide)** — right at the safe jump limit, use sparingly and only after warmup
- **Vary hazard patterns** — never repeat spike→gap→spike→gap in a simple loop. Mix hazard types, gap sizes, and mechanics. Repetition is both boring and unexpectedly deadly (player gets lulled into a rhythm).
- **Chain mechanics together** — pad → orb, sawblade → gap, double spike → breathing room. Each section should tell a story, not repeat a formula.
- **Double spikes** — two spikes side by side (2 wide). Harder than single, still clearable. Use for mid-difficulty sections after warmup.
- **Vary gap sizes deliberately** — never the same size twice in a row. E.g. 6-block gap → single spike → 5-block gap → pad → orb is interesting. Same gap over and over is not.
- **Beat sync — place spikes AFTER the beat mark, not ON it** — the player jumps when they hear the note, meaning the spike should land a little after the beat so the jump clears it naturally. Placing a spike exactly on the beat means the player gets hit before they can react. Think of it as: note plays → player jumps → spike appears a beat later → player clears it.

---

## Color Triggers Mid-Level

Color triggers placed during the level (not just at the start) are a powerful tool for atmosphere and storytelling. Confirmed working in Crystal Caverns v5.

### How to use mid-level color triggers
Place a color trigger at the x position where you want the shift to begin. Use `duration > 0` for smooth transitions rather than snapping.

```python
# Smooth 1-second shift to danger red at x=109
# Channel 1004 = objects/blocks, 1001 = ground texture, 1000 = background
# Do NOT use channels 1–999: blocks don't use those by default.
color_trigger(109, 1004, r=180, g_=0,  b=80,  duration=1.0, blending=True)
color_trigger(109, 1001, r=140, g_=0,  b=60,  duration=1.0)
color_trigger(109, 1000, r=25,  g_=3,  b=10,  duration=0.8)
```

### Recommended color journey pattern
Match color shifts to section transitions — the visual change signals the gameplay change to the player:

**Correct channel IDs (confirmed):**
| Channel | What it controls |
|---|---|
| 1004 | All objects/blocks (default for ID 1, 8, 21, etc.) |
| 1001 | Ground texture color |
| 1000 | Background color |
| 1–999 | User-defined — NOT assigned to objects by default, do not use |

| Section | Mood | Color suggestion |
|---|---|---|
| Intro | Calm, safe | Cool teal, ice white |
| First drop | Intensifying | Deeper blue, darker BG |
| Calm mid | Eerie, mysterious | Soft purple, lavender |
| Second drop | Danger | Hot pink/red, red spikes |
| Climax | Peak danger | Deep red, orange spikes |
| Outro | Resolution | Return to intro colors |

### Tips
- **Transition duration 0.8–1.5s** for section shifts — smooth but noticeable
- **Transition duration 0.0** for instant snaps — use at dramatic moments only
- **Outro resolution** — fading back to the intro color palette over 2s feels satisfying
- **BG color shifts too** — shifting channel 1000 alongside object channels makes the whole screen feel different, not just the blocks
- **Blending=True** channels glow and look better with color shifts than flat colors

---

## Known Issues / Still To Learn

- [ ] Confirm player hitbox size (assumed 1x1 block)
- [ ] How speed portals change horizontal speed (all gap/distance values change)
- [ ] Background and ground texture IDs (kA6, kA7 in start object — values unknown)
- [ ] Color channel / trigger behavior confirmed working ✓ (v6, Crystal Caverns v5)
- [ ] Mid-level color transitions confirmed working ✓ (Crystal Caverns v5)
- [ ] Exact orb hit timing window (frame window or pure collision?)
- [ ] Whether pink orb direction depends on current player velocity
- [ ] Gravity portals appear in default level template — investigation needed
- [ ] Safe decoration object IDs — ID 1006 confirmed safe (glow light) ✓. ID 39 = half spike, off-grid anchor, avoid.

---

## Design Pattern — Cave of Glow (Ex_1)
*Studied from Ex_1_Cave_of_Glow.gmd — ground-focused Hard level, Cycles, cave theme*

### Blueprint used
- **Difficulty:** Hard
- **Style:** Ground-focused
- **Theme:** Cave/underground
- **Music:** Cycles (OFFICIAL_SONG_ID = 8)

### Structural observations
- Level is ~71 grid units wide (moderate length for a Hard level)
- Ground is a single layer at grid y=-3 throughout — no chunk fill
- Raised platforms are 4 blocks tall (filled y=-3 to y=0), creating solid walls the player climbs or is blocked by
- Staircase descend: platforms step down 1 block per 2 units (y=0 → y=-1 → y=-2), giving the player time to react
- Pink orbs used throughout as the primary boost — placed at y=0 (ground level, one above surface) — consistent with ground-focused style keeping player low
- One pink orb placed higher at y=1 (grid) for a slightly more dramatic boost in a tighter section

### Spike patterns observed
- Opening: 3 consecutive spikes (x=2,3,4) — immediate Hard-level challenge right at the start
- Double spikes on raised platform surface (x=7,8 at y=-2) — forces a well-timed jump off the raised block
- Spike on raised wall (x=18, y=-2) with pink orb above — teaches orb use to escape
- Spike cluster near end (x=63–67): 5 consecutive ground spikes — climax difficulty spike
- Single spike on raised surface before gap (x=49, y=-1) — mid-level challenge

### Color trigger observations
- Color triggers placed at x<0 (before level start) to set the opening palette
- Warm amber (244, 206, 0) used for the cave glow — matches cave theme perfectly
- Near-black background with warm glow creates strong atmosphere
- ID 1006 (glow lights) placed at y=255 (well above level, invisible to player) — purely atmospheric

### New design patterns to adopt
- **Cave wall technique**: solid filled columns (y=-3 to y=0 or higher) used as walls/obstacles the player jumps over, not just platforms to land on
- **Staircase descent**: stepping platforms down 1 block at a time gives breathing room while maintaining difficulty
- **Pink orb as primary tool in ground-focused**: keeps player close to ground, consistent with style — yellow orb would push the player too high for a cave feel
- **Glow lights (ID 1006)** placed high above the level (y=255) for atmosphere without interfering with gameplay

---

## Version History — Neon Abyss

| Version | Notes |
|---|---|
| v1 | Impossible — ceiling spikes unpassable, orbs too high, pink orb misused |
| v2 | "Pretty good" — physics tuned with player feedback but orbs still at y=2, floating |
| v3 | Boost table applied, orbs/pads corrected, still floating (chunk fill issue) |
| v4 | Ground y=-3 confirmed ✓, spike spacing fixed, "way better!" — remaining issues: post-pad clearance, consecutive gaps, raised gap spike height, pad hovering |
| v5 | "Pretty good!" — most physics fixed. Remaining: raised platform gaps bypassable, yellow orb gap too large, repetitive spike patterns |
| v6 | "Neon Abyss" — colors confirmed working ✓, neon glow blending ✓, background ✓, 4-block orb gap confirmed good ✓. Remaining: gameplay still too repetitive/formulaic, raised platform gaps still not fully forced, default template portals appearing |
| v7 | Pending — fix gameplay variety, suppress template portals, apply decoration |

---

## Version History — Crystal Caverns

| Version | Notes |
|---|---|
| v1 | ID 10 placed as decoration = upside-down gravity portal killing player. Also dead orbs/pads, impossible gaps |
| v2 | Portal IDs fixed, still had floating decoration (ID 44 = bad), dead orbs, raised spike height wrong |
| v3/v3b | Decoration removed, orbs/pads fixed, but single spike directly before triple = ambush |
| v4 | Fixed difficulty curve, one spike per platform gap, all orbs/pads have required gaps |
| v5 | "GREAT JOB" ✓ — mid-level color transitions added, cave darkens through sections, resolves in outro. Best version yet. |
