---
name: workflow-model-guard
description: MANDATORY pre-flight + post-author guard for ANY Workflow/agent spawning — forbids Fable-model subagents; requires explicit model on every agent() call, a model-verification pass, and a big-banner compliance announcement (models + effort levels) BEFORE launch. Load this BEFORE authoring or opening any workflow. Knows the ONE sanctioned exception — explicit HIGHEST-REV / HIGHREV activation (via /highest-rev) switches to the HIGHREV override ruleset with its fixed model-per-tier map: tier-2 tmux teammates are Fable, tier-3 agents inside their dynamic workflows are Opus 5 ONLY (never 4.8, sonnet, or haiku); explicitness, verification, and banner still mandatory.
---

# workflow-model-guard — NEVER spawn Fable subagents

**Load and follow this skill BEFORE authoring, opening, resuming, or launching ANY
Workflow script — and apply the same rule to Agent-tool spawns.** (User directive
2026-07-03; standing Tokenomics doctrine.)

## The rule

Subagents must be **Opus 4.8 or below** — NEVER model Fable.

| Tier | Use for |
|---|---|
| `opus` @ high (default) | workhorse: build, validate, review |
| `opus` @ xhigh | design-critical / hardest verify-judge lanes |
| `sonnet` | classic (non-tmux) helper subagents under an opus parent — ≤3 per opus, context only from the opus, opus verifies everything (see `/pyramid`) |
| `haiku` @ xhigh | atomic logistics, cheap mechanical stages |
| **Fable — FORBIDDEN** | never, in any spawn path |

**⚠️ WATCH FOR: HIGHEST-REV / HIGHREV.** If HIGHREV mode has been activated, the
table above is superseded — different rules apply (see the override section
below). Absent that explicit activation, the table is absolute.

## HIGHEST-REV override — the one sanctioned exception

**Trigger (watch for it):** HIGHREV is ACTIVE in a session ONLY when the user
explicitly invoked `/highest-rev` (alias `/highrev`) or explicitly wrote
"HIGHEST-REV" / "HIGHREV" as an activation. It NEVER self-activates, is never
inferred from task size, ambition, or urgency. **A skill-description match is
NOT activation:** before the first Fable spawn, QUOTE the user's literal
activation turn (it must contain one of the four explicit forms). Fuzzy asks —
"blaze through this", "step on it", "rev up" — load the `/highest-rev` doctrine
for reading at most; they never flip this override. The mode ends at
"highrev off" / "normal rev" / a user budget concern / session end — exit runs
/highest-rev's SPIN-DOWN (drain + reap the fleet) BEFORE the defaults resume.
When not active, everything in this section is dormant and the default rules
above are law, unchanged.

**While HIGHREV is active, these rules replace the tier table:**

1. **Fable subagents ALLOWED and intended — at ONE tier only.** HIGHREV has a
   fixed model-per-tier map, and the USER'S PREFS FILE sets it — resolve it
   before authoring, never assume the table below is current:
   ```bash
   python3 ~/.claude/scripts/rev-prefs.py     # tier2_model / tier3_model / forbidden_models
   ```
   Defaults (what the file says today):

   | tier | who | model — MANDATORY |
   |---|---|---|
   | 1 | main orchestrator | the session's own model (usually Fable) |
   | 2 | tmux teammates it spawns | **Fable**, explicit `model: 'fable'` |
   | 3 | agents those teammates spawn inside their dynamic workflows | **Opus 5** — `model: 'opus'`, verified to resolve to `claude-opus-5` |

   Tier 3 is **Opus 5 and nothing else: never Opus 4.8, never sonnet, never
   haiku** (fire17's law, 2026-08-15). The cheap-tier allowances in the default
   table are SUSPENDED while HIGHREV is active — the budget is granted, so the
   floor rises with the ceiling. Fable never appears at tier 3.

   Two traps that silently produce a 4.8: an `ANTHROPIC_MODEL=claude-opus-4-8`
   env pin (the Zenith worker env carries exactly that — so Zenith workers are
   NOT a lawful tier-3 path under HIGHREV), and a custom `agentType` whose
   definition frontmatter pins an older opus. Check both before launching.
2. **Explicitness still MANDATORY.** Every spawn still declares its model —
   write `model: 'fable'` on purpose. Inheriting-by-omission is STILL a
   violation: intent must be visible in every spawn, HIGHREV or not.
3. **Verification changes shape, not existence.** The naked-spawn grep must
   still return empty. `grep -ni "fable"` is now EXPECTED to hit — instead
   confirm every fable hit is an intended, explicitly-written HIGHREV lane
   (a model param you wrote, never an accident of inheritance). Add the
   tier-3 checks:
   ```bash
   grep -n "model: *'" <script> | grep -viE "opus|fable"   # → EMPTY (no sonnet/haiku at tier 3)
   grep -ni "fable" <script>                               # → only tier-2 teammate spawns, never inside agent()
   ```
   Then confirm empirically after launch: every workflow agent's reported model
   reads `claude-opus-5` (the run's progress/journal carries it). An `opus`
   alias that resolved to 4.8 is a violation to fix, not a rounding error.
4. **Banner changes.** Announce with the HIGHREV banner below — every lane with
   model + effort, Fable lanes marked. The banner is how any reader knows a
   Fable spawn was a sanctioned exception, not a leak.
5. **Everything else still binds.** SACRED verbatim rule, nothing leaves the
   machine without confirmation, collision safety, honest verification, and the
   `MODEL:` first-report-line tripwire on workers — which now proves the
   sanction was applied on purpose, in both directions. HIGHREV changes the
   model economy, not the safety rails.

HIGHREV banner (replaces the standard banner while the mode is active):

```
╔══════════════════════════════════════════════════════════════╗
║  🔥 HIGHREV MODE ACTIVE — FABLE LANES SANCTIONED              ║
║  Activated explicitly by the user (/highest-rev).            ║
║  Verified by grep: every fable hit is an intended lane.      ║
║  Tier 2 teammates → fable   ·   Tier 3 workflow agents →     ║
║  OPUS 5 ONLY (no 4.8 / sonnet / haiku)                       ║
║  <lane/label> → fable @ high   (HIGHREV tier-2 lane)          ║
║  <lane/label> → opus  @ high   (claude-opus-5, verified)      ║
╚══════════════════════════════════════════════════════════════╝
```

Full mode doctrine (init checklist, the verbatim directive, orchestrator loop,
subagent contract): `/highest-rev` (`~/.claude/skills/highest-rev/SKILL.md`).

## Why omission is the trap

The **main session may itself run Fable** (`/model fable`). Both spawn paths
**inherit the main-loop model when no model is given**:
- Workflow scripts: `agent(prompt, opts)` with no `opts.model` → inherits → **Fable**.
- Agent tool: no `model` param → inherits → **Fable**.

So an *implicit* model is a violation even if it "usually" resolved to Opus before.

## Procedure (all steps MANDATORY)

**1. While authoring** — every single `agent()` call in the script (and every
Agent-tool spawn) sets an explicit `model: 'opus'` or `model: 'haiku'`. Set
`effort` deliberately (`'low'|'medium'|'high'|'xhigh'`); if omitted it inherits the
session effort — note that in the banner.
**HIGHREV active?** explicit `model: 'fable'` is the sanctioned workhorse there —
explicitness is unchanged (§HIGHEST-REV override, rule 2).

**2. VERIFY after creating the workflow (before launch)** — mechanically check,
don't trust memory of what you wrote:
```bash
# every agent( must carry an explicit non-fable model; any hit here = violation
grep -n "agent(" <script> | grep -v "model"        # → must be EMPTY (naked spawns)
grep -ni "fable" <script>                          # → must be EMPTY
```
For `workflow()` sub-calls, verify the child script too. For `agentType` custom
agents, confirm the agent definition's model frontmatter is not Fable.
If ANY check fails → **fix the script first; never launch-then-fix.**
**HIGHREV active?** The fable grep is expected to hit — apply the override's
verification shape instead (§HIGHEST-REV override, rule 3).

**3. ANNOUNCE with a big banner** — after verification and before/at launch, print:

```
╔══════════════════════════════════════════════════════════════╗
║  ✅ WORKFLOW MODEL GUARD — ALL SUBAGENTS OPUS OR BELOW        ║
║  No Fable subagents. Verified by grep, not assumption.       ║
║  <lane/label> → opus @ high                                   ║
║  <lane/label> → opus @ xhigh                                  ║
║  <lane/label> → haiku @ xhigh                                 ║
╚══════════════════════════════════════════════════════════════╝
```
List every lane/stage with its model **and effort level** (say "effort: inherited
(<session effort>)" when not explicitly set).

**4. Zenith runtime workers** — pinned since 2026-07-07: `~/Creations/.mcp.json`
zenith env carries `ANTHROPIC_MODEL=claude-opus-4-8` (re-verified vs disk
2026-08-15). But env is read at MCP-server LAUNCH only — sessions started before
the pin (or after a pin edit, before a fresh session) run unpinned and inherit
the host env's model. So still set an explicit allowed model on every Zenith
spawn and check every worker's first report line is `MODEL: <id>`; never assume
the pin protects you.

**4b. The `MODEL:` tripwire is SELF-REPORTED — verify it externally.** Observed
live 2026-08-15: a teammate launched with `--model opus` (no `ANTHROPIC_MODEL`
in its env) reported `MODEL: claude-fable-5` in its own status line. The report
was wrong, not the spawn. So a worker's model line is a prompt for
investigation, never proof in either direction — confirm against the launch
flags (`ps -eo args | grep -- '--agent-name <name>'`), the process env, or
`/cship-data` / `/verify-teammate` before believing a compliance claim OR
acting on an apparent violation.

**5. Resumes count too** — `resumeFromRunId` re-runs live agents under the CURRENT
session model for any call lacking an explicit model. Re-verify (step 2) before
every resume, not just first launch.
