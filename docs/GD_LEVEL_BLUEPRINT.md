# GD Level Blueprint
*Work through every section before writing any code. These decisions shape the entire level.*

---

## Difficulty
Choose one: **Easy / Normal / Hard / Harder / Insane / Demon**

Decide this first — it sets the ceiling for how punishing gaps, spike spacing, and timing windows can be. Every design choice should be consistent with this rating.

---

## Gameplay Style
Choose a primary style (and note any secondary influences):

- **Orb-heavy** — player is frequently in the air chaining orbs, rarely touching the ground. Vertical space and orb placement are the main design challenge.
- **Ground-focused** — player stays low, jumping over spikes and obstacles without going high. Tight horizontal rhythm, minimal orb use.
- **Gravity-heavy** — frequent gravity flips are the core mechanic. Requires careful ceiling and floor design on both sides.
- **Mixed** — draws from multiple styles. Still pick a *lean* — what does the level feel like most of the time?

Note which orbs and pads are in play, and which are off-limits for this level's style.

---

## Theme
Pick a visual theme, but **keep it simple**. You have a limited block vocabulary — don't overreach. A well-executed simple theme is better than a broken complex one.

Examples:
- Standard GD style — clean blocks, spikes, no heavy decoration
- Cave/underground — dark palette, enclosed corridors
- Sky/cloud — open vertical space, light colors
- Neon/cyber — glowing colors, blending enabled

Describe the theme in one or two sentences. Then note what colors support it (refer to the color journey section when filling that in). Do not plan decoration using block IDs you haven't confirmed — stick to known-safe objects.

---

## Music
Pick a song that matches the theme and gameplay style. The song sets the pace of everything.

- **Fast, intense songs** → harder difficulty, more orbs, more clicks, more chaos
- **Slow, atmospheric songs** → easier or more methodical gameplay, ground-focused, fewer orbs, more breathing room

Choose from the official GD song list (use `OFFICIAL_SONG_ID`). Note which song and why it fits the theme and gameplay style you chose. Then consider: does the beat suggest where spikes and orbs should land? Fast songs with lots of notes push toward orb-heavy. Slow songs with sparse beats push toward ground-focused rhythm.

**Reminder from design notes:** Place spikes *after* the beat mark, not on it — the player jumps when they hear the note, so the hazard should arrive a beat later.

---

## Filled Example — Ex_1 Cave of Glow

**Difficulty:** Hard
**Gameplay Style:** Ground-focused. Pink orbs only — keeps player low. No yellow orb (would push too high for cave feel).
**Theme:** Cave/underground. Dark background, warm amber glow lights (ID 1006 at y=255), single-layer ground, filled block columns as walls. Simple and effective — no unconfirmed decoration IDs.
**Music:** Cycles (OFFICIAL_SONG_ID = 8) — driving rhythm suits a ground-focused Hard level, beat naturally suggests spike placement.

*Key design decisions that followed from these choices:*
- Ground-focused → pink orb as primary boost, not yellow
- Cave theme → filled wall columns, near-black palette, amber glow
- Hard difficulty → opens immediately with 3 consecutive spikes, climaxes with 5-spike run
- Cycles' rhythm → spike clusters land after beat hits, not on them
