---
name: identify
description: Identify the CURRENT Claude Code session and report its complete live state — resolved by pid/tty and read from the cship live snapshot. An agent has no native way to know these facts about itself; use this skill whenever you (the agent) or the user need ANY one of them, each of which identify reports explicitly — (1) session id; (2) session name; (3) the hosting multiplexer — tmux, herdr, or none; (4) the window/tab/pane location (VOLATILE — re-resolve by pid/tty before acting); (5) the current MODEL (id + display name, e.g. claude-opus-4-8[1m] / "Opus 4.8 (1M context)"); (6) the reasoning EFFORT level (low/medium/high/xhigh/max, incl. the "ultracode" label); (7) whether FAST-MODE is on; (8) whether THINKING is on; (9) the CONTEXT-WINDOW fill % — tokens used and remaining of the total window size; (10) whether the session exceeds 200k tokens; (11) the OUTPUT STYLE; (12) the current REPO and cwd; (13) the session COST in USD + lines added/removed; (14) RATE-LIMIT usage — 5-hour and 7-day percent AND the timestamp each resets at; (15) the Claude Code VERSION; (16) the session ROLE — whether this is a MAIN agent or a spawned SUBAGENT (teammate), and for a subagent its label (e.g. @test-opus-agent), team name, parent session id, agent type, and color (recovered from the process launch flags, since the cship snapshot does not carry them); (17) whether a /goal (session-scoped Stop hook) is currently ACTIVE and its condition text (read programmatically from the transcript, the only place Claude Code keeps goal state). Use when the user types /identify, asks "what session am I", "am I in tmux/herdr", "which pane", "am I a subagent or the main agent", "what's my agent name/label", "do I have a goal active / what's my current goal", OR whenever you need to know your own model, effort level, context fill % / tokens remaining, session name, cost so far, rate limits or when they reset, CC version, fast-mode/thinking state, whether a goal is active, or whether you are a main agent or a subagent (and your agent label/team/parent) — or before injecting input into this session. The multiplexer is the durable fact; the pane location is volatile.
allowed-tools: Bash
---

# identify

Report the full live state of the **session this skill is running in**. An agent
can't natively introspect any of this about itself — so if you (or the user) need
**any single one** of the fields below, run identify to get it. Everything it
reports, **in output order**:

**Identity, role, goal & location:**
1. **session id** — the stable id of this session.
2. **name** — the session's human name (e.g. `extend_identify`).
3. **goal** — whether a `/goal` (session-scoped Stop hook) is **currently active**, and
   its condition text. Read programmatically from the transcript (see How it works).
4. **role** — whether this is a **MAIN agent** or a spawned **SUBAGENT** (teammate).
   For a subagent, also its **label** (e.g. `@test-opus-agent`), team name, parent
   session id, agent type, and color. A main agent has none of these.
5. **pid** — the hosting `claude` process id (the nearest `claude` ancestor).
6. **host / multiplexer** — **tmux, herdr, or none**.
7. **location** — the exact window/tab/pane, ⚠️ **VOLATILE** (re-resolve by pid/tty).
   - **herdr:** the FULL address `session:workspace:tab:pane` (`herdr_session` / `herdr_workspace`
     / `herdr_tab` / `herdr_pane`) plus the **stable agent name** `herdr_agent_name` (`"<name>
     [sid8]"`, set by the `claude-pane-autoname` hook) — the durable, session-keyed handle.
   - **tmux:** the volatile `session:window.pane` INDICES plus the **stable ids**
     `%pane_id`/`@window_id`/`$session_id` and the **`@claude_session`** marker (`tmux_*` fields).
   - Prefer the stable handle/marker over the index; to locate ANY session by it, use `/pane-mark
     locate <id|name>`.
8. **also_within** — outer multiplexer when nested (e.g. tmux inside herdr).

**Live session state (from the cship snapshot — authoritative, real-time):**
9. **model** — id + display name (e.g. `claude-opus-4-8[1m]` / "Opus 4.8 (1M context)").
10. **effort** — reasoning effort level (low/medium/high/xhigh/max) + label (e.g. `ultracode`).
11. **fast** — whether fast-mode is on/off.
12. **thinking** — whether extended thinking is on/off.
13. **context** — context-window fill: % used, % remaining, and total window size.
    (also `exceeds_200k_tokens`.)
14. **style** — the active output style.
15. **repo** + **cwd** — the git repo (owner/name) and working dir.
16. **cost** — session cost in USD + total lines added/removed.
17. **limits** — rate-limit usage: 5-hour % and 7-day %, **each with its reset time**.
18. **version** — the Claude Code version.

Each field comes from a different source, chosen for reliability: **1–2, 5–8** from
pid/tty resolution; **4 (role/label)** from the hosting process's launch flags;
**3 (goal)** from the transcript; **9–18** from the cship live snapshot. NOTE: the
transcript records the model per message but has **no effort field**, so the cship
snapshot is the **only** per-session source for effort (and name, cost, context %,
limits); and goal state lives **only** in the transcript (Claude Code persists it to
no queryable file).

## ⛔ ALWAYS run the command — never fabricate

Every `/identify` invocation MUST execute the command below via **Bash, in THIS turn**,
and your answer MUST quote its actual stdout. Session ids and hosts change (a session can
be re-cleared or moved), so do NOT answer from memory or a previous run — a stale id is
worse than useless. If you don't have fresh output in hand, run it now.

## How to run

```bash
python3 ~/.claude/skills/identify/identify.py
```

It prints a JSON line (for programmatic use) followed by a human summary, e.g.:

```
{"session_id":"…","pid":70543,"multiplexer":"tmux","location":"compact-test:0.0","also_within":[],"details":{"session_name":"compact-test","model_id":"claude-opus-4-8[1m]","model_display":"Opus 4.8 (1M context)","effort_level":"xhigh","effort_label":"ultracode","fast_mode":false,"thinking":true,"context_window_size":1000000,"context_used_pct":7,...}}
---
session : d9ccb0c5-…
name    : compact-test
goal    : ACTIVE — "keep refactoring until all tests pass"
role    : main agent
pid     : 70543
host    : tmux
location: compact-test:0.0   ⚠️ VOLATILE
          …
model   : Opus 4.8 (1M context)   [claude-opus-4-8[1m]]
effort  : ultracode  (xhigh)
fast    : off
thinking: on
context : 7% used of 1,000,000 tokens  (93% free)
style   : default
repo    : fire17/Tokenomics
cost    : $1.4986  (+701/-12 lines)
limits  : 5h  1%  · resets 2026-07-02 05:10 (in 4h 54m)
          7d 71%  · resets 2026-07-02 04:00 (in 3h 44m)
version : 2.1.197
```

Rate limits show both the **used %** and **when each window resets** — an absolute
local timestamp plus a relative countdown computed at run time.

For a spawned **subagent** the `role` line reads `subagent   @<name>` with a second
line for `type · team · parent · color`, e.g.:

```
role    : subagent   @test-opus-agent
          type general-purpose · team session-97e9fa03 · parent 97e9fa03-… · color green
```

The live-state fields live under the JSON `details` object (top-level keys —
`session_id`, `pid`, `multiplexer`, `location`, `also_within` — are unchanged, so
existing consumers keep working). If cship has no snapshot for the session, the
`details` block is empty and the summary prints `details : (cship snapshot
unavailable — model/effort/name unknown)` instead of guessing.

## How it works

- **Session id** comes from `$CLAUDE_CODE_SESSION_ID`; the pid is looked up in
  `~/.claude/sessions/<pid>.json`. Fallback: walk our process ancestry to the
  hosting `claude` process and map that pid → session.
- **Multiplexer** is decided by matching that pid (and its tty) against
  `tmux list-panes -a` and against each herdr pane's foreground process. Env vars
  like `$TMUX_PANE` are **not** trusted for identity — they go stale when a
  session is moved between panes.
- If tmux is nested inside a herdr pane, the **immediate** host (tmux) is what you
  drive; herdr is reported under `also_within` as the outer layer.
- **Role (main vs subagent)** is read from the launch flags of the **nearest `claude`
  ancestor** (the process we actually run under — resolved by walking ancestry, *not*
  the env→session pid, which a subagent inherits from its parent). Claude Code spawns
  a **separate-process teammate/subagent** as its own `claude` carrying
  `--agent-name` / `--agent-id` / `--team-name` / `--parent-session-id` /
  `--agent-color` / `--agent-type` (e.g. `@test-opus-agent` in a `claude-swarm` pane);
  a main agent has none of these. The cship snapshot does **not** carry the label, so
  the process args are the only source.
  - **Caveat (honest):** this detects the *separate-process* teammates (the ones with
    their own pane and an `@label`). An in-process **Agent/Task** subagent runs inside
    the main agent's own `claude` process (its Bash calls have the main agent as
    parent, and it inherits the parent's session env), so it has no OS-level signal and
    identify reports it as the **main agent**. Verified against the live process tree.
- **Goal (active `/goal`?)** is read from the **transcript** — a lightweight,
  deterministic single pass (substring-prefiltered, no AI). Claude Code persists goal
  state to **no queryable file** (verified: not in `settings.json`, `~/.claude.json`,
  `~/.claude/sessions/<pid>.json`, `session-env/`, or the cship snapshot), so the
  transcript is the only source. It scans the two structured markers CC writes:
  - **SET** (authoritative): a `type:user, isMeta:true` record whose text **starts with**
    `A session-scoped Stop hook is now active with condition: "<CONDITION>"`. The
    **startswith** check (not a mere substring) is deliberate — it ignores any message
    that only *quotes* the phrase mid-text (this skill's own docs, or a discussion about
    goals), which would otherwise be mistaken for a real goal.
  - **CLEAR**: an explicit `/goal clear` command, a "Goal cleared" stdout, or an
    `away_summary` recap noting the goal auto-cleared.
  A goal is **active** iff the last SET is later than any CLEAR. The transcript path
  comes from the cship snapshot (so it works for **any** chosen session), and
  `goal_status(session_id | transcript_path)` returns `{active, condition, set_line,
  cleared_line, note}`.
  - **Caveat (honest):** SET is reliably marked; `/goal clear` is reliably detected;
    but CC emits **no guaranteed marker when a goal auto-clears because its condition
    was *met*** — so a met-but-not-yet-superseded goal can still read active. This is a
    Claude Code limitation, surfaced rather than guessed.

## What to tell the user

Report the **session id** and the **multiplexer** (tmux / herdr / none) — that is
the stable answer. State the **role** (main agent vs subagent) when relevant, and for
a subagent give its **`@label`** (+ team/parent). If asked about a **goal**, say
whether one is active and quote its condition (and, if relevant, the honest caveat
that a met-but-unsuperseded goal can still read active). Then answer whatever
live-state field the need is about: **name**, **model**, **effort**, fast-mode, thinking,
**context %** / tokens remaining, output style, repo, **cost**, and the **rate
limits** (5h / 7d used % **and when each resets**), CC version. If the ask is about
just one (e.g. "what model am I?", "what's my effort?", "how full is my context?",
"when do my limits reset?", "am I a subagent?"), lead with that field. Also relay the
exact `location`, but ALWAYS include the warning:

> ⚠️ The exact window/tab/pane is **volatile** — multiplexers reindex and a session
> can be moved between panes. Do **not** cache this location. Before injecting input
> or otherwise acting on it, **re-resolve** the current pane inside the detected
> multiplexer by pid/tty (that is what this skill, `effort-set`, and `compact_remote`
> all do).

If `multiplexer` is `none`, there is no supervisor to inject through — say so.

## Getting context window size (future-proof solution)

The identify skill also provides `get_context_window_size(session_id)` — a function to query the authoritative, automatically-maintained context window size for any session.

### Why this is truly future-proof

**cship snapshots (`~/.cship/live/<session_id>.json`) are the authoritative source:**

```json
{
  "model": {"id": "claude-haiku-4-5-20251001"},
  "context_window": {"context_window_size": 200000}
}
```

- **Automatically maintained by Claude Code** — not manual registry updates
- **Accurate for every model** — Claude Code gets this from the Anthropic API
- **Future-proof** — when new Claude models ship, cship automatically has the correct window size
- **Real-time** — reflects the current session's actual model and context window

### Usage

**From Python:**
```python
from identify import get_context_window_size

# Get window size for a session
window = get_context_window_size("f5038291-69d1-46e0-ae44-8d13432eaea4")
# Returns: 200000 (or None if not available)

# Auto-detect from environment
window = get_context_window_size()  # Uses $CLAUDE_CODE_SESSION_ID
```

**Why NOT to use:**
- ❌ Model registry files (require manual updates)
- ❌ Guessing from model name (fragile, breaks with new models)
- ❌ API calls (adds latency, requires credentials)
- ❌ Hardcoded defaults (silent errors with new models)

**Core principle: Query authoritative sources. Never guess.**

**Use cship because:**
- ✅ It's automatically maintained by Claude Code in real-time
- ✅ It's accurate, authoritative, and truly future-proof
- ✅ Zero maintenance — works automatically for all current and future models
- ✅ Always reflects the current session's actual model from Anthropic API
- ✅ Returns None if unavailable (honest), never returns wrong value

**Fallback (if cship unavailable):**
- Query `~/.claude/models.json` (optional registry)
- If both fail, return None/"unknown" (never guess)
