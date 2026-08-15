# The .project marker — full spec (v1)

## Purpose

A `.project` marks a directory as **shipped-at-least-once** and carries its current
state. Its presence is the ripple gate: once it exists, every change inside that
directory (or to anything the graph says references it) triggers the ripple flow —
update all references, stage republish of affected published projects. It is created
the FIRST time a project ships (by /shipit or /sas; `ripple_graph.py backfill` covers
projects published before the law existed) and refreshed on every later ship.

## Two forms — file or dir, both first-class

- **Dir** (default for anything pushed to GitHub — fire17's call, 2026-07-06):
  `<project-root>/.project/` with the marker at `.project/status`, plus any other
  state files the project wants beside it (metrics, notes, machine state…) — more
  data stores naturally as sibling files than crammed into one. `ensure-project
  <slug> --dir` creates it, and upgrades an existing file in place (content preserved).
- **File**: `<project-root>/.project` — one lightweight marker file; fine for
  local-only / not-yet-repo projects.

All tooling reads both transparently (`project_marker_path()` resolves file-or-dir).
Either one or the other exists — never both.

## Format — any structured/unstructured combo, line-separated

```
#project v1
slug: shipit
status: published
version: v0.4.1
repo: https://github.com/fire17/shipit
channels: github, brew
first_shipped: 2026-07-06
last_shipped: 2026-07-06
last_updated: 2026-07-06
refs-out: sas:chains-to awesome-readme:doc-mention
---
anything below the separator is freeform: prose, JSON blobs, logs, TODO scraps —
never parsed, always preserved verbatim by the tools.
```

Rules:
- `#project v1` header line.
- Before the first `---`: flat `key: value` lines are structured metadata; anything
  else (blank lines, comments, stray prose) is tolerated and preserved.
- After `---`: freeform, verbatim, forever. Tools rewrite the structured block but
  never touch the freeform tail.
- **`refs-out`** is the curated-edge escape hatch: space-separated `target[:flag]`
  tokens that add graph edges the scanner can't discover (runtime deps, data files,
  cross-repo links). Targets are node ids (registry slugs / skill names).

## Well-known keys (extend freely — unknown keys are fine)

| key | meaning |
|---|---|
| `slug` | registry slug / node id |
| `status` | published · shipped · working · … |
| `version` | last shipped version |
| `repo` | canonical remote |
| `channels` | where it's published (github, brew, npm, …) |
| `first_shipped` | the day the marker was born — the gate's start |
| `last_shipped` | bumped by every ship that leaves the machine |
| `last_updated` | bumped by any tool touch |
| `refs-out` | declared outgoing edges (see above) |

## Who writes it

- **/shipit**: creates it on a first ship (publish phase), bumps `version`/
  `last_shipped`/`channels` on update runs.
- **/sas**: ensures it exists when the ship half runs; records the snapshot in
  freeform if useful.
- **/ripple**: `ensure-project`, `backfill`, and reads it for the gate + declared edges.
- **Anyone else**: welcome — it's a marker, not a lock. Keep the header and the
  separator convention and the tools stay happy.
