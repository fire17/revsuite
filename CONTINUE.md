# CONTINUE.md — RevSuite

For a fresh Claude with zero context. Read this first; it is the honest state.

## What this is

**RevSuite** — the rev throttle for Claude Code agents. It governs *how hard an
agent runs*: how many workflows it keeps live, which models it may spawn at each
tier, when it slows down, and how that gear propagates to the agents it manages.
Built for fire17 on 2026-08-15 in a single session, then hardened against a live
fleet that was actually running the mode at the time.

The pieces (all installed by `install.sh`):

| piece | live path | in this repo |
|---|---|---|
| `/rev` gearbox | `~/.claude/skills/rev-reminder/` (alias `rev`) | `skills/rev-reminder`, `skills/rev` |
| `/rev-update` resync | `~/.claude/skills/rev-update/` (alias `rev-sync`) | `skills/rev-update`, `skills/rev-sync` |
| `/highest-rev` fleet mode | `~/.claude/skills/highest-rev/` (alias `highrev`) | `skills/highest-rev`, `skills/highrev` |
| model guard | `~/.claude/skills/workflow-model-guard/` | `skills/workflow-model-guard` |
| preferences | `~/.claude/rev-prefs.toml` | `prefs/rev-prefs.toml` (template) |
| resolver | `~/.claude/scripts/rev-prefs.py` | `scripts/rev-prefs.py` |
| no-caveman hook | `~/.claude/hooks/no-caveman-for-subagents.py` + `settings.json` | `hooks/no-caveman-for-subagents.py` |
| 16 dependency skills | `~/.claude/skills/*` | `skills/*` |

Registry entries for the same work live at `~/Creations/{highest-rev,
rev-reminder,rev-update,rev-prefs,no-caveman-subagents,workflow-model-guard}.md`.

## The design decisions worth knowing

- **Preferences are the authority, prose is documentation.** Every number and
  model (band 5–10, tier-2 Fable, tier-3 Opus 5, forbidden models) lives in
  `rev-prefs.toml`. Skills resolve it at run time so fire17 can change behavior
  without editing a single skill. A live human instruction outranks the file.
- **`/rev-update` deliberately contains no rules** — only the process of
  re-reading and re-activating the suite. That is why it never needs editing
  when the rev system changes; it globs `~/.claude/skills/rev*/SKILL.md` so
  skills added later are picked up automatically.
- **The verbatim laws are SACRED.** fire17's SPAWN LAW (Phase 6 of
  `/highest-rev`), the nested rev directive (Phase 2), and the standing
  close-done-subagents order are stored byte-exact, typos included
  (`parralel`, `IMPORTATNT`, `develompent`, `symultanious`). Never "fix" them.
- **Tier map:** orchestrator → Fable teammates → **Opus 5 only** inside those
  teammates' workflows. Two silent-4.8 traps are documented: an
  `ANTHROPIC_MODEL` env pin (Zenith's worker env pins 4.8) and a custom
  `agentType` frontmatter naming an older opus.

## Current state — honest

**Verified live:**
- Installer: fresh install (23 skills), idempotent re-run (0 installed, 23
  skipped, prefs untouched), existing `settings.json` hooks preserved with no
  duplicate registration, isolated `CLAUDE_CONFIG_DIR` honored (proved by a
  5–99 band reading from a temp prefs file).
- Resolver: defaults resolve; `conserve` profile layers to 1–3/fleet 2; unknown
  profile exits 2 listing valid names; missing/malformed TOML degrades to
  built-in fallbacks with a warning instead of blocking.
- No-caveman hook: both detection paths emit the override (parent-argv and env
  fallback); a main session emits nothing.
- Verbatim laws: byte-compared after every edit round.
- `/highest-rev` ADOPT mode: exercised by a real fleet (session `ltx-attempt2`)
  — it inventoried 23 worktrees, reused an existing `.grand/BUDGETS.md`,
  reconstructed a corrupt `VISION.md` into a dated file without touching the
  original, and wrote `ADOPTED.md`.

**NOT yet live-verified:**
- The no-caveman hook on a *freshly spawned* teammate (the four live ones
  predated the hook and were corrected verbally).
- `/rev up` / `/rev down` propagation through a real multi-tier fleet.
- `/rev-update` fired at a running fleet.
- A per-project preferences override or a named profile used in a real run.
- The tier-3 Opus 5 verification step observed on a real teammate's workflow.

## How to resume

```bash
claude --resume 4e08c44e-8cc9-4de4-99c8-d77685034ea0     # from ~/Creations
```

Or read `conversation/4e08c44e-8cc9-4de4-99c8-d77685034ea0.jsonl` (verbatim,
`cmp`-verified copy) plus `conversation/cship-*.json` for model/cost provenance.

## Next steps

1. Close the NOT-yet-verified list above, starting with a fresh teammate spawn
   to prove the caveman override lands in its context.
2. Use a profile and a per-project override in a real mission.
3. Consider a `/rev status` that prints resolved prefs + the live band without
   changing gear.

## Related, not copied

- `~/Creations/CLAUDE.md` — the registry god file (rule 4 carries the HIGHREV
  exception).
- `~/.claude/settings.json` — holds the hook registration. NOT copied here (it
  can contain machine-specific permissions); `install.sh` re-creates the two
  entries idempotently.
- The full quality stack `/highest-bar` activates (impeccable,
  master_engineering + book payload, ladder-abstraction) ships in
  `github.com/fire17/highest-bar`, deliberately not duplicated here.
