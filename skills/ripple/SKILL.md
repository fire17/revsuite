---
name: ripple
description: The AUTO-PROPAGATION LAW for fire17's ecosystem — once anything has been shipped/published (it carries a .project marker, or its registry entry says published), EVERY later change to it or to anything it's referenced by must automatically ripple outward - update every reference across every surface (vault copies, aliases, snapshots, doc-mentions, registry) and stage a REPUBLISH of every affected published project, with ONE user confirmation covering the whole wave. This behavior is DEFAULT-ON and self-triggering; the user must never have to ask for it. Trigger this skill whenever ANY of these happen, even if the user never names it: a change lands in a project that was published before; a skill/file referenced by a published project is edited; /dnl, /sas, /shipit or skill-creator finish updating something that was shipped in the past; the user says "push", "update everywhere", "republish", "sync all references", "don't let things get outdated", or asks which projects a change affects. Also use for querying the dependency graph itself ("what depends on X", "what breaks if I change Y"). Runs scripts/ripple_graph.py — a lightweight, cycle-safe, multi↔multi flagged pseudo-dependency graph over all creations, skills, vault copies and snapshots.
argument-hint: "[node|changed-path] — e.g. shipit, or a file you just edited; empty = check current project"
---

# ripple (alias: rpl) — one stone, every pond

fire17's standing order, verbatim core: *"once changes have been made to a project that
has been published in the past or is referenced in a project that was published by us in
the past - then all of this behavior must happen by itself automagially"* — he was
repeating "remember to update all the references and republish related projects" many
times a day. This skill makes saying it zero times the default.

**The law:** publication creates a standing obligation. Shipping something once means
every later change to it — or to anything it references — owes the world an update.
The `.project` marker is how a directory remembers that obligation, and the graph is
how we find everyone the obligation extends to.

## The engine

`~/.claude/skills/ripple/scripts/ripple_graph.py` (stdlib-only, fast):

```bash
python3 ~/.claude/skills/ripple/scripts/ripple_graph.py scan            # rebuild graph cache
python3 ~/.claude/skills/ripple/scripts/ripple_graph.py affected <node> # who depends on X
python3 ~/.claude/skills/ripple/scripts/ripple_graph.py check <paths…>  # dirty files → ripple report (noise-filtered)
python3 ~/.claude/skills/ripple/scripts/ripple_graph.py markers [--refresh]  # all .project markers, lazily cached
python3 ~/.claude/skills/ripple/scripts/ripple_graph.py ensure-project <slug> [--dir] [k=v…]
python3 ~/.claude/skills/ripple/scripts/ripple_graph.py backfill        # markers for all published
python3 ~/.claude/skills/ripple/scripts/ripple_graph.py selftest        # prove cycle-safety + noise filter
```

- **`project_markers()` — the programmatic marker registry.** Importable
  (`sys.path.insert(0, "~/.claude/skills/ripple/scripts"); from ripple_graph import
  project_markers`) and CLI (`markers`). Auto-discovers new `.project` files/dirs via
  a bounded, pruned walk — and is LAZY: repeat calls hit a validated cache
  (`~/Creations/.ripple/markers.json`) in ~0.1ms; a deleted marker invalidates
  instantly (stat fails), a new one is seen at TTL expiry (300s) or `--refresh`.
  Measured live 2026-07-06: cold 15ms, warm 0.1ms.

- **Nodes**: every registry creation, every live skill, every vault copy, every /sas
  snapshot. **Edges**: directed, multi↔multi, each carrying a SET of flags (`alias`,
  `vault-copy`, `snapshot`, `doc-mention`, `declared`, `symlink-canonical`) — one link
  can be several kinds at once, and new flags cost nothing.
- **Cycle-safe by construction**: every traversal is BFS with a visited set — mutual
  references, diamonds and self-loops all terminate (proven by `selftest`). Never walk
  references by hand; that's how loops and misses happen.
- The cache lives at `~/Creations/.ripple/graph.json`. It's derived state — when in
  doubt, `scan` (cheap, ~1s) rather than trust a stale cache. Edges the scanner can't
  see get **declared** in a `.project` (`refs-out: target:flag …`) — curation beats
  guessing.

## The .project marker (the gate)

Created **the first time something ships** (shipit and /sas both do this; `backfill`
covers the pre-law era). Its PRESENCE is the gate: a directory with a `.project` has
been published before, so changes inside it always require a ripple check.

Format — deliberately liberal (any structured/unstructured combo, line-separated):
`#project v1` header · flat `key: value` lines (slug, status, version, repo,
first_shipped, last_shipped, channels, refs-out…) · a `---` separator · freeform
below it, never parsed, preserved verbatim. Both forms are legal: a `.project/` DIR
whose status file is `.project/status` — the DEFAULT for anything pushed to GitHub,
since richer state stores naturally as sibling files — or a lightweight `.project`
FILE for local-only projects (the tools read both transparently; `ensure-project
--dir` creates or upgrades to the dir form, content preserved).
Full spec: `references/project-file.md`.

## The default-on flow (what "automagic" concretely means)

Whenever you finish changing anything — inside /dnl, /sas, /shipit, skill-creator, or
just plain editing — before declaring done:

1. `check <changed paths>` (or `affected <node>`). If the gate is closed (never
   shipped, nothing shipped affected) — done, no ceremony.
2. Gate open → **update every reference now, in the same pass**: re-sync vault copies
   (`sync_skill.py`), refresh snapshots' `.new-` deltas if hand-edited, fix
   doc-mentions whose content went stale (a mention that merely names the node needs
   no edit — judge by content, not by edge existence), bump registry entries
   (three surfaces + changelog), refresh `.project` (`last_updated`, version).
3. **Stage the republish wave**: every affected node marked REPUBLISH gets its update
   ship prepared via /shipit's update-run path (version bump, changelog, re-verified
   install). Present the whole wave as ONE batch and ask for ONE confirmation —
   nothing leaves the machine without it (the confirmation is batched, never skipped).
4. Record: the ripple report (what updated, what republished) goes in your final
   report, and `.project` `last_shipped` is bumped on each node that actually shipped.

## Judgment notes (why not a dumb cascade)

- **A `.project` marker NEVER means auto-republish.** It means *check required*. The
  republish decision has three gates in series: (1) the engine's noise filter — OS
  droppings, caches, `.git`/`.save_and_ship`/`.project` internals never open the gate
  (else refreshing a marker would trigger the wave it exists to gate); (2) relevance —
  does the change touch shipped-artifact content? (/sas's per-node delta gate enforces
  this: reference updates without artifact deltas get no version bump); (3) the user's
  ONE batched confirmation — REPUBLISH in a report always means STAGED, nothing ships
  itself.
- The graph gives you the SUSPECT list; you decide per node whether content actually
  went stale. Edges err toward over-reporting (doc-mention is deliberately broad) —
  triage them, don't blindly rewrite 30 files.
- Hop-1 dependents almost always need attention; deeper hops usually only when the
  hop-1 update itself changed their content (the ripple re-runs naturally as you
  update each layer — the visited-set means this converges, never loops).
- Never republish for nothing: /sas's delta gate still applies per node — an affected
  project whose own artifacts didn't change gets its references updated but no
  version bump.

## Provenance

Distilled 2026-07-06 from fire17's ripple directive (Seeds S38, verbatim preserved) —
built, cycle-selftested, and live-verified same day: `affected shipit` correctly
surfaced 30 dependents (1 republish), and `check` on an edited shipit file walked
path → node → open gate → report.
