---
name: wartable
description: fire17's WARTABLE planning doctrine — before any plan is handed to cheaper worker models (subagents, workflows, Zenith missions, teammates, future sessions), war-game it 10+ steps ahead. Play every step forward across all probable AND improbable outcomes, premortem the failures, red-team the plan itself, sweep the known/unknown quadrants, and forge the results into a PSEUDO-ORACLE (context capsule + decision records + dead ends + symptom-keyed playbooks + risk register + invariants + escalation contract + field log) so the cheap executors find every situation they will hit already pre-solved, on a silver platter. Use whenever planning, designing, or architecting a system that other/cheaper/future models will build; when writing a "Prepared brief for Zenith"; when kicking off any multi-session project or long /goal mission; when delegating substantial work to weaker models; or when the user says "wartable", "wargame this", "war-table planning", "think 10 steps ahead", "anticipate everything", "pre-solve the future", "unknown unknowns", "build the oracle", or "set the stage for the workers". The planning session is the ONE moment of maximum intelligence and maximum context — everything not written down is lost at the handoff.
argument-hint: "[mission, plan, or path to wargame — blank = wartable the current context]"
---

# wartable

**War-game the plan 10+ steps ahead, then forge what you learned into a pseudo-oracle
so cheaper models execute like masters.** Planning is not done when the architecture
is drawn; it is done when the future has been pre-solved and written down for whoever
comes next.

---

## The source principle (verbatim — never rewrite)

fire17, 2026-07-05, ytai kickoff:

> "one of the things you should do is do wartable style planning where you think 10
> steps (or more) ahead, targeting all potential outcomes during the development of
> this system, anticipating everything, all probable and less probable scenerios, and
> including in as part of the plan, mapping all the possible unknown knowns, and
> unknown unkowns, so the future models working on this would have an psuedo oracle -
> already made for them - where they can consolt against what they are dealing with
> and it would have already found good solutions or approaches or any useful guides or
> insights that would both save us alot of time down the road and more importantly -
> making sure the outcome is as state of the art and intelligent as possible."

And the expansion directive, 2026-07-06:

> "add the things about the point that other cheaper models will be used later so this
> is the chance to set the stage and give them as much as possible plausible or could
> happend along the way on a silver platter"

---

## Why this exists — the intelligence-transfer window

Every serious mission has two populations of minds working on it:

- **The planner**: the strongest available model, at the moment of richest context —
  it has just absorbed the vision conversation, investigated the terrain, and holds
  the whole picture at once.
- **The executors**: cheaper worker models (subagents, workflows, Zenith workers,
  tomorrow's fresh sessions), each arriving later with a cold context, no memory of
  *why*, and less judgment to improvise with.

The wartable session sits exactly at the handoff between them, and that handoff is
**asymmetric and one-shot**:

1. **Everything not written down is lost.** The planner's insight does not travel in
   the code or the task list — only in artifacts. An anticipated failure that never
   made it into the oracle simply does not exist for the executor.
2. **The economics run one way.** Strong-model planning is paid **once**; the oracle
   it produces is consulted for free, forever, by every worker. Every question the
   oracle can answer is a question that never becomes an expensive escalation or —
   worse — a cheap wrong guess. This is zero-shot distillation of *judgment* into
   *artifacts*: the tier knob for execution cost only works if intelligence was
   banked up front.
3. **Wrong guesses compound.** A cheap model that hits an unanticipated fork does not
   stop — it guesses, plausibly, and builds on the guess. By the time anyone notices,
   the guess is load-bearing. The oracle's job is to make sure the fork was never
   unanticipated.

So the standing law:

> **THE SILVER PLATTER LAW.** The planning session is the one chance to set the
> stage. Hand the future workers everything that plausibly — or even implausibly —
> could happen along the way, pre-solved, on a silver platter. Not advice
> ("be careful with rate limits") but moves ("on HTTP 403 `quotaExceeded`: do NOT
> retry-loop — quota resets midnight PT; switch to the browser-driver path, playbook
> §7"). If a worker meets a situation at 3am, the measure of the wartable is whether
> that exact situation is already in the oracle with a good answer next to it.

---

## Running a wartable session

Eight phases. The early ones generate raw foresight; the late ones compress it into
the artifact. Do not skip Phase 0 and do not skip Phase 7 — an oracle built on
imagined terrain, or one too bloated to read, are the two ways this fails.

### Phase 0 — GROUND: investigate before planning
Read the disk, probe the APIs, run the commands, verify the constraints. A wartable
over imagined terrain produces a *confident oracle about a world that does not
exist* — strictly worse than no oracle, because workers will trust it.

### Phase 1 — MAP: chart the terrain
Decompose the mission into components, dependencies, data flows, and external
interfaces. Every boundary with a system you don't control (APIs, auth, quotas,
filesystems, other agents, the user's own habits) is a surprise generator — list
them exhaustively; the wargame draws its scenarios from this map.

### Phase 2 — WARGAME: play it forward 10+ moves
For each step of the roadmap, play the game tree forward. Minimum three branches per
step: it **succeeds**, it **fails loudly**, and the dangerous one — it
**half-succeeds and lies** (looks done, isn't). Follow the critical path at least 10
moves deep. For every branch record four things: *likelihood · blast radius ·
detection signal · pre-approved response*. The response written now, calmly, by the
strong model, is worth ten improvised by a cheap one mid-incident.

### Phase 3 — PREMORTEM: write the failure history
Jump forward: "It is six months later. The project failed / was quietly abandoned /
rotted into unmaintainability. Write the history of how." Enumerate every cause the
exercise surfaces; each one becomes a guard, a monitor, or an oracle entry. The
premortem finds what forward-planning is structurally blind to, because it licenses
imagining failure.

### Phase 4 — RED TEAM: attack the plan
Now attack your own plan: hidden coupling, scale cliffs, quota walls, auth expiry,
API deprecation, data loss, permission prompts that stall automation, concurrent
writers colliding, cost leaks (storage, memory, tokens, compute). Then the
meta-attack, which is special to wartable: **read the plan as a cheap model would.**
Every ambiguity a weaker reader could misread is a defect in the plan itself —
rewrite until there is one interpretation. "Handle errors gracefully" is not an
instruction; it is a judgment call smuggled into an adjective.

### Phase 5 — SWEEP: the four quadrants
- **Known knowns** → state them as invariants with verification commands.
- **Known unknowns** → resolve now with a research spike, or plant a tripwire.
- **Unknown knowns** → things already known but never written (in someone's head, in
  an old chat, in a sibling project) — extract them into the oracle now; these are
  the cheapest wins on the table.
- **Unknown unknowns** → cannot be enumerated, so build *detection* instead:
  monitors, anomaly alarms, invariant checks, and the standing **divergence rule**
  every oracle carries: *"the moment reality diverges from what this oracle predicts,
  STOP, log the divergence to the field log, and escalate — do not improvise past a
  broken map."*

### Phase 6 — FORGE: write the oracle
Produce the artifact (spec below). Colocate it with the project (`ORACLE.md`, or an
`oracle/` dir with a table of contents once it outgrows ~500 lines) and reference it
from the project's brief / CLAUDE.md so no worker can miss it.

### Phase 7 — POLISH: compress until every entry earns its place
Fewer, more meaningful words. An oversized oracle is an unread oracle — bloat is not
thoroughness, it is a regression vector. Merge duplicates, cut hedges, sharpen every
entry to its symptom, its move, and its why. Polish > accrete.

---

## The oracle artifact — eight sections

1. **Context capsule** — the mission's intent in one screen: what we are building,
   why, and the *why behind the whys*. Executors inherit intent, not just tasks; a
   worker that understands intent degrades gracefully, one that doesn't degrades
   creatively.
2. **Decision records** (ADR-style) — "chose X over Y and Z because W; consequences;
   revisit if <trigger>." Kills relitigation, and stops workers from "improving" the
   system into an alternative that was already evaluated and rejected.
3. **Dead ends** — the anti-map: approaches tried or evaluated and rejected, each
   with the reason. Cheap models love rediscovering dead ends; make the map show
   where the cliffs are.
4. **Playbooks** — if-you-hit-X-do-Y entries, **keyed by symptom**: the exact error
   text, the observable behavior — what the executor *sees*, not the planner's
   internal vocabulary. Exact paths, exact commands, expected output of the fix.
5. **Risk register** — risk · likelihood · impact · detection signal · pre-approved
   response. The wargame's branch table lands here.
6. **Invariants & verification recipes** — what must always hold, plus the exact
   command that proves it, plus per-milestone "done means" definitions. This is the
   antidote to looks-done-isn't.
7. **Escalation contract** — the precise conditions under which a worker must STOP
   and say "I'm struggling" instead of guessing, and what the escalation must
   include: the symptom, what was tried, which oracle entries were consulted.
   Escalating early is cheap; wrong guesses compound. Silence is the failure mode —
   never let a worker grind quietly against a wall.
8. **Field log** — append-only. Every surprise a worker meets in the wild gets
   logged: symptom → what worked. This is the oracle's sensory organ and the raw
   material for the next re-wargame.

### Write for the weakest reader

Every oracle entry is written for the **weakest model that will ever read it, at its
worst moment** — cold context, 3am, mid-mission. Imperative, self-contained, exact.
No judgment calls hidden in adjectives. The acceptance test: *could Haiku follow this
entry without asking a single question or making a single judgment call?* If not,
rewrite the entry — not the reader.

---

## The oracle is alive

A wartable is not a ceremony performed once at kickoff.

- **Workers append** every field encounter (section 8) — the oracle learns from
  contact with reality.
- **Re-wargame triggers**: a milestone completes · a divergence event fires · the
  field log accumulates entries · an external dependency shifts (API version, quota
  policy, model lineup). On trigger, the strongest available model re-reads reality
  against the oracle and updates it.
- **Staleness is worse than absence** — a wrong oracle is trusted, an absent one at
  least breeds caution. Date every entry; let the re-wargame prune.
- **Verbatim law**: founding vision quotes stay verbatim forever; derived content is
  marked as derived and is fair game for pruning.

---

## When to invoke — and when not

**Invoke** before handing any substantial mission to cheaper executors: spawning
worker subagents or workflows, writing a "Prepared brief for Zenith", kicking off a
multi-session build, arming a long /goal, or graduating a vision doc into a roadmap.

**Skip** for one-shot edits, and for work the strong model will execute itself,
immediately, in this same session — the oracle's entire value is the handoff; no
handoff, no oracle needed. (A thin risk-sweep is still often worth it.)

---

## Speaking to the outside world

"Wartable" is fire17's coinage (war room × wargaming). When talking to anyone else,
map to the industry-standard kin — and know that wartable is the *union* of them
plus the silver-platter handoff doctrine, which none of them carries alone:

| Facet of wartable | Industry name |
|---|---|
| Play the plan forward N moves, branch on outcomes | **Wargaming** / business wargaming |
| All plausible & implausible futures | **Scenario planning** |
| "It already failed — why?" | **Premortem** (Gary Klein) |
| Walk the team through hypothetical incidents | **Tabletop exercise (TTX)** |
| Systematic per-component failure enumeration | **FMEA** |
| Adversarial attack on your own plan | **Red teaming** |
| Known/unknown quadrants | **Rumsfeld matrix** |
| Decision records with rejected alternatives | **ADRs** |
| Pre-solved if-X-then-Y procedures | **Runbooks / playbooks** |
| Enumerated risks with responses | **Risk register** |

---

## Acceptance checklist — the wartable is done when

- [ ] Phase 0 grounding was real (commands run, disk read) — not imagined terrain
- [ ] Every roadmap step wargamed ≥3 branches; critical path ≥10 moves deep
- [ ] Premortem run; every surfaced cause has a guard, monitor, or oracle entry
- [ ] Red team pass done, including the cheap-model-misread ambiguity attack
- [ ] All four quadrants swept; tripwires + divergence rule cover unknown unknowns
- [ ] Oracle has all eight sections; playbooks symptom-keyed; commands exact
- [ ] A sample of entries passes the weakest-reader test
- [ ] Escalation contract is explicit — workers know exactly when to stop and speak
- [ ] Polish pass done: dated entries, no duplicates, nothing that doesn't earn its place
- [ ] Oracle is colocated with the project and referenced from its brief / CLAUDE.md
- [ ] Recheck loop run until scenario coverage saturates — then the **final chaser**
      written, signed, and dated at the oracle's end (see below)

---

## The final chaser — a personal note to whoever comes next

The founding directive, verbatim (fire17, 2026-07-06 — never rewrite):

> "And as a final note: after you did everything and recheck your work again and again
> until you feel like it completes all the possible scenerious many (potentially
> dosens) of cases or possiblites, then add a final personal note based on the current
> case and you intuition as a final chaser to the future models that will recieve all
> of your work"

How to honor it:

1. **First, saturate.** When you believe the wartable is done, recheck it — again and
   again. Each pass, hunt for the scenario you haven't covered yet. Stop only when
   passes stop finding gaps and the coverage genuinely spans the many — potentially
   dozens — of cases and possibilities this mission can produce. Saturation is felt,
   not counted: the signal is a recheck that comes back empty.
2. **Then, and only then, write the chaser.** Everything above this point is process —
   structured, verifiable, impersonal. The chaser is the one deliberately *personal*
   artifact: drop the format and write, in first person, what you — the planner, at
   this moment of maximum context — would whisper to the next model before handing
   over the keys. Not a summary of the oracle (it exists; don't repeat it), but what
   the structure couldn't hold: where you suspect the real danger sleeps despite
   every check passing, which part feels most fragile, what you'd reach for first if
   things get weird, what surprised you while planning, the hunch you couldn't
   justify well enough to make into a formal entry — written *for this specific
   case*, from intuition, not from template.
3. **Place it last.** The chaser is the oracle's coda — the final thing a future model
   reads before starting work, and the closest thing to meeting the mind that planned
   the mission. Sign it and date it.

Why this matters: the eight sections capture everything that survives being
structured. Intuition is the residue — real information that didn't fit the schema.
A checklist transmits your conclusions; the chaser transmits your *judgment*. For a
cheaper model about to inherit the mission, that handful of honest, situated
sentences is often worth as much as the entire register above it.
