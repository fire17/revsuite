---
name: tracks
description: >-
  Run the work as continuous, always-on TRACKS so the user can feel-test and review
  asynchronously while development never idles — a fast SEQUENTIAL quick-win track plus one
  or more PARALLEL bulk tracks, under strict disjoint-file conflict avoidance. Invoke when the
  user asks to work "in tracks", wants parallel + sequential lanes, a rapid feel-test/feedback
  loop, or references this multi-track philosophy. Runs agent teams AND ultracode dynamic workflows
  TOGETHER — agent-team agents for the sequential lane, and (whenever ultracode is enabled) ultracode
  dynamic workflows each as their own parallel bulk track alongside the team, not as an either/or
  fallback; turns every user message into routed action items; recommends a seamless live-reload so
  feedback flows without manual restarts. Continuously re-evaluates parallelism throughout the
  session — pulling queued or sequential items out into new parallel tracks whenever they can run
  independently, to keep the queue minimal and the most work in flight at once.
argument-hint: "describe the work to run in tracks"
---

# Tracks — continuous multi-track development

A working methodology: **development always runs** so the user can **feel-test and review asynchronously** and feed notes back in a rapid, rewarding loop. You split the work into **concurrent tracks** that never idle, and you route the user's every reaction back into those tracks.

**The loop:** a track lands an increment → the user feel-tests it → they send notes/impressions → you turn those into routed action items → the tracks absorb them → repeat until the user says it's good enough. Nothing blocks on the user: while they review, the tracks keep producing the next thing.

## The tracks

- **Track 1 — sequential quick-wins.** Runs one task at a time (main lane or a single named agent). Knock off simple/quick items **one after another** so the user gets a **steady stream of small, visible changes** to feel-test and give fast feedback on.
- **Track 2… — parallel bulk.** Do **many independent things at once**; present the batch **together** for review when it's all ready.
- **Use MORE than two tracks** when the work safely parallelizes further. Each additional track needs its own **disjoint lane** (see conflict rule). Scale track count to the real parallelism available, not a fixed number. **A parallel track can itself be a dynamic workflow, and you can run several workflows at once as separate tracks** — each in a disjoint lane.

The point: while the user reviews Track 1's latest win, Track 2+ are producing the next batch. The loop **never idles** while they review.

## Non-negotiable rules

1. **No conflicts.** Every concurrently-active track/agent gets **disjoint file/package ownership**. Never let two live agents edit the same files. **One editor per package at a time**; serialize edits to shared code. Parallel agents get non-overlapping lanes (e.g. one owns the UI layer, another the core/data, another docs/content). **Default to PARALLEL.** Reserve sequential execution for a genuine LOGICAL dependency (B needs A's output / B is blocked by A) — NOT for mere file contention. If two otherwise-independent pieces of work happen to touch the same files (a hot `model.go`, router, registry), do NOT serialize them by default — give each its own **worktree** (below) and merge back, so they still run in parallel. "They share a file" is a reason to reach for worktrees, not a reason to go sequential.
2. **Rank by simplicity first.** Order the backlog quick/simple → complex/heavy. Do **quick rewarding wins first**, but **bump a heavier item earlier** when logic or priority demands it (a dependency, or it unblocks/accelerates the rest). Keep the heaviest / final-phase work last.
3. **Every user message is a feel-test note.** Convert each note, impression, or description into concrete **action item(s)** — **miss nothing** — and **route each to the most logical track** (respecting any explicit where/when the user specifies). **Confirm the routing** back to the user so they know where it landed. _Routing heuristic:_ an explicit "do this in X / now / later" always wins; otherwise route by lane — a quick change in the sequential lane's domain → Track 1; independent, bulk, or heavy work in a disjoint area → a parallel track; a note that spans lanes → split it into per-lane action items. Also capture "not now" ideas as tracked items for a future phase so nothing is lost.
4. **Keep the user in the loop.** Surface **feel-testable increments** as they land (Track 1), and present **parallel batches together** (Track 2+). Tell the user what to try and where each of their notes went.
5. **Verify, don't trust.** Independently verify each agent's "done" — build, test, and inspect the **real output** (run it, capture it) — before reporting success. Agents sometimes over-claim, skip parts, or go idle without finishing. Re-check the actual files/behavior.
6. **Use ultracode AND agent teams together — never either/or.** The two mechanisms are **complementary and run concurrently**: agent-team named agents carry the sequential / persistent-addressable lanes, and — **whenever ultracode is enabled** — the parallel bulk lanes are **ultracode dynamic workflows**, with **each workflow as its own track** and **several workflows at once** when the parallelism is there. This is the DEFAULT, not a fallback: reach for ultracode's fan-out for bulk/multi-part parallel work by default. A loose batch of independent agents is only the fallback when **ultracode is genuinely unavailable** — and if the work wants bulk parallelism while ultracode is off, **turn it on (or ask to)** via the `effort-set` skill rather than grinding it with the team alone. Every workflow still obeys rule #1 (disjoint lanes / worktrees). **This includes a SINGLE cohesive parallel task — dispatch it as a workflow too (e.g. an `implement → independent verify` pipeline), NOT a bare background agent. Do NOT rationalize a "it's only one task, a workflow is just ceremony" exception: a one-item workflow is still the correct container (scoped, ephemeral, and the verify stage is pure upside — it catches gaps you'd otherwise chase by hand). Reserve bare/persistent named team-agents for a genuinely interactive, sequential lane only — and be aware that persistent named agents can lose context across compaction and try to RE-GRAB already-finished work, which is a real collision source that ephemeral workflows structurally cannot cause.**

7. **Continuously re-parallelize — re-evaluate CONSTANTLY, never stop.** Parallelism is **not** decided once at kickoff; it is **re-decided throughout the entire conversation**. On an ongoing, recurring basis — after **every** landing, every new user message, every status change, every agent report — **rescan the WHOLE set of tracked/queued/assigned work** and ask: _can anything that is currently waiting in a queue, or assigned sequentially to a track, be pulled OUT and run as its own parallel track RIGHT NOW?_ If it has (or can be given) a **disjoint file/lane** and has **no true logical blocker**, **pull it out and parallelize it immediately** — as a fresh agent or a lane in a dynamic workflow. **The explicit goal is the SMALLEST POSSIBLE QUEUE and the MOST work in flight at once.** Treat every queued/sequential item as a *missed parallelization opportunity* until proven otherwise (a genuine dependency, or unavoidable shared-file contention → give it a worktree, don't serialize it). When you spot queued items that could fan out, **move them into an ultracode dynamic workflow (or parallel agents) at once** rather than draining them one-by-one. This re-evaluation is a **standing operation for the life of the session — it never ceases.** Don't wait to be asked; do it every time the state changes.

## Agent teams + dynamic workflows

- **Sequential track:** a named agent (or the main lane) doing one task at a time; hand it the next item when the current lands.
- **Parallel track(s) — default to ultracode workflows RUNNING ALONGSIDE the team.** Whenever **ultracode is enabled**, **always** author **ultracode dynamic workflows** (fan-out / pipeline / verify) for the bulk parallel lanes, and run them **concurrently with** the agent team — **each dynamic workflow is its own track**, and you run **several workflows at once** as separate tracks when the parallelism is there. Agent teams and ultracode are **not either/or**: keep the named team-agents on the sequential/persistent lanes while the workflows churn bulk fan-out in parallel. Spawning a plain **batch of independent agents** is only the fallback when **ultracode is unavailable** (and if bulk parallelism is wanted while ultracode is off, enable it via `effort-set` first). Either way, each parallel unit stays in its **disjoint lane**, keeps the build green, and makes **self-contained** changes so concurrent workers aren't broken mid-edit.
- **Sweep the backlog into workflows — proactively, not just reactively.** Don't only handle new requests one at a time; periodically look at the WHOLE pending backlog and batch the parallelizable items into dynamic workflow(s) to churn through them faster (quality first — never trade correctness for speed). The disjoint-file rule still governs: items living in independent files fan out cleanly as parallel agents; items that all mutate a **hot shared file** (e.g. a central UI model/router/registry) can't be *live*-parallelized on one tree — so give each its own **worktree** and merge back (still parallel). Only fall back to truly sequential when there's a real **logical dependency**; shared-file contention alone is NOT a reason to serialize. (Note: worktrees only carry *committed* files — if the repo has lots of untracked work, commit a checkpoint first so the worktrees aren't empty.)
- **Fan out multi-part tasks — don't grind them sequentially.** When a SINGLE task decomposes into several independent, similar sub-deliverables (e.g. N animations, N variations, N components, N files or items to process), do NOT crawl through them one-by-one in one agent — author a **dynamic workflow** that builds them **in parallel** (roughly one agent per sub-deliverable). Treat "make several of X" as a fan-out by default. **Requirement:** give each sub-deliverable a **disjoint file/function** (e.g. each animation as its own pure function/file) so the parallel agents can't collide; then a shared **integration/wiring step** (hooking them into the UI, registering them in a cycle/registry) runs **sequentially afterward** on the owning track. Running **multiple dynamic workflows concurrently as separate tracks is fine** — as long as each stays in its own disjoint lane.
- **When an agent stalls or is unreliable:** reassign the task to a **fresh dedicated agent**, and **stand down the old one first** (explicitly tell it to stop editing those files) so two editors don't race on the same code.
- Give agents **enough time before re-checking** — polling mid-edit produces false "it's missing" reads and churn. Check once they report, or after a reasonable interval.

## Recommendation: seamless live-reload for async feel-testing

Early on, **set up (or offer to set up) a seamless live-reload / hot-preview** so the user can run the product and have it **auto-update in place** as tracks land changes — letting them test and send feel-test notes **asynchronously**, with **no manual restarts**. Anything that gives a low-friction "always shows the latest" experience qualifies: dev-mode auto-reload (re-exec/hot-swap on rebuild), a watch build, a live-reloading server/preview, etc. Keep it **unobtrusive** (ideally it shouldn't feel like a restart), and consider a small "what changed" surface (version/build id + latest change note) so the user can see what each reload contains.

## Worktrees

Use git **worktrees** when advantageous — to let parallel tracks work on **isolated copies** (so agents whose work would otherwise overlap can run truly in parallel), or to keep **risky/experimental** work off the main tree. Worktrees are a strong conflict-avoidance tool when clean disjoint-file partitioning isn't possible. Weigh the setup cost; use them when they genuinely unlock more safe parallelism.

**Branch hygiene (verbatim user directive):** use branches intelligently if you need to; after merging, verify that everything is ok, and rename the branch to `*-done` so when the user sees it they know it was already merged.

## When invoked — tailor to the work at hand

1. **Scout** the work; build or refresh the backlog; **rank by simplicity**.
2. **Partition** into disjoint lanes; decide the **track count** (2+, as parallelism safely allows).
3. If feasible, stand up the **live-reload / preview** for async feel-testing.
4. **Kick off** the sequential quick-win track (agent team) **and** the parallel bulk track(s) — as **ultracode dynamic workflows when ultracode is enabled**, run alongside the team — so nothing idles and both mechanisms are working at once.
5. As the user sends notes: **convert → route → confirm**; keep every lane fed. **And after every landing / message / status change, re-run rule #7** — rescan all tracked/queued work and pull anything independent out into a new parallel track or workflow. This recurs for the whole session and never stops.
6. **Verify** every landing (build/test/real output) and surface it for feel-testing.
7. Persist this preference/state as needed so it carries across the session/handoffs.

## Anti-patterns to avoid

- Two live agents editing the same file/package (race / clobber).
- Producing parallel output **faster than the sequential lane can integrate/surface it** — balance production with what the user can actually feel-test now.
- Reporting "done" without verifying the real artifact.
- Letting any track go idle while the user waits.
- **Leaving work QUEUED or sequential when it has a disjoint lane and no true blocker** — a queue is an un-taken parallelization opportunity; rescan the whole backlog constantly and pull independent items out into new parallel tracks/workflows (rule #7).
- Dropping, merging, or half-capturing a user note — each one becomes tracked action items.
- **Grinding N independent sub-deliverables sequentially** in one agent when they could **fan out into a parallel workflow** (disjoint files) — see "fan out multi-part tasks."
- **Running agent teams WITHOUT ultracode when it's enabled** — defaulting to a loose batch of agents (or team-only) for bulk parallel work instead of authoring ultracode dynamic workflows that run **alongside** the team, each as its own track. Ultracode and agent teams are complementary; use both (rule #6).

## Rule #8 — TOKENOMICS model discipline (pairs with the /tokenomics skill — load it before any spawn)

Every spawn decision obeys Principle 0 (TOKENOMICS): **NEVER spawn Fable subagents** (Fable = orchestrator only). Workflow `agent()` calls ALWAYS set `opts.model` explicitly — `opus`+`effort:'high'` default, `opus`+`xhigh` for design/judge/hardest stages, `haiku`+`xhigh` only for atomic child-simple logistics with an explicit escalate-on-struggle clause. Prefer `resumeFromRunId` over relaunch (cached agent calls are free); verify journal results are non-null before trusting a resume. Time is bought with parallelism, money with model choice — quality with neither.
