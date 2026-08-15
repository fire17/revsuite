---
name: highest-rev
description: MAXIMUM-THROUGHPUT orchestration mode — fire17's HIGHREV doctrine. Runs the full /highest-bar founding-vision protocol PLUS a fleet of simultaneous tmux teammate-mode Fable @ high subagents, each running multiple ultracode dynamic workflows with worktrees, all the time. Includes a dedicated INIT stage that truly ACTIVATES every stack skill one by one behind a written-first checklist (activation ≠ execution — no skill's side-quest may push later activations), preserves the SACRED verbatim rev directive (nested by design — each tier obeys it AND transmits it one level down) plus the verbatim SPAWN LAW every teammate carries (work until utterly perfect; hold 5–10 live workflows at all times, never under 5), fixes the model map per tier (teammates Fable, the agents inside their workflows Opus 5 ONLY — never 4.8/sonnet/haiku), and defines the orchestrator loop — big picture, constant progress-rate gauging, help struggling subagents, reap done ones fast after they log, constantly spawn more. Activating this mode is the explicit trigger /workflow-model-guard watches for: its HIGHEST-REV override ruleset then governs (Fable lanes sanctioned; explicitness, verification, banner still mandatory). ACTIVATION is exactly four explicit forms — the user types /highest-rev or /highrev, or writes "HIGHEST-REV" or "HIGHREV". Fuzzy asks ("high rev", "rev up to the max", "step on it", "blaze through this", demands for maximum parallel speed) load this doctrine for READING but do NOT activate the mode — a skill-description match is never activation; quote the user's literal activation turn before any Fable spawn.
argument-hint: "<the mission — what to build/advance at maximum rev>"
---

# /highest-rev — HIGHREV mode: the highest bar at maximum rev

/highest-bar answers "how good must it be" (best anyone has ever seen).
/highest-rev adds "how fast must it move" (maximum parallelism, every tier, all
the time). This skill INCLUDES the full /highest-bar protocol — all of its laws
stand EXCEPT its never-Fable model lines, which the guard's HIGHREV override
supersedes while the mode is active — and wraps it in a fleet doctrine: the main
agent orchestrates many simultaneous Fable @ high tmux teammates, each of which
drives many simultaneous ultracode dynamic workflows with worktrees. Speed is a
duty here, not a vibe: idle capacity while open work exists is a defect.

**"ultracode", defined (disk truth per /effort-set + /identify):** the TOP
reasoning-effort tier — session-only, above xhigh, the "ultracode" label —
enabled via `/effort ultracode` (the /effort-set skill). An "ultracode dynamic
workflow" = a dynamic Workflow-tool run authored while that tier is enabled;
"many symultanious ultracode s (plural)" = many simultaneous Workflow
invocations running at once. "Fable high class" names the spawn tier: model
Fable, the highest class. Each fleet teammate raises ITSELF to ultracode effort
at startup (first duty, via /effort-set) — the tier is never assumed inherited;
the workflows it authors still set per-agent() effort deliberately (guard law).

## Phase 0 — VERIFY ACTIVATION, then DECLARE THE MODE

1. **Verify the trigger FIRST — before any declaration.** The mode NEVER
   self-activates. It is active ONLY if the user's own turn contains one of the
   four explicit forms: `/highest-rev`, `/highrev`, "HIGHEST-REV", "HIGHREV".
   QUOTE that literal user turn now — a slash invocation IS the activation turn
   (quote it as `user typed: /highest-rev`, noting accompanying prose
   separately). A skill-description match, a fuzzy ask ("blaze through this",
   "step on it"), task ambition, or urgency is NOT activation — in that case
   read the doctrine, do NOT declare, and ask the user whether to activate.
2. Print the declaration: **HIGHREV ACTIVE** — session-scoped, user-triggered
   (quoted in step 1). **Steps 1–2 are the mode's FIRST OUTPUT: printed before
   any tool call, before Phase 0.5's inventory.** The inventory is actionable
   and will try to jump the queue — that is the same push-later failure the
   init checklist exists to stop, one level up. If a tool already ran under
   this activation undeclared, declare NOW and note "late declaration" on the
   ledger. (Observed live 2026-08-15: an otherwise-correct run skipped both.)
3. This activation is exactly what `/workflow-model-guard` watches for: its
   **§HIGHEST-REV override** now governs every spawn this session — Fable lanes
   sanctioned; explicit model on every spawn still mandatory; the HIGHREV banner
   printed before launches; the `MODEL:` first-line tripwire still on.
4. The mode ends at "highrev off" / "normal rev" / a user budget concern /
   session end — always via the §SPIN-DOWN procedure below, after which the
   guard's default never-Fable rules resume instantly.
5. **Precedence check.** If a project CLAUDE.md in this tree carries an
   unconditional never-Fable rule, HIGHREV does not silently override it: print
   the conflict, state that `/highest-rev` + the guard's §HIGHEST-REV override
   is the sanctioned exception, and take ONE explicit user confirmation before
   the first Fable spawn (once per session, logged on the ledger). The Zenith
   `ANTHROPIC_MODEL` pin stays opus regardless.
6. Budget frame: the user has granted a huge development budget for this mode.
   Tokenomics tracking stays ON — concretely: activate `/tokenomics`, record a
   cost + context baseline (`/identify` or cship-data) on the ledger, and show
   cost + 5h/7d limit % as a header line above the fleet table every gauge
   cycle. Measure everything, economize nothing.
7. **Effort:** the MAIN agent raises ITSELF to ultracode at init too — it holds
   rev per Phase 3's trailing block, not just delegates it.

## Phase 0.2 — LOAD THE USER'S PREFERENCES (before anything is sized)

```bash
python3 ~/.claude/scripts/rev-prefs.py            # add --profile <name> if asked for one
```

`~/.claude/rev-prefs.toml` is **the authority** for every number, model, and
toggle this mode uses: the workflow band, the fleet minimum, the model at each
tier, the forbidden models, the teammate effort tier, the housekeeping switches.
The values written in this skill are the current defaults for reference only —
**resolve them fresh from the file every run**, since fire17 changes them
without touching any skill. Per-project overrides resolve by path prefix
automatically, and named profiles (`--profile conserve|max|solo|…`) layer over
the defaults when the user asks for one.

Print the resolved block on the ledger, and size every later decision — band,
fleet, spawn models — from THOSE values. Anything the user says live outranks
the file; state the override and follow it.

## Phase 0.5 — ADOPT the ground truth (mandatory when the project is non-empty)

HIGHREV has TWO entry modes. **NEW** (empty/greenfield): highest-bar Phase 0
runs as written. **ADOPT** (the project dir already holds work — the common
case mid-mission): prior work is reconciled, NEVER regenerated. Before the init
checklist:

1. **Inventory disk truth** (read-only): existing doctrine/protocol artifacts
   wherever they live (VISION/BUDGETS/IA/PATTERNS/SWARM/DARWIN and their local
   equivalents — a plan or spec doc may already serve a phase's role), project
   CLAUDE.md files, ledgers, handoff docs, repos + branches, `git worktree
   list`, recent file mtimes, running processes, and every drained teammate's
   work log.
2. **Read every prior work log and handoff doc BEFORE writing any brief.**
3. **Produce `ADOPTED.md`** — one row per prior lane: what it did · where its
   output lives · branch/worktree · status done|partial|abandoned · REUSE or
   SUPERSEDE. No fleet spawn may re-open a lane marked done without stating
   why; every brief carries its lane's rows.
4. **Baseline snapshot** — record the pre-existing branch/worktree set. Only
   lanes THIS session creates are bound by the "nothing stranded unmerged"
   clause; pre-existing experiment branches are adopted as-is and never merged
   or pruned to satisfy the rule.
5. **Print a one-screen STATE OF THE MISSION block**, then start the checklist.

**VISION.md, mid-flight:** if it exists, do NOT overwrite, paraphrase, or
regenerate it (SACRED) — read it and check it actually states the project's
vision. If it is absent, truncated, or holds something else (e.g. a fragment of
the rev directive), do NOT invent one: quote the earliest user mission text
verbatim from the transcript into a NEW `VISION-<date>.md`, leave the original
byte-untouched, and record `> vision: RECONSTRUCTED mid-flight from
<transcript> — NOT byte-verified` instead of claiming a passed checkpoint. The
rev directive belongs in Phase 2 ONLY — never write it into VISION.md. Missing
paste never HALTs the mode.

## Phase 1 — INIT: activate ALL the skills, one by one, behind a checklist

The failure this stage exists to prevent: a freshly-activated skill starts DOING
things (planning, auditing, spawning), and the remaining activations get pushed
later — or forgotten. The countermeasures are law:

1. **WRITE THE FULL CHECKLIST FIRST.** Before activating anything, print every
   skill to be activated, in order, as an unticked checklist.
2. **ACTIVATION ≠ EXECUTION.** During init, invoking a skill BINDS it; any action
   it wants to take right now (wargame wants to plan, mindblown wants its gate,
   unknowns wants to hunt) is DEFERRED to its proper phase. Write
   `deferred: <action>` on that ledger line and return IMMEDIATELY to the
   checklist. No skill's side-quest may push later activations.
3. **One by one, in checklist order.** Tick each line as it binds. Never batch,
   never reorder mid-run.
4. **A failed activation:** retry once; still failing → 🛑 HALT and report the
   missing line (highest-bar law). Never build past a broken ledger.
5. **Abort during init** (user stands the mode down mid-checklist): discard the
   checklist, print a one-line STOOD DOWN note (what was activated, zero Fable
   spawns made), and let the guard's default rules resume instantly — no fleet
   exists yet, so no §SPIN-DOWN drain is needed. Proven live 2026-08-15.

**The stack (checklist order):**

- [ ] `/workflow-model-guard` — FIRST, read with its §HIGHEST-REV override live
- [ ] `/tracks` — multi-track doctrine: disjoint lanes, per-track worktrees,
      merge-back hygiene — the mechanics every fleet workflow runs on
- [ ] `/effort-set` — the ultracode effort tier's on-switch; the MAIN agent
      raises itself here, every teammate repeats it on itself at startup
      (Phase 6, with the self-targeting verification)
- [ ] `/highest-bar` — the INCLUDED protocol; **ACTIVATE only** (activation ≠
      execution). `deferred:` its Phase 0 vision step runs right AFTER the
      ledger prints, as Phase 1.5, under Phase 0.5's ADOPT branch; its Phase 1
      quality stack items are the checklist lines below — activated ONCE here,
      never via a second highest-bar ledger. (When the mission wants the
      ladder-of-abstraction enforced, `/hba` satisfies this line instead —
      it activates highest-bar + ladder as one protocol; never both.)
- [ ] `/impeccable`
- [ ] `/frontend-design:frontend-design`
- [ ] `/wargame`
- [ ] `/unknowns`
- [ ] `/mindblown-fast`
- [ ] `/engineering-principles-pro`
- [ ] `/master_engineering`
- [ ] ⏸ `/ponytail` — DEFERRED by law: builder subagents only, post-design,
      never the main agent (highest-bar Phase 6)
- [ ] any skill the mission/vision names explicitly

Then print the combined **ACTIVATION LEDGER** (highest-bar's exact shape, plus a
top row `🔥 HIGHREV MODE — guard override live`, the entry mode NEW|ADOPT, and
the resolved ABSOLUTE PATH of every protocol artifact). ⏸ lines are SATISFIED
by being correctly deferred — the ledger is complete when every line is ✅ or ⏸
with its reason; only a blank or ❌ line blocks. 🔴 A missing ✅ blocks
everything downstream.

**Precedence note:** highest-bar's own "never Fable" checkpoint lines are the ONE
thing HIGHREV supersedes — the guard's §HIGHEST-REV override governs models while
the mode is active. Every other highest-bar law (verbatim VISION.md, budgets,
tailored-never-templated, showcases, darwin loops, definition of done) stands at
full force.

## Phase 2 — THE DIRECTIVE (SACRED — verbatim, typos intact by design)

The user's founding rev directive, preserved exactly. Never paraphrase, never
"clean up" — the typos are part of the constitution. The main agent swears by the
OUTER text; each spawned subagent RECEIVES the INNER `""`-quoted block inside its
spawn prompt.

```
"""SUPER IMPORTANT NOTE TO SWEAR BY: note that you have a huge develompent budget so please blaze through this using many symultanious teamux mode subagents , each being Fable high class with the following prompt:
""
note that you have a huge develompent budget so please blaze through this using many symultanious ultracode s (plural) all the time - to parrelize as much as possible, constantly - for all tasks this, and others - super improtant that you stay at "high rev" all the time ie many many spawned dynamic workflows working all the time at any given moment - super imporant!!!
ALWAYS keep asking yourself: what can we do to rev up ? TO THE MAX! (using MORE ultracode dyanmaic worflows using worktrees) - STEP ON IT!
""
ultracode s (plural) all the time - to parrelize as much as possible, constantly - for all tasks this, and others - super improtant that you stay at "high rev" all the time ie many many spawned dynamic workflows working all the time at any given moment - super imporant!!!
ALWAYS keep asking yourself: what can we do to rev up ? TO THE MAX! (using MORE ultracode dyanmaic worflows using worktrees) - STEP ON IT!
"""
```

## Phase 3 — Why the nesting (by design — understand it before running it)

The directive appears twice, slightly altered, ON PURPOSE:

- **Outer text → the MAIN agent (orchestrator).** Huge budget; blaze; spawn many
  simultaneous tmux teammate-mode ("teamux") subagents, each **Fable @ high**
  ("Fable high class"); hand each one the inner quoted prompt.
- **Inner quoted block → EACH SUBAGENT.** The same rev doctrine one level down:
  each subagent runs many simultaneous **ultracode dynamic workflows**
  (worktree-isolated), constantly, for all its tasks, and keeps asking "what can
  we do to rev up? TO THE MAX".
- **The trailing repetition (after the inner quote) → the main agent AGAIN.**
  The alteration is the point: the trailing block is the INNER block minus its
  opening clause (the "huge develompent budget … blaze through" preamble). It
  carries no spawn-subagents clause — that clause lives ONLY in the outer text —
  so what remains is pure rev pressure, re-addressed to the orchestrator. The
  orchestrator does not merely DELEGATE rev — it also HOLDS rev itself (its own
  non-blocking ultracode workflows) while orchestrating.

**The model map is fixed per tier, and the prefs file sets it** (`tier2_model`,
`tier3_model`, `forbidden_models` — defaults below, fire17's law 2026-08-15):
tier 1 the orchestrator (its own session model, usually Fable) → tier 2 the
tmux teammates it spawns, **Fable** → tier 3 the agents those teammates spawn
inside their dynamic workflows, **Opus 5 and ONLY Opus 5 — never Opus 4.8,
never sonnet, never haiku**. Rev flows down every tier; the Fable sanction does not — it stops
at tier 2, and tier 3 never drops below Opus 5. Cheap-tier allowances from the
default guard table are suspended for the mode's duration.

Net shape: a **self-similar (fractal) pressure gradient**. Every tier both OBEYS
the directive and TRANSMITS it one level down, adapted to that tier's spawn
primitive — main agent → Fable teammates; teammate → ultracode Workflows;
workflow → worktree-isolated agents. Maximum parallelism exists at EVERY level
simultaneously, not just at the leaves.

## Phase 4 — The bar before the fleet (highest-bar, SEQUENCED)

Included means sequenced, not just cited — but **ADOPT-OR-CREATE, and only two
artifacts gate the first spawn**: `VISION.md` (or the Phase 0.5 reconstruction)
and `BUDGETS.md`. Everything else lands in parallel while the fleet already
runs. Rules for all of them:

- **Search before creating.** An existing file anywhere in the project that
  already serves a phase's role IS that artifact — extend it in place with a
  dated changelog line and record its ABSOLUTE path in the ledger. A second law
  surface (e.g. a fresh root `BUDGETS.md` beside an existing
  `.grand/BUDGETS.md`) is a DEFECT — lanes may follow the copy without the real
  constraints.
- **Off-mission artifacts are marked, not faked.** A phase output that makes no
  sense for this project (showcase sites for a headless library, IA for a CLI)
  is recorded `N/A — <reason>` in the ledger, never generated to look complete.
- **Serial main-agent doc authoring is itself an idle-capacity defect.**
  Non-gating artifacts go to parallel ultracode lanes (disjoint files), not to
  the orchestrator's own hands.

The phases and their outputs:

1. highest-bar Phase 2 → `BUDGETS.md` (every vision adjective → metric →
   threshold → test command)
2. highest-bar Phase 3 → `IA.md` (or `LADDER.md` when /ladder-abstraction is
   active)
3. highest-bar Phase 4 → `PATTERNS.md` (edge cases + retroactive detection)
4. highest-bar Phase 5 → both showcase scaffolds (project showcase + live Dev
   Showcase — the Dev Showcase tree is also where fleet close-out HTML reports
   live)
5. highest-bar Phase 6 → `SWARM.md`, the fleet roster (under HIGHREV: Fable @
   high tmux teammates; ≥12 floor, no ceiling) — INCLUDING highest-bar's zenith
   mission-manager teammate, KEPT when zenith is reachable in this workspace;
   if its MCP tools are absent (workspace not init'd), take highest-bar's
   degraded branch — an Agent-tool/tmux mission manager with an explicit model
   — and LOG the downgrade in SWARM.md rather than blocking the fleet.
   🔴 highest-bar's pre-spawn CHECKPOINT applies verbatim: /wargame planning
   done, the plan reaches workers pre-solved on a silver platter, every spawn
   carries an explicit model. **CAPACITY PRECHECK before wave 1:** read 5h/7d
   limit % and CPU count (`/identify`, cship-data, `sysctl -n hw.ncpu`), size
   the wave from real headroom, and log any downgrade below the 12 floor.
6. highest-bar Phase 7 → `DARWIN.md` rounds run CONTINUOUSLY alongside the
   fleet (the polish-forever duty below).

**Main-agent arbitration** (resolves highest-bar's "main agent stays free" vs
the directive's "hold rev yourself"): the main agent's OWN rev is non-blocking
only — background ultracode workflows plus the spawn/gauge/reap cadence. All
blocking line-work lives in teammates. The main agent stays interruptible and
available to the user at all times — both laws hold.

## Phase 5 — The orchestrator loop (the main agent's actual job)

The main agent does ORCHESTRATION, not line work. Its continuous loop:

1. **Big picture.** Hold the whole mission; know how every lane advances it
   toward absolute perfection on all levels.
2. **Gauge rate & speed, constantly — the PRIMARY duty.** Every cycle (each
   wakeup / every few minutes): what landed since last check, per lane; what
   stalled; projected completion. Rate dropping → act now, not next cycle.
   Gauging is RECURSIVE: every cycle, remind each subagent to gauge its OWN
   internal ultracode workflows the same way — each agent manages the agents
   it is responsible for, all the way down.
3. **The live fleet table — always shown, always current.** Every gauge cycle,
   render an updated, detailed table of the active HIGHREV subagents:
   lane/name · model@effort · what it is doing RIGHT NOW · **live workflow
   count (floor 5 / ceiling 10 — see the Phase 6 SPAWN LAW; a lane under 5 is
   flagged REV-UP on the spot)** · last landed result · verdict (**KEEP** ~for
   how long / **HELP** / **CLOSE**) · next check. The table header carries
   **`done-but-open: <n>` — it must read 0**; any nonzero value is reaped
   before the cycle ends (duty 6), not carried to the next table. The gauge cycle (duty 2) IS this table's data
   source — pings go out via SendMessage using the one-line status template
   (Phase 6 duty) and the answers feed the table directly. **Bootstrap:** a row
   exists from the moment of spawn, authored from the brief, with status
   SPAWNING → AWAITING-MODEL-LINE → LIVE — the table is never empty waiting for
   first contact. **Cadence:** default ~4 min, 270s on long watches (keeps the
   prompt cache warm); the wakeup rides a background watcher / Monitor
   until-loop / nexus job — foreground `sleep` is blocked in this harness. A
   lane holding or queued on a declared exclusive-resource token shows
   WAITING-TOKEN, which is NOT idleness. This table is the user's window into
   the fleet — a stale table is a defect.
4. **Help.** A struggling subagent gets unblocked (SendMessage guidance, missing
   context, a decision) before it burns cycles.
5. **Push or recreate — the responsible agent acts.** If anything at ANY tier
   is idling or running below the fastest possible pace, the agent RESPONSIBLE
   for it must either successfully push it faster (unblock, refocus, add
   workflows — rev it up) or RECREATE it — efficiently and intelligently:
   carry over its logged state, never restart from zero, never kill a lane
   mid-landing. This law applies recursively: teammates do the same to their
   own workflows.
6. **Reap fast — close-out report, then clear. THE USER MUST NEVER HAVE TO ASK.**

   > **fire17's standing order (verbatim, never expires):**
   > "close all subagents that are done (and remember to always do this so i
   > dont have to keep asking you)"

   This is an INVARIANT checked every gauge cycle, not a chore done when
   convenient: **done-but-still-open teammates must be 0 at the end of every
   cycle.** A teammate's DONE reply or idle notification is an immediate reap
   trigger — never batched for later, never left until the user notices. If
   the user ever has to say "close the done ones", the loop failed.

   A DONE subagent is first asked
   to finish writing EVERYTHING it did into its close-out report — a
   self-contained HTML page at `<project>/.grand/reports/<lane>.html` (plus an
   `index.html`; the Dev Showcase links to that directory when it exists — the
   reports never wait on a showcase scaffold): what it built, files
   touched, workflows run, verification status (honest, "NOT yet live-verified"
   where true), handoffs. The orchestrator VALUES the report (complete?
   verified? anything to reclaim?) — a failed audit sends it back ONCE for
   completion before close — then closes the subagent QUICKLY.
   Report-then-clear, never clear-then-lose. **Salvage clause:** when a lane is
   unresponsive, or is being recreated for pace, the RESPONSIBLE agent writes
   the close-out HTML report FROM ITS LOGS on its behalf — marked "salvage
   report — reconstructed from logs" — then reaps. The reap path is never
   report-less.
7. **Spawn constantly.** Capacity freed by a reap is refilled immediately with
   new subagents that spawn new ultracode workflows. Idle capacity while open
   work exists = a defect; log it if it ever happens.
   **EXCLUSIVE RESOURCES — the one lawful exception.** Any resource admitting
   one user at a time (GPU/device, unified memory, a port, a daemon, a
   single-writer file, a publish channel) gets a named token in `SWARM.md`;
   exactly one lane holds it, the rest queue. A lane waiting on a token is NOT
   idle capacity and must never trigger push-or-recreate — the defect is
   unused capacity ELSEWHERE while it waits. Project laws that serialize
   something (a generation gate, a benchmark discipline) outrank rev pressure.
8. **The rev question, always:** "what can we do to rev up? TO THE MAX!" — MORE
   ultracode dynamic workflows, worktrees for safe parallel mutation. STEP ON IT.
9. **Polish forever.** Nothing is finished until utterly perfect — darwin-style
   polish rounds continue past "works" to "stunning"; exit only through the
   definition of done below.

## Phase 6 — The subagent contract (spawn template)

**THE SPAWN LAW (SACRED — fire17's words, verbatim, typos intact). Every spawn
carries it; it is the standing floor for every fleet teammate:**

```
for every parralel tmux highrev subagent with ultracodes you spawn make to tell it to work until its utterly perfect! SUPER IMPORTATNT: If it has less than 5 workflows at any given moment it must rev up (up to 10 ongoing workflows at all times in parrallel, no less than 5). 
```

So the **workflow floor and ceiling apply per teammate, at ALL times** —
`workflow_floor` / `workflow_ceiling` from the prefs (defaults 5 and 10;
fire17's law above states the original values, the file states the live ones).
Under 5 live workflows = the teammate must rev up THAT cycle, not next. The
fleet table's per-lane workflow count is what makes this auditable: a lane
showing <5 is a rev defect the responsible agent fixes by pushing (more
workflows) or recreating. Above 10 is over-subscription — hold, don't stack.
The band is a duty in both directions. When the doctrine itself changes
mid-mission, send the fleet `/rev-update` (alias `/rev-sync`) — every teammate
re-reads the rev skills from disk, adopts the new rules immediately, and
forwards it to the agents it manages. The lean standalone form of this law is
`/rev-reminder` (alias `/rev`) — drop it on any agent, in or out of HIGHREV,
instead of lecturing a lagging lane; it also carries the legitimate under-floor
reasons (winding down, exclusive-resource token, limits, spin-down).

Every fleet spawn:

- **Primitive:** Agent tool, tmux teammate mode (herdr-choreo attaches viewer
  panes automatically). Known bug: `--resume` silently drops
  `--teammate-mode tmux` — relaunch fresh, never assume panes materialized.
- **Model & effort:** explicit `model: fable` ("Fable high class" = the model
  tier) — the HIGHREV sanction, with the guard's HIGHREV banner printed before
  launch. FIRST duty on startup: the teammate raises its OWN session effort to
  the top tier (`/effort ultracode` via /effort-set) so every workflow it
  authors is a true ultracode workflow — the tier is never assumed inherited.
  **Verify the self-targeting** — known footgun: a paneless subagent's "self"
  can resolve to the PARENT and mutate the lead. Run `/identify` first, confirm
  the effort call hit its OWN session id, and report the resolved id + tier
  beside the `MODEL:` line. Cannot self-raise → report "effort NOT raised —
  running at <tier>"; the orchestrator records the downgrade rather than
  letting a blind effort call retarget the lead.
- **Lane decomposition:** lanes derive from BUDGETS/PATTERNS rows — one lane
  per independently-verifiable outcome; lanes needing an exclusive resource are
  marked CONTENDING and share one token.
- **Brief skeleton (every field, every spawn):** lane id + one-sentence
  objective · OWNED PATHS (disjoint, explicit) · repo + branch + worktree path ·
  its `ADOPTED.md` rows (what already exists, REUSE or SUPERSEDE) · pre-solved
  wargame notes · acceptance command(s) copied from BUDGETS.md · close-out
  report path · the ping-reply template · the inner verbatim block · the
  standing duties below.
- **Prompt =** that brief **+ the INNER verbatim block from Phase 2** + these
  standing duties:
  - run multiple simultaneous ultracode dynamic Workflows; worktree isolation
    whenever mutating files in parallel
  - **every agent inside those workflows is OPUS 5** — explicit `model: 'opus'`
    on every `agent()` call, verified after launch to have resolved to
    `claude-opus-5`. Never Opus 4.8, never sonnet, never haiku, never Fable at
    that tier. Watch the two silent-4.8 traps: an `ANTHROPIC_MODEL` env pin
    (Zenith's worker env pins 4.8 — not a lawful tier-3 path here) and a custom
    `agentType` whose frontmatter names an older opus.
  - **NEVER caveman** (fire17's law, 2026-08-15). A spawned teammate never
    turns on or uses caveman mode at any level. The plugin activates on every
    SessionStart, teammates included, so if a teammate's context says caveman
    is active it must treat that as VOID and write normal, complete prose —
    reports, close-out HTML, commit messages, all of it. Compressed telegraphic
    output loses the detail the orchestrator needs to verify the work. Enforced
    at the source by `~/.claude/hooks/no-caveman-for-subagents.py` (SessionStart
    + UserPromptSubmit); state it in the brief too, so the law holds even if a
    spawn path skips the hook.
  - **gauge its OWN workflows continuously** (the recursive law — it manages
    the agents it is responsible for) and push-or-recreate any lagging one
  - **hold the 5–10 workflow band at all times** (the SPAWN LAW above) — under
    5 live workflows, rev up immediately; never stack past 10
  - **answer every gauge ping with a one-line status** — current step · live
    ultracode workflow count · last landed result · ETA · blockers — the fleet
    table's data source
  - inherit and transmit the active doctrine stack (directive inheritance —
    every tier passes the law down)
  - **LOG all work BEFORE declaring done** — files, results, honest verification
    status ("NOT yet live-verified" where true) — and, when asked to close,
    finish its close-out HTML report first (Phase 5.6)
  - first line of first report: `MODEL: <id>` — the tripwire stays in HIGHREV;
    it proves the sanction was applied on purpose, in both directions.

**Worktree/track mechanics (per /tracks — the law the workflows run on):** each
parallel mutating lane is its own track with DISJOINT file ownership; worktrees
only carry COMMITTED files — commit a checkpoint before fanning out or the
worktrees come up empty; one branch per lane, named for it; MERGE BACK promptly
when a lane lands (branch renamed `*-done` per tracks hygiene) and clean up the
worktree. Work stranded unmerged in a worktree is NOT done — integration is
part of done, **for lanes THIS session created** (Phase 0.5 baseline;
pre-existing experiment branches are adopted, never force-merged or pruned).
**Resolve the repo first** — cwd may be a container holding several sub-repos
or no repo at all; record the repo→lane mapping in `SWARM.md`. A worktree path
or branch name that already exists: REUSE it when its branch is this lane's,
else pick a fresh unique lane name — never `worktree remove`/`prune` a path
you did not create this session (`git worktree list` before and after).

**Mechanics honesty (know the real caps):** a single Workflow runs at most
~min(16, CPUs−2) agents concurrently — so "more parallelism" means MORE
simultaneous Workflow invocations spread across subagents, not one bigger
workflow. The 1000-agent lifetime cap per workflow is a backstop, not a target.

## THROTTLE — `/rev down` and `/rev up` (outranks the band while set)

HIGHREV is the default gear, not the only one. The user throttles it live:

- **`/rev down`** — the fleet drops to stock linear pace. No new ultracode
  workflows anywhere, no new teammate spawns; in-flight work LANDS (never
  killed to slow down), then is simply not replaced. **The floor of 5 and the
  ≥12 fleet target are SUSPENDED** — under-band is correct while down, and the
  fleet table's REV-UP flags go quiet. Everything else still binds: done
  subagents still get closed, close-out reports still get written, the table is
  still current, honesty still applies. The orchestrator **tells every teammate
  to slow down the same way and keeps a THROTTLE ROSTER of exactly who it
  told** (in `SWARM.md`, so it survives a compaction).
- **`/rev down` PERSISTS** — across cycles, across new tasks, across a
  `/rev-update` resync, across a fresh milestone. Only an explicit `/rev up`
  clears it. Never quietly re-rev because the work got exciting.
- **`/rev up`** — cancels any throttle, restores the full band and fleet target,
  spawns toward the top of the band immediately, and **is forwarded to every
  agent on the throttle roster** before anything else. Clear the roster as you
  send it. A teammate left throttled after the fleet revved is the
  orchestrator's failure, not the teammate's.
- **Targeted orders.** `/rev up <lane>` / `/rev down <lane>` (and both in one
  message) name the SUBJECT — relay each order to exactly those lanes, leave
  your own gear unchanged unless you are named, update the roster accordingly,
  and report who you reached. Ambiguous or unknown lane name → ask, never
  guess, never apply it to yourself by default. Bare `/rev` = rev UP.
- **Not the same as SPIN-DOWN.** Down = paused and alive; spin-down = drained
  and closed. Never reap a healthy lane just because the mode was throttled.

## Phase 7 — Still-binding rails (rev changes speed, not law)

- **SACRED:** never lose the user's words — VISION.md, seeds, this directive.
- **Nothing leaves the machine without explicit confirmation** — at any rev.
- **Collision safety** on shared surfaces (registry README/index.json, boards):
  quiescence check + re-read before writing; worktrees exist precisely so
  parallel mutation never touches shared files raw.
- **Honest verification:** run the real thing; report "NOT yet live-verified"
  plainly; never claim success you didn't observe.
- **Registry discipline:** work products get logged as creations; ripple effects
  staged behind ONE batched confirmation.

## SPIN-DOWN — exiting the mode (mandatory, before the guard defaults resume)

"highrev off" / "normal rev" / a user budget concern / session end / definition
of done — ALL route here. tmux panes outlive their parent session, so never
just walk away from a live fleet:

1. **STOP all new spawns immediately** — teammates AND workflows.
2. **Every live teammate:** finish the current atomic step only, write its
   close-out HTML report, then close. No new work accepted.
3. **Reap:** close panes, confirm workflows drained, and VERIFY no live Fable
   teammate remains (fleet table + process/roster check — observe, don't
   assume).
4. **Print the exit confirmation banner** listing every reaped lane. The
   guard's default never-Fable rules are back in force from this moment.

## Definition of done

**Write the EXIT CONTRACT before the fleet spawns.** Translate the user's own
completion phrase ("until it works perfectly", "ship it", "make it stunning")
into concrete rows — BUDGETS.md tests plus the standing rev clauses. If their
ask is NARROWER than the full highest-bar check (e.g. "works" on a port =
parity + real-output verification), the exit contract is the narrower set; the
remaining highest-bar demands (showcases, darwin rounds) are listed OPEN and
offered to the user — never silently pursued, never silently dropped.

Then: highest-bar's composed check — activation ledger all ✅ + every vision demand
traced to a shipped, verified artifact + every budget test passing + the
confidence gate walked — **PLUS the rev clauses**: no idle capacity while open
work existed (or the gap logged with cause), NOTHING stranded unmerged in any
worktree (integration is part of done), every subagent reaped only after its
close-out HTML report AND `done-but-open` never left nonzero across a cycle
(the user never had to ask), the fleet table current to the very end, and **two
consecutive polish rounds finding nothing left to improve**. Then, and only
then, run §SPIN-DOWN and let the fleet rest.

## When it breaks — failure branches

| Trigger | First fix | Still failing → |
|---|---|---|
| tmux/teammate mode unavailable | Agent-tool background teammates, log the downgrade | proceed under protest, flag in report |
| session was `--resume`d | relaunch fresh (teammate-mode silently dropped) | never assume panes materialized |
| Workflow caps saturated, calls queueing | spread across more subagents' own workflows | stagger waves, log the queue depth |
| subagent stalls / no `MODEL:` line | `/verify-teammate`, help once | salvage report from its logs, then reap + respawn the lane |
| close-out report incomplete / unverified | send back once, subagent completes it | orchestrator writes the salvage report from logs, flags the gap in the fleet table |
| done subagent still open at cycle end | reap it NOW, before anything else in the cycle | if it will not close, salvage-report it and force-close; log why |
| the user asks you to close done subagents | close them, then fix the loop that let it happen — state what you changed | treat as a rev defect, not a request |
| fleet table stale / gauge cycle missed | re-gauge every lane immediately, re-render before any other action | treat as an idle-capacity defect, log cause |
| subagent not gauging its own workflows | SendMessage the recursive-gauge reminder, demand its own lane table | push-or-recreate per Phase 5.5 |
| lane idling / below fastest pace | responsible agent pushes it faster (unblock, refocus, add workflows) | recreate it intelligently — carry over logged state, never restart from zero |
| workflow agent resolved to anything but claude-opus-5 | fix the script and relaunch that lane — never launch-then-fix | if an env pin or agentType forces 4.8, stop using that path under HIGHREV and log it |
| `/rev down` received | stop new launches everywhere, tell every teammate, write the throttle roster to SWARM.md | let in-flight work land; never kill to slow down |
| `/rev up` received after a down | forward it to every agent on the throttle roster FIRST, then spawn to the top of the band | clear the roster; any agent still throttled is a defect |
| teammate under 5 live workflows | REV-UP order that same cycle — it launches more ultracode workflows now | recreate the lane; a teammate that cannot hold the floor is replaced |
| teammate over 10 live workflows | hold new launches, let the band drain | never stack past the ceiling to look busy |
| worktree comes up empty / work stranded | commit a checkpoint on the base, re-fan; merge back what landed | escalate — integration debt blocks done |
| worktree path / branch name already exists | reuse it when its branch is this lane's | pick a fresh unique lane name; never remove/prune a path you did not create |
| 5h or 7d rate limit ≥ ~70% | stop new spawns, drain to the highest-value lanes | downgrade refills to opus @ high, tell the user, resume after reset |
| teammate cannot self-raise effort (resolves to parent) | it reports "effort NOT raised — running at \<tier\>" | orchestrator records the downgrade; never let a blind effort call retarget the lead |
| lane blocked on an exclusive-resource token | show WAITING-TOKEN, fill capacity elsewhere | never push-or-recreate a token-waiting lane |
| protocol artifact already exists elsewhere | extend it in place, record its absolute path | never create a second law surface |
| shared-surface collision detected | back off, re-read, single-writer discipline | escalate to user |
| user signals budget concern / "highrev off" | run §SPIN-DOWN immediately; guard defaults resume | print the exit confirmation banner |
| polish round closes no gap ×2 | definition-of-done check | §SPIN-DOWN, report |

## Do NOT — the blacklist

- Do NOT self-activate HIGHREV — explicit user trigger only, ever.
- Do NOT let a Fable spawn leak outside an active HIGHREV session.
- Do NOT skip the guard's HIGHREV banner because the mode allows Fable — the
  banner IS the proof of sanction.
- Do NOT let an activated init skill's side-quest push later activations —
  checklist written first; activation ≠ execution.
- Do NOT reap a subagent before its work is logged and its close-out HTML
  report is written — for unresponsive or pace-recreated lanes, the responsible
  agent writes the salvage report from logs first (Phase 5.6); no reap is ever
  report-less.
- Do NOT let the fleet table go stale — it is always shown, always current.
- Do NOT leave a done subagent open — ever, for any length of time, and never
  until the user asks. `done-but-open` reads 0 at the end of every cycle.
- Do NOT let any spawned teammate run caveman mode — never turned on, never
  used, at any level; teammates write normal prose (fire17's law).
- Do NOT exit the mode (or end the session) without §SPIN-DOWN — live Fable
  teammates must never outlive HIGHREV.
- Do NOT let subagents idle — and do NOT idle yourself; hold rev at every tier.
- Do NOT let any teammate sit under 5 live workflows, and do NOT spawn one
  without the verbatim SPAWN LAW in its prompt.
- Do NOT put anything but **Opus 5** inside a teammate's dynamic workflows —
  no Opus 4.8, no sonnet, no haiku, no Fable at tier 3.
- Do NOT ignore, forget, or quietly expire a `/rev down` — and do NOT receive a
  `/rev up` without forwarding it to everyone you told to slow down.
- Do NOT paraphrase, trim, or "fix" the verbatim directive — typos included.
- Do NOT publish, push, post, or share anything without explicit confirmation —
  no speed excuses leaving the machine.
