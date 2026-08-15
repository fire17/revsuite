---
name: rev-priority
description: SET THE PRIORITY AND REBALANCE THE FLEET — records the user's goals/mission/instructions VERBATIM into a durable priorities ledger (.rev/PRIORITIES.md — rich per-priority state, subgoals, and two append-only timestamped note streams for user and agent), then judges every currently open workflow and subagent against the full active priority set, routes the ones serving no priority through /rev-collapse so nothing is wasted, and spawns multiple new parallel workflows aimed at what actually matters. The big-picture layer above session todo lists, which die with the session. Use on /rev-priority <goals/mission/instructions>, /priority, "this is the priority now", "refocus on X", "what are we even working on".
argument-hint: "<the goal / mission / instructions — or a subcommand: list | show P1 | note P1 … | status P1 …>"
---

# /rev-priority — what matters now, and make the fleet match it

Three moves, always in this order: **record → judge → rebalance.**

## 1. RECORD — the user's words, verbatim, in a durable ledger

```bash
python3 ~/.claude/scripts/rev-priorities.py add "<their exact text>" --label "<short label>"
python3 ~/.claude/scripts/rev-priorities.py list            # what is already set
python3 ~/.claude/scripts/rev-priorities.py show P1
```

The ledger lives at `<git root>/.rev/PRIORITIES.md` (or `./.rev/PRIORITIES.md`).
Each priority carries:

- **VERBATIM block — SACRED.** Their goal/mission/instructions exactly as typed,
  typos included. Never edited, paraphrased, reordered, or deleted.
- **state** — rank, status (`active·paused·achieved·superseded·dropped`),
  serving lanes/workflows, artifacts, measured progress.
- **subgoals** — decomposition, checkable.
- **notes** — two append-only, timestamped streams: `USER:` (what they told you
  about it, verbatim) and `AGENT:` (what you observed, decided, measured). Many
  over time; nothing is ever overwritten.

This is the layer ABOVE the session todo list: todos are this turn's mechanics
and die with the context; priorities persist across sessions, compactions, and
agents. Read the ledger before deciding anything — a new priority never silently
cancels an old one, it joins the set (mark the old one `superseded` explicitly,
with a note saying why).

## 2. JUDGE — every open lane against the whole active set

Inventory what is running (workflows, subagents-with-workflows). For each, state
plainly which priority it serves and how directly:

```
LANE JUDGMENT
<lane/workflow>   serves: P1 (directly) | P2 (partially) | NONE   →  KEEP | REFOCUS | COLLAPSE
```

- **Judge against ALL active priorities**, not just the one just set — earlier
  priorities stay in force unless retired.
- "Interesting" is not "aligned". A lane doing good work that serves no active
  priority is still a lane to collapse.
- Be honest about partial alignment: a lane serving 20% of P1 gets REFOCUS, not
  a generous KEEP.

## 3. REBALANCE — collapse the misaligned, spawn for the aligned

- **Everything marked COLLAPSE goes through `/rev-collapse`** — harvest its
  output and lessons into the carry-forward ledger FIRST, fold what is still
  useful into the unified workflow, then close it. Nothing is wasted; work that
  served no priority still produced knowledge.
- **Then spawn multiple NEW workflows in parallel** aimed at the active
  priorities — decomposed by outcome, disjoint file ownership, up to the band's
  ceiling (`python3 ~/.claude/scripts/rev-prefs.py`), models per the tier map,
  the guard's verification and banner as always.
- Weight the fan-out by rank: the top priority gets the most lanes.
- **Write it back to the ledger** — update each priority's `serving
  lanes/workflows` and append an AGENT note recording what was collapsed, what
  was spawned, and why. The ledger is the record, not this reply.

## Subcommands (pass through to the ledger)

```bash
… rev-priorities.py note P1 --user "<what they said>"     # their words, verbatim
… rev-priorities.py note P1 --agent "<what you observed>"
… rev-priorities.py status P1 achieved --why "<evidence>"
```

Status changes need evidence: `achieved` means observed and verified, never
"probably done". `superseded` names what replaced it.

## Report in this shape

```
REV PRIORITY — <label>  (<id> recorded verbatim)
active set: P1 <label> · P2 <label> (paused) · …
lane judgment: <n> keep · <n> refocus · <n> collapse
collapsed: <lanes> → carried forward as <what>
spawned: <n> parallel workflows → P1 ×<n>, P2 ×<n>   (band <n>/<ceiling>)
ledger: <path> updated
```

## Do NOT

- Do NOT edit, tidy, or paraphrase a VERBATIM block — ever.
- Do NOT let a new priority silently cancel an old one; retire it explicitly.
- Do NOT close a misaligned lane without `/rev-collapse`'s harvest step.
- Do NOT mark `achieved` without observed evidence.
- Do NOT rebalance and forget the ledger — an unrecorded decision is lost by the
  next session, which is the exact failure this file exists to prevent.
