---
name: unknowns
description: Blind-spot hunt + war-table analysis for the current plan, spec, feature, or project — surface and ADDRESS the user's unknown knowns (tacit assumptions they carry without realizing) and unknown unknowns (edge cases, failure modes, and scenarios nobody has thought of), say plainly if anything could be BAD or backfire, think 10+ steps ahead across probable and improbable futures, and pitch cool relevant value-adding features the user didn't ask for. Every finding gets a proposed solution or mitigation, never a bare list. Can persist the result as a pseudo-oracle file (UNKNOWNS.md) so future sessions — even cheaper/weaker models — consult pre-made answers instead of rediscovering problems. Use when the user types /unknowns [topic] or /uu, or asks "what am I not seeing", "what are my blind spots", "edge cases I'm missing", "unknown unknowns", "what could go wrong", "war-table this", or wants a pre-mortem.
argument-hint: "[topic] [save]"
---

# /unknowns — blind-spot hunt & war-table oracle

Surface what the user cannot see about the thing being planned or built, address every
finding, and (in a project context) leave a durable pseudo-oracle behind for future models.

## Scope resolution

- `/unknowns <topic>` → analyze that topic/spec/idea.
- Bare `/unknowns` → analyze the active subject of this session: the plan, spec, diff,
  or project currently being discussed. If genuinely ambiguous, ask one short question.
- `/unknowns save` (or `--save` / `--oracle`) → additionally persist the oracle file (see below).

## The analysis — four quadrants, weighted toward the last two

Ground every finding in THIS specific project/spec. Generic boilerplate ("consider
security", "add tests") is banned — if a finding would fit any project, it doesn't count.

1. **Known knowns → verify.** Assumptions stated as facts in the spec. Spot-check the
   load-bearing ones against reality (the code, the docs, the platform) before building on them.
2. **Known unknowns → answer.** Open questions the user already flagged. Resolve what can
   be resolved by reading/searching/testing now; list the rest with a recommended default.
3. **Unknown knowns → surface.** Tacit assumptions the user carries without realizing:
   platform/environment defaults, "obvious" behaviors that aren't, habits from one ecosystem
   applied to another, constraints they know but forgot to state. Name each one explicitly
   and challenge it.
4. **Unknown unknowns → hunt.** What nobody has thought about: edge cases, failure modes,
   second-order effects, hostile/weird inputs, concurrency and scale effects, what happens
   at step 10 not step 1, how the thing ages, what it collides with. Use the war-table
   method below.

## War-table method (for quadrant 4)

Think 10+ steps ahead, targeting all potential outcomes — probable AND less probable:

- Play out the build: what breaks at each future step of development, not just today.
- Play out real usage: first run, hundredth run, wrong user, wrong machine, wrong decade.
- Pre-mortem: "it's six months later and this failed / caused harm — what happened?"
- Collisions: what existing tools, habits, or systems does this stomp on or get stomped by?
- For each scenario worth keeping: what happens, the early warning signal, and the
  prepared response.

## "Could this be bad?" — mandatory honesty pass

Explicitly answer: is there anything this could be bad for? Harms, footguns, data loss,
security/privacy exposure, irreversibility, maintenance burden, ecosystem annoyance.
If the honest answer is "yes, and it's serious", say so prominently — do not bury it.

## Address everything — no bare lists

Every finding ships with its resolution: a proposed solution, mitigation, design change,
guard, test, or an explicit "accepted risk because X". A risk without a next move is
an incomplete finding. This is the pseudo-oracle property: future readers get answers,
not just warnings.

## Bonus features (the positive mirror)

Close with features NOT asked for that are cool, relevant, and value-creating for this
specific project. Mark them clearly as opt-in suggestions, ranked by value-for-effort.
If nothing genuinely clears the bar, say so instead of padding.

## Output format

A tight report, most severe first:

1. **Critical** — would sink or harm the project; address before building.
2. **Important** — will bite within the project's natural lifetime.
3. **Worth knowing** — accepted risks and monitored scenarios.
4. **Feature ideas** — the opt-in suggestions.

Each item: finding → why it matters here → how to address it. If a category is honestly
empty after real analysis, state that — an empty category found by looking is information;
one filled by padding is noise.

## The oracle file (durable artifact)

When working inside a project (a repo or project directory) and the user said `save`,
asked for it, or the analysis is part of a larger plan/vision that future sessions will
execute: write the report to `UNKNOWNS.md` at the project root (or merge into an existing
one — update stale entries, never duplicate). Header it as a consult-first oracle:
"Future models: check here before solving a problem — it may already be answered."
Keep entries dated. On later `/unknowns` runs in the same project, diff reality against
the oracle: retire what got handled, add what changed. Without a project context or a
save request, the report stays in-chat only.
