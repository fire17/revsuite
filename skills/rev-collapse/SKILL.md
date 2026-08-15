---
name: rev-collapse
description: COLLAPSE THE FLEET INTO ONE — fold every running workflow (and every subagent running workflows) into a single unified workflow that does it all together, reusing everything they produced so nothing is wasted, close the old ones, then rev to the MAX on whatever the human says next. With no specific next goal, run autoresearch self-improvement loop cycles that make the work faster and better. The collapsed state PERSISTS until the human says otherwise. Use on /rev-collapse or /collapse, "collapse the workflows", "condense this into one workflow", "fold everything into one and go max on X", or when sprawl has become the bottleneck.
argument-hint: "[optional: what to rev to the max on after the collapse]"
---

# /rev-collapse — many into one, then maximum rev on one thing

## The order (SACRED — fire17's words, verbatim)

```
take all of the workflows (and or subagents with workflows) that you made - turn them into one workflow that does it all together - then close all currently running workflows - then please rev up to the max on just what i will tell you to do next (or doing autoresearch loop cycles of self improvement to make it go even faster and better as much as possible if i dont give you a more specific goal or mission) until i say otherwise - the current work could be condensed into one workflow - make sure to reuse what the current workflows (and or subagents) did so far so nothing is wasted!
```

## 1. HARVEST FIRST — nothing is wasted, ever

Before anything is closed, capture what exists. Closing first and reconstructing
later is the one way this goes wrong.

- Inventory every live workflow and every subagent running workflows: what it
  was doing, what it has already LANDED, what is mid-flight, what it learned
  that is not yet written down.
- Pull the results out: finished artifacts, partial outputs, verified findings,
  dead ends worth not repeating. Ask each subagent for its close-out report; for
  an unresponsive one, write the salvage report from its logs on its behalf.
- Write a **CARRY-FORWARD ledger** — one row per lane: what it produced · where
  that lives · what remains · whether the unified workflow REUSES it or must
  redo it. A row marked "redo" needs a reason; wasted work is the failure this
  step exists to prevent.
- Let anything mid-landing LAND if it is close. Never kill work to tidy the
  fleet.

## 2. COLLAPSE — author the one workflow

Fold the lanes into a single workflow that does it all together:

- Compose rather than concatenate — independent lanes become one `parallel`/
  `pipeline` stage set inside ONE workflow, so the whole thing still runs wide.
- **Seed it with the carry-forward ledger.** Every stage starts from what was
  already produced; the unified run RESUMES the mission, it does not restart it.
- Drop what is finished. Keep what is unfinished. Fold duplicated lanes into
  one stage.
- All standing law still binds: explicit model on every agent (tier-3 agents at
  the prefs' `tier3_model`, never a forbidden model), the guard's verification
  and banner, worktree/disjoint-ownership rules for anything mutating files.

## 3. CLOSE the old fleet

Only now: stop the superseded workflows and reap the subagents that fed them —
each after its close-out report or salvage report exists, per the standing
close-done-subagents order. `done-but-open` ends at 0. Report what was closed
and what its work became inside the unified workflow.

## 4. REV TO THE MAX on the one thing

- **If the human names the next goal** — go to the ceiling on it
  (`workflow_ceiling` from the prefs, `--profile max` if they asked for it),
  everything focused there, nothing else competing.
- **If no goal is named** — run **autoresearch self-improvement loop cycles**:
  measure the current thing (speed, quality, cost), find the biggest lever,
  change it, measure again, keep the wins, discard the rest, repeat. Each cycle
  states what got faster or better and by how much, measured — never asserted.
- **This state PERSISTS** until the human says otherwise. It is not a one-shot
  burst: subsequent turns keep the single-workflow shape and the maximum rev.
  A `/rev down` still outranks it; `/rev up` restores it.

## Report in this shape

```
REV COLLAPSE — <mission>
harvested: <n lanes> → carry-forward ledger at <path>
  <lane> · produced <what> · REUSED as <stage> | redo because <reason>
collapsed into: <the one workflow, its stages>
closed: <workflows stopped, subagents reaped, all with reports>
now maxing on: <the named goal | autoresearch self-improvement cycles>
band: <n> live (ceiling <n>)   persists until: you say otherwise
```

## Do NOT

- Do NOT close anything before its output and lessons are captured — "nothing is
  wasted" is the whole point of the order.
- Do NOT restart work the old lanes already finished; the ledger exists so the
  unified workflow starts from their results.
- Do NOT collapse into something serial — one workflow, still wide.
- Do NOT let the collapse quietly lower the models or skip the guard.
- Do NOT treat the max-rev state as finished after one turn; it holds until the
  human says otherwise.
- Do NOT claim an improvement in an autoresearch cycle you did not measure.
