---
name: tokenomics
description: >-
  The TOKENOMICS operating doctrine (Principle 0): every token is a cost of time or money —
  maximum quality at minimum time (parallelism) and minimum money (deliberate model choice for
  every spawned agent). Invoke BEFORE spawning any subagent, dynamic workflow, or agent team;
  when planning parallel work; when choosing models/effort for delegation; when resuming paused
  workflows; or whenever the user references tokenomics doctrine / Side B / the North Star.
  Enforces: NEVER spawn Fable subagents; Opus 4.8 default (effort high), Opus xhigh for
  design/hardest work, Haiku xhigh only for atomic logistics with escalation; resume-over-restart
  cache economics; and the Side-A parallelism+engineering doctrine it pairs with.
argument-hint: "optional: the delegation/spawn decision to check"
---

# /tokenomics — model & token economics doctrine (Side B of the North Star)

Canonical source: `~/Tokenomics/NORTHEN_STAR.MD` (Sides A+B, user's verbatim words) + `~/Tokenomics/docs/design/PRINCIPLES.md` Principle 0. Side A (parallelism + engineering, the "big mission goal") and Side B (this doctrine) are EQUALLY crucial and work together: A minimizes TIME, B minimizes MONEY, quality is never traded by either. Give the user self-feedback on how well you're living Side A and Side B — often, as you evolve through the mission.

## THE LAW (triple-check before every spawn)

1. **NEVER EVER spawn Fable subagents.** Not in workflows, not via the Agent tool, not as teammates. Fable is the one-of-a-kind orchestrator (main session only, and only when the user put it there). If the main session IS Fable, inheritance is a trap — see Mechanics.
2. **Opus 4.8 is the workhorse** — "more than capable". Default every real-work subagent to Opus @ effort **high**.
3. **Opus 4.8 @ effort xhigh** — ONLY for designing, super-difficult, or the most important jobs (architecture, contracts, adversarial verification of critical claims, hardest debugging).
4. **Haiku 4.5 @ effort xhigh** — allowed ONLY for logistical, non-code, non-logic, child-simple processes, and only when the task is decomposed to ATOMIC subtasks: **one line to explain the task + one line to enforce good behavior** (reason, self-check, back assumptions with data/results, gate-check "done vs needs more thought"). Every Haiku prompt MUST carry the escalation clause: *"If you're having a hard time, SAY SO and stop — the task gets deferred to a stronger model. Admitting struggle is success, not failure."*
5. **Never pay twice.** Prefer `resumeFromRunId` over relaunch (cached agent() calls are FREE); inspect `journal.jsonl` result values before trusting a resume (a cached null poisons downstream); don't edit the (prompt, opts) of completed calls unless you intend to repay them.
6. **Never idle paid capacity.** Every wait is a chance to pull forward independent work (Side A rule #7). But never spawn an agent whose output you won't use.
7. **Spend where it compounds, starve where it doesn't.** Architecture/contracts/verification deserve xhigh; ceremony, relays, and file-shuffling deserve Haiku or nothing. Dense outputs, batched tool calls, no re-derivation of established facts.

## Mechanics (exact, per spawn surface)

- **Dynamic Workflow `agent()` calls:** ALWAYS set `opts.model` explicitly — `{model:'opus', effort:'high'}` default; `{model:'opus', effort:'xhigh'}` for design/judge/adversarial-verify stages; `{model:'haiku', effort:'xhigh'}` for mechanical stages. NEVER omit model when the session might be Fable (omission = inherit = possible Fable = violation). Workflow scripts cannot run slash commands — opts are the ONLY lever there.
- **Agent tool / teammates:** set `model:'opus'` (or `'haiku'`) in the spawn call; for full interactive sessions (tmux teammates), additionally direct them to run `/effort-set high` (or `xhigh`) as their FIRST action (nexus `/effort` also works).
- **Zenith runtime workers:** dispatched by the zenith server's backend config, not by your spawn call — verify the configured worker model is NOT Fable before `advance_project`; if it is, fix config or surface to the user before advancing.
- **Model ladder cheat table:** design/architecture/contracts/hardest → opus+xhigh · implementation/validation/review/research → opus+high · atomic logistics (rename, collect, format, relay, count, verify-file-exists) → haiku+xhigh with escalation clause · orchestration/synthesis-of-everything → main session only.

## Side A pairing (the mission doctrine this serves — see NORTHEN_STAR.MD for verbatim)

Max parallelism via tracks + trees of ultracode dynamic workflows; items inside a track are NOT sequential; continuously re-evaluate and re-register work into more parallel lanes; 2 polish passes per track; the 26+1-principle charter verified per track; nothing missed, assumptions validated, temp code deleted, versioning discipline. Quality is NEVER the variable — time (parallelism) and money (model choice) are.

## Self-feedback cadence

At every milestone/status report, include a short **Side A / Side B scorecard**: what parallelized well, what queued too long (A); model/effort choices made, tokens saved by resume/caching/dedup, any near-violations caught (B). Own violations plainly — e.g. "spawned N agents on inherited Fable" is a Side B failure to report, not hide.
