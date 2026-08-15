---
name: pyramid
description: fire17's hierarchical agent-orchestration doctrine — how a Fable main session runs opus agent swarms (agentteams/tmux or Agent-tool teammates) where every opus lane may offload to up to 3 verified SONNET classic subagents, with park-on-pause, the never-Fable model guard, engineering-principles-grade briefs, and directive inheritance down every tier. Load this WHENEVER spawning opus agents, building an agent swarm/fleet, fanning out review or build lanes, delegating heavy work from a Fable session, or when the user says "pyramid", "opus agents", "agent swarm", "fan out", "spin up workers", "orchestrate this", or asks to conserve opus tokens — even if they don't name the skill. Also load it BEFORE resuming a paused fleet and when a pause/park order might arrive mid-mission.
argument-hint: "[mission or wave to orchestrate — e.g. 'review wave: 5 lanes' or 'resume paused fleet']"
---

# /pyramid — the hierarchical agent doctrine

One conductor, opus lanes, sonnet helpers. This skill exists because the pattern below
repeatedly produced verified, high-quality parallel work at a fraction of the token cost —
and because every failure mode it guards against (Fable subagents, unverified worker
claims, killed-instead-of-parked fleets, directives lost between tiers) has actually
happened. Each rule carries its why.

## The pyramid (three tiers + the ground it stands on)

```
        FABLE (main)      — conducts, judges, integrates. Never bulk-works.
       /   |   \
   OPUS  OPUS  OPUS…      — the workhorses: build / review / validate lanes.
   /|\    |     /|\
  S S S   S    S S S      — ≤3 SONNET classic subagents per opus, opus-verified.
─────────────────────────
  engineering principles  — every tier's briefs are built from them (see §5).
```

### Tier 0 — Fable main: the conductor
- **Orchestrate; don't bulk-work.** Main stays lean and AVAILABLE to the user at all
  times (a head-down main is a UX failure and a token failure at once). Heavy reading,
  building, and reviewing go to lanes; main decomposes, briefs, integrates, judges, and
  owns the single accountable judgment — an orchestra with two conductors is noise.
- **NEVER spawn Fable subagents.** Every spawn carries an explicit `model:`. Omission is
  the trap: spawns inherit the main-loop model, and main may be Fable. Load
  `/workflow-model-guard` BEFORE authoring any wave, grep-verify no naked spawns, and
  announce the banner (see §6) before/at launch AND before every resume.
- **Single-writer surfaces stay with main** (release notes, version files, the steward
  CLAUDE.md, memory) — workers report, main writes. Two writers on a hub file is a
  drift factory.
- **Main verifies independently, by sampling.** A worker's "it works" — carbon or
  silicon — is a claim, not evidence. Re-run a test, read a diff, run the real binary
  with your own hands on at least a sample of every lane's output. Trust is a sampling
  strategy calibrated to track record, not a feeling.

### Tier 1 — Opus lanes: the workhorses
- **Model/effort:** `opus` @ high is the default; xhigh for the hardest design/review
  lanes. Spawn as agentteam/tmux swarm lanes for interactive, steerable work, or
  Agent-tool teammates for background lanes — match the transport to the work's shape.
- **Scopes are disjoint.** Each lane owns an explicit file/dir scope; hub files
  (Makefiles, main.go, shared styles) get exactly ONE owner per wave. Shared-file
  contention is a reason for worktrees or sequencing, never for silent collisions.
  In a multi-writer tree, every commit stages explicit paths — `git add <its files>`,
  NEVER `-A`/`.`: a blanket add once swept a sibling lane's half-landed files into one
  lane's commit, and a caller who committed with no implementation left HEAD alone
  (AttributeError). Explicit paths keep each lane's commit its own.
- **tmux swarm hygiene:** teammate swarms land on a socket named
  `claude-swarm-<lead-pid>` — resolve it by the LEAD's actual pid, never by guessing
  (killing someone else's swarm is a real, near-missed accident). Cleanup sequence when
  standing a fleet down: active lanes finalize a short progress summary → clean
  shutdown → tear down THAT swarm only → fresh swarm for remaining work — main stays
  available throughout.
- **Fleet hygiene, continuously:** audit-prune-respawn as phases change — close lanes
  whose work is behind you before spawning the next wave; every open task that needs
  work has exactly one owner; no stalls (anything that can hang gets a timeout and a
  fallback, and waiting time is spent thinking or preparing, never idling).
- **Idle ≠ done (learned live, audiotop mission 2026-07-06):** a lane emits idle
  notifications whenever it ends a turn — including while its sonnets are still
  out. On a lane's FIRST idle, ping it to deliver; if it answers "not done, sonnets
  in flight," let subsequent idles pass silently until its report arrives. If a
  lane sits idle long past its ETA, ping with "partial-but-honest beats waiting:
  send what you've verified, flag what's pending" — lanes then deliver a verified
  brief plus addenda deltas as stragglers land. Main integrates incrementally;
  never block the whole mission on the slowest lane's last citation.
- **Every opus brief embeds, verbatim:** its outcome spec + acceptance test, its
  boundary contract (explicit scope, explicit prohibitions), the escalation clause,
  the sonnet rules of Tier 2, the park protocol of §4, and the report format of §5.
  Why verbatim: delegation fails at the spec, and a model fills spec gaps with
  confidence, not common sense. What a tier isn't told, it improvises.

### Tier 2 — Sonnet helpers: the offload (the rule this skill exists to enforce)
Each opus lane MAY — and, to conserve opus tokens, is encouraged to — spawn up to
**3 sonnet subagents**. Hard rules, which every opus brief must carry verbatim:
1. **Classic subagents only** — normal (non-tmux, non-agentteam) Task/Agent subagents.
   They are ephemeral tools of their opus, not fleet members.
2. **Cap: 3 per opus,** context handed down ONLY from the spawning opus — a sonnet
   knows exactly what its opus tells it, nothing else. Phrase their tasks so the
   answer can come back either way (a fresh window is a fresh witness — use it).
3. **The opus manages and verifies EVERYTHING sonnets return.** Sonnets make more
   mistakes than opus: re-run their tests, read their diffs, check their claims
   against disk. The opus owns the result as if it wrote it — "my sonnet said so"
   is never evidence.
4. **Unless a sonnet's result is perfect, ask: "is there anything better that could
   be done?"** — and improve it before integrating. Perfect results pass; everything
   else gets the opus's own hands on it.
5. **Sonnets never spawn further agents** and never touch single-writer or hub files.
   The pyramid is three tiers deep, full stop.
- Haiku remains allowed for trivial logistics only, with an escalation clause — never
  for judgment or code that matters.

## §4 · The park protocol (pause ≠ kill — this was learned the hard way)
When the user says pause/stop/park (tokens out, attention needed, anything):
1. **PARK, immediately, tier by tier:** main messages every ACTIVE lane "PARK NOW:
   stop all work this instant, stay resident, await resume." Each opus instantly
   relays the same order to its live sonnets. Speed matters — active agents are
   burning tokens while you compose prose.
2. **Do NOT terminate.** Parked/idle agents burn ZERO tokens but keep their working
   context; killed agents leave half-written files and force finish-or-revert triage
   on resume. Kill (TaskStop) only when the user explicitly says close/kill/clean up.
3. **After parking** (never before — parking is the urgent half), main writes a durable
   checkpoint: mission state, per-lane status + verified/unverified marks, in-flight
   file scopes, exact resume sequence, decisions owed by the user.
4. **On resume:** message "resume" to parked lanes — they continue with context intact.
   Re-run the model-guard banner before any NEW spawns.

## §5 · Briefs are built from the engineering principles
Load `/engineering-principles` (master) or its pro/quick-essentials editions as the
lens; `/master_engineering` for the delegation disciplines. The parts every brief in
the pyramid embeds:
- **Escalation clause, verbatim, every tier:** "If you're stuck, the fix exceeds your
  scope, or something feels architecturally wrong — say so and STOP. Never guess;
  wrong guesses compound and become load-bearing. Struggling silently is the only
  failure that won't be forgiven."
- **Evidence or it didn't happen:** every claim in a report carries a `file:line` or
  verbatim command output. Reviews mark unverifiable items UNVERIFIED rather than
  guessing. Verification runs the REAL surface (build the binary, drive the flow),
  not source-reading alone.
- **Ground truth beats memory:** workers re-derive state from disk, never from what
  the brief remembers being true; concurrent-writer trees make transient reds normal —
  rerun before believing a failure, never revert another agent's in-flight change.
  Before declaring a shared tree quiescent, identify the WRITERS, not just mtimes —
  read `~/.cship/live/*.json` for live sessions holding that cwd (a tree "quiescent 11h"
  by memory was being written that morning by a foreign 4-lane fleet; cship snapshots
  named them in seconds).
- **Report format (fire17's):** numbered tables, progress bars (full bars even when
  done), ETAs with stated basis, deltas since last report; outcome first.
- **Durable ledger:** lane reports, checkpoints, and adjudication digests persist to
  the mission's working dir (e.g. `.deify/` or a review dir) as they land — written
  ≈ real; anything only-in-context dies with the window.
- **The user's words are sacred:** capture directives verbatim, derive after, never
  blur the two. New standing directives get a memory file in the same pass.

## §6 · The banner (announce before every launch and resume)
```
╔══════════════════════════════════════════════════════════════╗
║  ✅ PYRAMID MODEL GUARD — NO FABLE BELOW THIS LINE            ║
║  <lane>  → opus @ <effort>   (may run ≤3 verified sonnets)   ║
║  <lane>  → opus @ <effort>   (may run ≤3 verified sonnets)   ║
║  logistics → haiku @ <effort> (escalation clause armed)      ║
╚══════════════════════════════════════════════════════════════╝
```
List every lane with model + effort (say "effort: inherited (<session effort>)" when
not explicitly set). Verified by grep, not assumption.

## §7 · Ready-to-paste brief boilerplates

**Into every OPUS brief (append after its task/scope):**
> SONNET OFFLOAD: you may spawn up to 3 sonnet classic (non-tmux) subagents to take
> workload off you, each briefed only with context you hand it. You must manage and
> verify EVERYTHING they return (sonnets err more than you): re-run their tests, read
> their diffs; unless a result is perfect, ask "is there anything better that could be
> done?" and improve it before integrating. You own their output as if you wrote it.
> They never spawn further agents and never touch single-writer/hub files.
> COMMIT BEFORE REPORT: commit your scoped work (explicit-path `git add`) BEFORE you
> report done or go idle — an idle lane with uncommitted work opens a coherence window
> siblings trip on, and main should never have to commit for you.
> PARK PROTOCOL: if you receive a PARK order, stop all work THIS INSTANT, relay PARK to
> your live sonnets, stay resident, await resume. Do not write handoffs unless asked.
> ESCALATION: if stuck, out-of-scope, or something feels wrong — say so and STOP.
> REPORT: numbered changes with file:line, test names, verbatim verification tails.

**Into every SONNET brief (the opus writes this):**
> You are a scoped helper. Do exactly this task within these files: <scope>. Everything
> you know is in this brief — verify against disk, never assume. If stuck or the task
> exceeds this scope, say so and STOP — never guess. Do not spawn agents. Report with
> file:line evidence and verbatim command output. If a PARK order arrives, stop
> instantly and stay resident.

## §8 · Economics (why the pyramid is shaped like this)
Time is bought with parallelism, money with model choice — quality with neither.
Fable's window is the most expensive surface in the system: spend it on decomposition,
contracts, judgment, and integration — the moments where one decision saves a thousand
corrections. Opus buys correctness on real work; sonnet buys throughput under opus
supervision; haiku buys logistics. The invoice is part of the output: estimate before
big runs, and when the user sets a budget or says tokens are scarce, bias down-tier
and shrink scopes — but never below the verification floor: an unverified cheap result
is the most expensive thing in the building.
