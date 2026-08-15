---
name: cship-data
description: Read ANY Claude Code session's live state — model, reasoning effort, context-window fill %, cost, rate limits, fast/thinking, version, cwd — from its authoritative per-session cship snapshot (`~/.cship/live/<id>.json`), resolved BY SESSION ID (O(1) direct read) or BY NAME (freshest match wins). Blazingly fast (~25ms), width-independent, and does NOT trust any agent's self-report. Use when the user types /cship-data, asks "what model/effort/context/cost is session X", "verify a teammate's real state", "get session info by id or name", or wants to script session state into a pipeline.
argument-hint: "<name_or_sessionid> [--json | --field <dotted.path> | --list]"
allowed-tools: Bash
---

# cship-data

Thin front-end over the `cship-data` CLI. Every session writes its full live state
to `~/.cship/live/<session_id>.json`; this reads it **by id or by name** and prints
a summary, raw JSON, or one field. It's the authoritative, terminal-width-independent
source of truth — never scrape the rendered statusline, never trust an agent's
self-report.

Engine: `python3 ~/.claude/skills/cship-data/cship_data.py`
On PATH: `cship-data` (launcher in `~/.local/bin`)

## ⛔ ALWAYS run the CLI — never fabricate
Every `/cship-data` invocation MUST run the command via **Bash this turn** and quote its
real output. Session state changes constantly; do not answer from memory.

## Mapping `/cship-data …` → the CLI
| User types | Run |
|---|---|
| `/cship-data a500d95c-…` (full id) | `cship-data a500d95c-…` — O(1) direct file read |
| `/cship-data a500d95c` (short id) | `cship-data a500d95c` — id-prefix match |
| `/cship-data extend_identify` (name) | `cship-data extend_identify` — name match, freshest wins |
| raw JSON (for piping) | `cship-data <tok> --json` |
| one field (scripting) | `cship-data <tok> --field model.id` |
| list every session | `cship-data --list` |

```bash
cship-data a500d95c                         # summary
cship-data a500d95c --field effort.level    # single dotted field
cship-data "my session name" --json         # full snapshot JSON
cship-data --list                           # all sessions, freshest first
```

## Resolution order (blazingly fast)
1. **Exact `<id>.json` exists** → direct read, no globbing. Fastest path — use the full id when you have it.
2. Otherwise scan once and rank: **id-prefix** > **exact name** > **substring name**; among ties the **freshest** (`_captured_at`) wins.

## Useful `--field` paths
`session_id` · `session_name` · `model.id` · `model.display_name` · `effort.level` ·
`_effort_label` · `context_window.used_percentage` · `context_window.context_window_size` ·
`exceeds_200k_tokens` · `fast_mode` · `thinking.enabled` · `output_style.name` ·
`cost.total_cost_usd` · `rate_limits.five_hour.used_percentage` ·
`rate_limits.seven_day.used_percentage` · `version` · `cwd` · `_captured_at`

## Exit codes (for scripting)
`0` ok · `1` not found (session gone / never wrote a snapshot / name unknown) · `2` field missing.

## Traps to relay
- **Haiku effort is snapshot-blind** — Haiku snapshots carry `effort: null` even when set;
  confirm Haiku effort from the pane's `/effort` result line, not this snapshot.
- **Missing snapshot** → the session ended or never wrote one. Report "unknown", don't guess.
- Getting the **id** for a running teammate: have it run `python3 ~/.claude/skills/identify/identify.py`
  and report only its `session_id` (that's factual, unlike self-reported *state*).

Related: `/identify` (this session), `/verify-teammate` (lead-side pane→snapshot matching), `/cship` (only *sets* the statusline center — does not read state).
