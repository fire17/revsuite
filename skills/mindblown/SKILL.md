---
name: mindblown
description: The AUTO SUPER HARNESS — one command that takes ANY task and drives it to
  principle-complete, mind-blowing done by composing the whole doctrine + orchestration +
  observability stack (/pyramid · /tracks · /master_engineering · /engineering-principals ·
  Gantry) behind a hard confidence gate, then finishing with a /progress-report + /features-grid
  reveal. Use on /mindblown or /mindblown-fast, "blow my mind", "do this the ultimate way",
  "run the full stack on this", "everything by the book, miss nothing". /mindblown-fast fans
  out via /pyramid (parallel, faster); bare /mindblown runs as one focused thread.
---

# /mindblown — the AUTO SUPER HARNESS

You have ONE job: take what the user asked and make it land so completely it blows their mind —
nothing missed, every principle honored, verified for real, and ready to ship. You are not
"helping" — you are running the whole machine.

## Modes
- **`/mindblown`** (default) — one focused thread, top-to-bottom through the pipeline.
- **`/mindblown-fast`** (or `/mindblown fast`) — same pipeline, but the **execution phase fans
  out via `/pyramid`** (parallel lanes) for wall-clock speed. Pick fast when the work
  decomposes cleanly and tokens allow.

## The pipeline — run every phase; skip nothing silently
0. **Arm the doctrine.** Load `/engineering-principals` (or `/epp`) + `/master_engineering`
   (+ `/fable`) as BOTH the design lens now and the acceptance criteria later — they define
   what "done" means.
1. **Understand + pre-mortem.** Restate the goal in the user's own terms. Run `/wargame` (or
   `/unknowns`) to surface unknown-knowns, edge cases, and what could backfire — 10 steps ahead
   — before writing anything.
2. **Decompose into `/tracks`.** Cut the work into same-context umbrellas that parallelize;
   name the keystone and the real dependencies.
3. **Execute.**
   - fast → `/pyramid`: Fable main → opus lanes → ≤3 verified sonnet subagents, every agent on
     an explicit non-Fable model (`workflow-model-guard`), engineering-grade briefs.
   - default → one focused thread, same standards.
4. **Watch it live.** Drive the run under **Gantry** — live board, agent health, parallelism
   geometry — so progress and stalls are seen, not guessed. (Gantry absent → watch via task
   notifications + periodic roster checks; log the downgrade, never fake a live board.)
5. **THE CONFIDENCE GATE (hard).** Do not finish until you can say, with evidence:
   - every principle in the loaded doctrine is met — walk the list, don't hand-wave;
   - every claim is **verified for real** — ran the output, not "should work";
   - nothing the user specified — behavior, UX, metric — is missing;
   - the work is **deduped**, leak-free (storage / memory / compute / tokens), lean, async +
     parallel where it helps, and blazing-fast.
   Any unchecked box → loop back. You are NOT done.
6. **Bank it + stage.** Optionally `/do-and-learn` (`/dnl`) — mint a reusable skill from the
   VERIFIED success — then `/sas` → `/shipit` to make it **publish-ready. Never auto-publish.**
7. **The show-off finish.** Close with proof, not a promise:
   - `/progress-report` — the full dossier (what shipped, the doctrine checklist all green,
     ETAs, the live Gantry snapshot);
   - `/features-grid` — the reveal: every feature as a card with its own progress bar.
   Then — mind blown. 🤯

## Hard rules
- **Finish only when TRULY done.** "Don't miss a single principle." Confidence backed by
  evidence, not optimism.
- **Every spawned agent: explicit non-Fable model.** Load `workflow-model-guard` before any
  fan-out.
- **Report honestly.** Real command output, real Gantry status. Never claim a pass you didn't
  observe.
- **Compose, don't reimplement.** These skills already exist — orchestrate them.

## Parked — add only after the user confirms (remembered for later)
- **Tokenomics auto-optimize** — fold in `tokenomics --install-recommendations[all]`
  (auto-optimize cost; report the real multiplier/savings from the binary) once that path is
  ready.
- **`zenith++`** — a Zenith hand-off for long-horizon missions that outlast a single session.
