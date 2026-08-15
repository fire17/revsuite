---
name: progress-report
description: "Extended /report: the full dossier PLUS enforced progress bars with ETAs and the complete section battery, where EVERY section renders as a numbered table — What I have JUST done · What I have done OVERALL · What is next · How can I improve parallelism or tokenomic efficiencies · How could I have done things better · What I want to do before other things · UP NEXT (future work/phases) · a dedicated project-specific section · the DEBT LEDGER (staged-unshipped work, blocked-on-user decisions, unverified claims, aging backlog — each with what unblocks it) · Immediate or important things to note · What I will do now. Progress bars are mandatory on every work row, INCLUDING completed ones (full bar + ✅). Every report is ALWAYS timestamped at the top with a fresh command-sourced wall-clock time (enforced), and TIME/COST-AWARE: real session duration, $ cost, and context-window % pulled live from the cship snapshot, never guessed. Use when the user types /progress-report, asks 'where are we / full progress report / status with ETAs', wants to 'see where we are visually', asks for 'rich ETAs and progress bars', wants to be 'time and debt aware', or mid-mission checkpoint reporting is wanted."
argument-hint: "[focus or scope notes]"
---

# /progress-report — the full progress dossier

Everything in `/report` (`~/.claude/skills/report/SKILL.md` — same evidence and style
rules, same dossier spine), PLUS the rules and sections below.

## Three hard formatting laws

1. **Every report is TIMESTAMPED at the top (ENFORCED — no exceptions).** The FIRST
   line of the report MUST be a real wall-clock timestamp obtained FRESH this turn via
   `date '+%Y-%m-%d %H:%M:%S %Z'` (run it — never invent, reuse, or infer the time).
   Format: `**📊 Progress report — <YYYY-MM-DD HH:MM:SS TZ>**`. A report without a
   fresh, command-sourced timestamp line is invalid — regenerate it. (The timestamp
   makes a mid-mission checkpoint diffable against the next one and honest about when
   its ETAs were computed.)
2. **Every section is a TABLE with a numbered `#` column.** No prose sections, no
   bare bullet lists — every item is a numbered row. (Short lead-in sentence above a
   table is fine; the content lives in rows.)
3. **Progress bars are ENFORCED on every row that describes work — past, present, or
   future — including DONE work.** Done = `██████████ 100% ✅`. Not started =
   `▁▁▁▁▁▁▁▁▁▁ 0%`. In flight = partial bar + honest % + ETA with its basis stated
   ("unknown — blocked on X" is a valid ETA; an invented one is not). Idea/proposal
   rows show their adoption bar (usually 0% until acted on).

## Overview block (before the sections)

One bar per active workstream/phase, then ONE budget line:

```
workstream A  ██████████▁▁▁▁▁  67% · ETA ~25m (basis: 2/3 stages, last took 12m)
workstream B  ███▁▁▁▁▁▁▁▁▁▁▁▁  20% · ETA unknown — blocked on <X> ⚠️
workstream C  ███████████████ 100% ✅ · closed <time>
─────────────────────────────────────────────────────
session: 1h40m · $36.87 · ctx ██▁▁▁▁▁▁▁▁ 26% of 1M · burn ~$22/h
```

**The budget line is command-sourced like the timestamp (4th hard law):** read
`~/.cship/live/<session-id>.json` (`cost.total_cost_usd`, `cost.total_duration_ms`,
`context_window.used_percentage`) — or `/checkwindow`+`/identify` where cship is
absent. Never estimate these numbers; time-awareness built on guesses manages nothing.

## The section battery (render ALL, in this order, each as a numbered table)

1. **✅ What I have JUST done** — `# | Done item | Progress | Evidence`
   (bars all `██████████ 100% ✅` — done still gets its bar).
2. **📦 What I have done OVERALL** — `# | Work item | Progress | Outcome/Evidence`
   (cumulative session/mission ledger; completed rows keep full bars).
3. **➡️ What is next** — `# | Next step | Progress | ETA (basis)`
   (the immediate queue, top row = the singular focus).
4. **⚡ How can I improve parallelism or tokenomic efficiencies** —
   `# | Opportunity | Adoption | Expected gain` (what could fan out, which
   model/effort tier fits each lane, what's serially blocked and why, cache-friendly
   pacing — the /tokenomics doctrine lens; Adoption is a bar, usually 0%).
5. **🪞 How could I have done things better** — `# | What happened | Better path |
   Cost of the miss` (honest retrospective on THIS session's choices).
6. **🥇 What I want to do before other things** — `# | Priority | Progress | Why it
   outranks`.
7. **🔮 UP NEXT** — `# | Future work/phase | Progress | Horizon` (roadmap view
   beyond the current arc).
8. **🎯 <Project-specific section>** — `# | Health surface | Status/Progress |
   Evidence`. Generic here, SPECIFIC when rendered: name it after the project's own
   health surface and fill it with real metrics (e.g. "Registry health — 38/38/38 ✅"
   in ~/Creations; build/test status in a code repo; milestone state under Zenith).
9. **💳 Debt ledger** — `# | Debt item | Kind | Age | Progress | What unblocks it`.
   Everything owed but not yet delivered, so nothing rots silently: staged-but-unshipped
   work (prepared waves awaiting the user's word), blocked-on-user decisions, unverified
   claims ("NOT yet live-verified" items), deferred follow-ups/backlog, and standing
   drafts (prepared-never-posted media). `Kind` ∈ staged · decision · unverified ·
   backlog · draft. `Age` is since the debt was incurred (be honest — old debt is the
   point of the section). The unblocks column names the exact word, action, or event
   that clears the row. A report with an empty debt ledger on a real mission is almost
   certainly lying to itself — hunt before declaring zero.
10. **📌 Immediate or important things to note** — `# | Note | Severity | Action
    needed?` (risks, waiting-on-input, expiring context, surprises).
11. **▶️ What I will do now** — `# | Action | Progress | Starting when` (the moment
    the report ends — then actually do it; its bar starts moving immediately).
