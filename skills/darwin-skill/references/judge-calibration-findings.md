# Judge-calibration findings — local addendum (fire17 machine, 2026-07-08)

Measured live during the watch-skill optimization saga (session 7db50699; full ledger
in `results.tsv` rows 2026-07-08, journal `do-and-learn/watch-mega-mission`). These are
empirical properties of blind opus judges scoring the 9-dim rubric — account for them
in every run.

## 1. Single-judge scores swing ±1.5 points

The same artifact scored 68.2 and 67.0 by two same-prompt judges minutes apart. A
ratchet on single scores churns on noise (observed: a genuine dedup "regressed" −1.2
and was reverted on what was later shown to be noise). **Use a 2-3 judge panel mean
for every keep/revert decision.**

## 2. Strict-prompt judges structurally withhold 10s

Across 13 same-prompt judges: zero 10s ever granted on dims 1/2/5 even when the reason
column contained no actionable residual ("dense but valid", "solid"). The strict prompt
("be strict, deduct, judges are optimistic") biases *withholding*. Adding one SYMMETRIC
line — "a dimension that fully satisfies its criteria with no concrete residual
deserves its 10 — withholding a deserved 10 is as much a calibration error as
inflating" — freed deserved 10s WITHOUT freeing undeserved ones (a judge still gave
three 9s with it; every granted 10 cited concrete content by name). Measured effect on
the same artifact: +4.4/76. **Declare which prompt a run uses and never compare scores
across prompts; if switching mid-run, score once with the old prompt as a control.**

## 3. 10s are granted when criteria become objectively checkable

Dims where judges DID grant 10s under the strict prompt: resource paths exist on disk
(dim6), dedicated blacklist section present (dim9), N visually-marked checkpoints
(dim4), explicit named failure branches (dim3 — a 10 arrived the round six concrete
branches were added). **The path to a high score is converting judgment into checkable
structure, not prose polish.**

## 4. dim7 (redundancy) is a roaming perception with a floor

Every judge finds a *different* "restated 3×" — fix one, the next names another.
Partly structural: a Do-NOT blacklist necessarily restates rules; a Security section
must stand alone. Under the strict prompt dim7 never exceeded 9 and usually reads 8.
**Do not chase dim7 past one true structural merge; further rounds trade real content
for a point that relocates.**

## 5. Phrase-trims lose; structural merges draw; residual-elimination wins

Three dim7 strategies tested under ratchet: trimming repeated phrases → REGRESSED;
pointer cross-refs → flat; folding a whole duplicate section → kept. A comprehensive
eliminate-every-NAMED-residual round (darwin Phase 2.5) produced the largest single
verified gain (+1.2 strict-protocol, in one round after four rounds of ±0.3).
