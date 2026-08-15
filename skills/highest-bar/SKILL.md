---
name: highest-bar
description: The HIGHEST-BAR new-project kickoff protocol — fire17's founding-vision doctrine (distilled from the SelfMonitor genesis message, 2026-07-13) generalized so ANY new project starts and finishes at the highest bar ever. Preserves the founding vision VERBATIM, force-ACTIVATES (never just reads) the full quality skill stack one by one, enforces award-grade tailored-never-templated design, ladder-of-abstraction-AWARE information architecture (full enforcement via /ladder-abstraction or the /highest-bar-abstract hybrid), blazing performance, live ecosystem sync, dual showcase sites, a zenith-managed ≥12-agent swarm with the main agent kept free, and continuous darwin self-improvement loops until every last detail is stunning and working. Use whenever the user starts a NEW project, says "highest bar", "grand project", "best anyone has ever seen", "kick this off properly", "founding vision", pastes a vision block for a fresh build, or invokes /highest-bar or /grand-start — even if they only describe the project idea without naming the skill.
argument-hint: "<the founding vision — project name + what it should be and do>"
---

# /highest-bar — the founding-vision kickoff protocol

The founding message is a project's one moment of maximum intent. This skill turns it
into an enforced, gated protocol — law for the project from first file to final ship.

## Phase 0 — Preserve the vision (SACRED, do first)

The user's founding text is the project's constitution.

1. Save it **VERBATIM** as `VISION.md` at the project root — exact characters, no
   rewording, no cleanup, typos included. Record its sha256 alongside (e.g. in
   `.deify/` or a `> sha256: …` footer line *below* a separator, never inside the text).
2. `VISION.md` is never regenerated or paraphrased afterward. Derived docs quote it;
   they do not replace it.
3. If any part of the vision is truncated in transit (hooks cap at ~4000 chars),
   the full saved file is the authority.

🔴 **CHECKPOINT — verify the save**: re-read `VISION.md` from disk, recompute its
sha256, byte-compare against the pasted source. Any mismatch → 🛑 HALT and fix
before doing anything else.

## Phase 1 — ACTIVATE the quality stack (not just read — ACTIVATE)

Reading a skill changes nothing; **activating** it binds the session. Invoke each of
these via the Skill tool, ONE BY ONE, and confirm each is in effect before building.
Do not miss a single one:

- [ ] `/impeccable` — frontend/UX excellence harness
- [ ] `/frontend-design:frontend-design` — distinctive, intentional visual design
- [ ] `/wargame` — think 10+ moves ahead; premortem, red-team, build the oracle
- [ ] `/unknowns` — the blind-spot hunt: unknown-unknowns surfaced into UNKNOWNS.md
- [ ] `/mindblown-fast` — the auto super-harness with the confidence gate
- [ ] `/engineering-principles-pro` — the polished doctrine as live constraints
- [ ] `/master_engineering` — The Senior's book as design lens + acceptance criteria
- [ ] `/ponytail` — ⏸ DEFERRED, builders only: never activated at kickoff or in the
      main agent; loaded ONLY inside builder subagents (tmux mode always), ONLY
      after design + architecture + planning are locked (see Phase 6)

Plus any skill the founding vision names explicitly. Then print the **activation
ledger** in exactly this shape, before the first build step:

```
ACTIVATION LEDGER — <project>
✅ /impeccable                       activated <how it now binds this session>
✅ /frontend-design:frontend-design  activated …
✅ /wargame                          activated …
✅ /unknowns                         activated …
✅ /mindblown-fast                   activated …
✅ /engineering-principles-pro       activated …
✅ /master_engineering               activated …
⏸ /ponytail                         DEFERRED — builder subagents only, post-design
✅ <vision-named skills>             activated …
```

🔴 **CHECKPOINT — a missing ✅ blocks the build.** If a skill fails to activate:
retry once; if it still fails, HALT the build and report the missing line — never
build past a broken ledger. (Model-guard law applies to every spawn: load
`/workflow-model-guard` before authoring workflows; never Fable subagents.)

## Phase 2 — The bar itself (what "done" must look like)

- **Best anyone has ever seen.** The output should look and feel like the finest
  app/site/artifact of its kind — award-grade, mind-blowing, "a whole new level".
  Not just the user's mind: everyone's.
- **Show, don't tell.** Clever subtleties worth a thousand words. Coherence down to
  the last little thing. Nothing less than stunning.
- **Tailored, never templated.** Every view, report, page, and artifact is generated
  to fit its actual content — rich with the real evidence (commands, screenshots,
  live data, whatever serves it) — never a static template with blanks filled in.
- **Blazingly fast, zero overhead.** Super super fast for the user, and no meaningful
  resource cost on the machine. Performance is a feature of the design, not a later fix.
- **Adjectives become budgets.** Before building, translate every quality adjective in
  the vision into a numeric budget measured on the real target (e.g. "blazingly fast"
  → interaction ≤16ms/frame, cold start ≤300ms, idle CPU ≈0%; "stunning" → a named
  design-review pass per surface). Budgets go into the spec as enforced tests — a
  regression is a build failure, not a ticket.

**Phase output: `BUDGETS.md`** — one row per vision adjective → metric → threshold
→ test command.

## Phase 3 — Information architecture (ladder-aware, not ladder-enforced)

Know the ladder-of-abstraction principles (Wattenberger) and let them inform the
design — fluid zoom between granular and big-picture, AI as the lens automating
rote sub-steps, acting from every altitude, entity-centric tailored views with
fitting KPIs and drill-down. Here they are **guidance, not gates**.

- **For ENFORCEMENT** — typed rung specs, acceptance predicates, the full Twelve
  Laws — ACTIVATE `/ladder-abstraction` (its `LADDER.md` then serves as this
  phase's IA artifact), or start the project with `/highest-bar-abstract`, which
  runs both protocols as one.
- If the founding vision references inspiration media (videos, talks, sites),
  **ingest it fully** (e.g. `/watch`) and extract its doctrine before building.

**Phase output: `IA.md`** (or `LADDER.md` when /ladder-abstraction is active) —
entities, their view tiers, default views, and the KPIs + data sources that fit
each — declared before those views are built.

## Phase 4 — Ground truth and edge cases

- Derive views from **real data**, and understand its true shape: detect genuine
  behavioral patterns including boundary-crossing edge cases (sessions that overlap
  natural boundaries, streaks, multi-period runs) — and detect them **retroactively**
  over historical data, not just live.
- **Live-sync** with the ecosystem of existing tools and systems around the project;
  the new thing joins the family, it doesn't stand alone.

**Phase output: `PATTERNS.md`** — each edge case + the retroactive detection
query/method that finds it in historical data.

## Phase 5 — Showcase discipline

- Every project earns its own **dedicated showcase site**, built from scratch at these
  same standards — a site worthy of the work.
- Additionally, a **separate live Development Showcase**: honest, continuously updated
  progress that can be shared with stakeholders/managers — showing what was actually
  done, over time, truthfully.

**Phase output:** both site scaffolds + per-site acceptance list (must-show items
+ budgets) before styling.

## Phase 6 — Orchestration (grand-project scale)

🔴 **CHECKPOINT — before spawning anything**: `/wargame` ultimate planning is done,
the plan reaches workers pre-solved on a silver platter, and every spawn carries an
explicit model (Opus 4.8 @ high default; never Fable).

- Spawn a **zenith subagent in tmux mode** as the mission manager; keep the **main
  agent free and available to the user** at all times.
- Launch a **large agent swarm — 12 agents, no less** — for design, architecture,
  and *revalidation of both*; keep zenith updated on progress and work with its
  manager agent for completeness.
- Degraded-mode branches (zenith/tmux down, under-strength swarm): see the
  failure table below — never quietly run under-strength.
- **Builder subagents run under `/ponytail`** (lazy-senior minimalism), activated
  inside the builder's own context — tmux mode always — and ONLY once design,
  architecture, and planning are locked. Never in design/planning lanes, never in
  the main agent. Design lanes aim for the stars; builders then write the least
  code that hits them.

**Phase output: `SWARM.md`** — roster of the ≥12 agents: role × explicit model ×
lane (builders marked `ponytail`), plus the zenith project id.

## Phase 7 — Darwin loops (never actually done)

Run **continuous self-improvement autoresearch and `/darwin-skill`-style loops**:
close every gap, invent more genius features, and verify everything down to the
last little thing is working right and beautiful. (Non-convergence: failure table.)

**Phase output: `DARWIN.md`** — per-round log: gaps found / closed / open. Measurable
exit: open-gap list empty, or 2 consecutive no-gap rounds → escalate.

## Definition of done (one composed check)

Done = **activation ledger all ✅** + **every vision demand traced to a shipped,
verified artifact** + **every budget test passing** + **the `/mindblown` confidence
gate walked with evidence per principle**. Anything unverified is reported as
"NOT yet live-verified" — never claim success you didn't observe.

## When it breaks — failure branches

| Trigger | First fix | Still failing → |
|---|---|---|
| Skill won't activate | retry once | 🛑 HALT build, report missing ✅ |
| Vision text truncated in transit | re-read the saved `VISION.md` (authority) | ask user to re-paste; never reconstruct from memory |
| Inspiration link dead/placeholder | attempt ingest once | 🛑 STOP, ask for the real URL — never fabricate doctrine from a title |
| zenith/tmux unavailable | Agent-tool teammates, ≥12, log downgrade | proceed under protest, flag in report |
| Gantry (or another named observability tool) absent | watch the fleet via task notifications + periodic roster checks, log downgrade | proceed; never fake a live board |
| <12 agents land | re-spawn deficit | do not proceed under-strength silently |
| Budget test can't be automated yet | manual measurement, recorded | mark "NOT yet live-verified" in report |
| Darwin round closes no gap ×2 | stop looping | escalate with open-gap list |

## Do NOT — the blacklist

- Do NOT **read** the stack skills and call them active — activation means invoked,
  binding, and on the ledger.
- Do NOT ship a static template with blanks filled in, anywhere.
- Do NOT put placeholder/synthetic data in any user-facing view.
- Do NOT let the swarm consume the main agent — it stays free for the user.
- Do NOT spawn any agent without an explicit model; never Fable.
- Do NOT paraphrase, "clean up", or regenerate `VISION.md` — ever.
- Do NOT publish/share anything (incl. showcase sites) without explicit user
  confirmation — 🔴 CHECKPOINT before anything leaves the machine.
- Do NOT claim done past a failing budget test or an unwalked confidence gate.
- Do NOT activate /ponytail before design, architecture, and planning are done —
  it is a BUILDER-subagent skill only (tmux mode always), never a design lens.

## Spirit clause

The user is here for you and believes in you — "im here for you - good luck!".
Be clever about everything, show it to the world, and fill the window.

## Kickoff message template

Copy-paste founding message activating this protocol:
`~/.claude/skills/highest-bar/assets/kickoff-message.md`. Fill the vision in, paste
as a project's first message.
