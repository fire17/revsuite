---
name: smart-trim
description: Cut a video (or Remotion timeline) down to a target length intelligently — importance-weighted scene trimming that NEVER speeds up animations or changes content pacing; time is reclaimed from dead lead-ins, static tails, hold shots, and oversized cards, while high-value beats (typing, output reveals, key transitions the timing was chosen for) keep their full real-time length. Use when the user asks for a shorter cut/version of a video ("make it half as long", "60% version", "tighter cut", "trim the demo"), /smart-trim, /strim.
argument-hint: "<video-or-composition> <target length or %> [notes]"
user-invocable: true
---

# smart-trim — importance-weighted cuts, animations untouched

Distilled from the betterkill demo 82s→47s cut (2026-07-10, cycle 11). Sibling of the
`demo-video` skill (`~/.claude/skills/demo-video` — its Remotion pipeline is the main host).

## The method

1. **Inventory segments** with current durations and a value class each:
   - **content beat** (typing, output reveal, the moment the scene exists for) — protected,
     runs 1x, full length
   - **establishing/hold shot** — compressible (keep a beat, cut the plateau)
   - **card** (title/quip/CTA) — floor = type-on time + ~1.5s read; trim the rest
   - **dead time** — lead-in sleeps, baked static tails, long outros — reclaim ~all of it
2. **Reclaim dead time FIRST** — it usually funds most of the target:
   - Remotion: `trimBefore` on the video element skips recorded lead-in sleeps (a CUT, not a
     speed change); shrink `clipFrames` to drop baked static tails — a last-frame PNG hold
     covers the end state identically.
   - Raw video: ffmpeg segment concat of keep-ranges (`-ss/-to` per segment, then concat).
3. **Distribute remaining trim proportional to (duration − floor) × (1 − importance)** — big
   low-value segments give the most; every segment keeps its floor.
4. **Rebuild the timeline** (new section table + rescaled camera keyframes so moves stay
   gentle — see demo-video's MOTION SICKNESS and NO MICRO-JINKS gotchas), render, then run the
   **flashbang gate** (`demo-video/scripts/flashbang_check.py`) + frame-QA before delivery
   (VLC per fire17's protocol).

## Gotchas (live-earned)

- "Shorter" ≠ "faster": time-compressing animations/typing reads as a glitch and violates the
  ask — cut time BETWEEN beats, never inside them.
- Trimming a clip's tail is safe only when the tail is static — verify the last shown frame
  matches the hold image content.
- After shortening a scene, RESCALE its camera keys to the new length — keeping old absolute
  frames turns gentle ramps into whips.
- Card floors: type-on cps × chars + ~45 frames read time; below that, text isn't finishable.
- Keep the full-length master composition intact; the cut is a NEW composition/file
  (`Demo` + `Demo60` pattern) — both stay renderable.

*Provenance: distilled 2026-07-10 from the live 82s→47.3s betterkill cut (Demo60.tsx),
flashbang-gated, under /dnl.*
