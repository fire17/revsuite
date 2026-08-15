---
name: effort-set
description: Set the current Claude Code session's reasoning effort from the agent side (low/medium/high/xhigh/max/ultracode) — a stand-in for the built-in /effort, which only a human can type. v2 is powered by nexus — it injects /effort into the live session the moment your input is clear (never clobbering typed text), auto-approving the "Change effort level?" dialog. Claude Code itself persists the new default when /effort runs — nexus never writes settings. Use when the user asks to change/raise/lower effort or turn ultracode on/off without typing /effort themselves.
argument-hint: "[low|medium|high|xhigh|max|ultracode]"
allowed-tools: Bash
---

# effort-set (v2, via nexus)

Change reasoning effort **from the agent side** — same levels as the built-in `/effort`:
`low medium high xhigh max ultracode`. It arms a nexus job that injects `/effort <level>`
into the live session **once your input is clear**, auto-confirming the "Change effort
level?" dialog if it appears. **nexus never writes `~/.claude/settings.json`** — it only
interacts with the session; Claude Code itself persists the new default when `/effort` runs.
Non-blocking; runs in nexus's shared background worker. (The command stays `/effort-set`
because `/effort` is the human-only built-in.)

## ⛔ ALWAYS run the command — never fabricate

Every `/effort-set` invocation MUST execute the `python3 ~/Creations/nexus/nexus.py effort …`
command via **Bash, in THIS turn**, and your reply MUST quote its actual output (a real job
id `j-…`). Do NOT claim effort was set/queued without running it. Obey the "agent report
contract" the program prints (relay the real outcome, or the boxed warning).

## Mapping `/effort-set …` → the CLI

| User types | Run |
|---|---|
| `/effort-set xhigh` | `effort xhigh` |
| `/effort-set ultracode` | `effort ultracode` |
| `/effort-set low --session <id>` | `effort low --session <id>` |
| conditional, e.g. "drop to medium when context > 80%" | `effort medium --when-ctx-pct 80` |
| add `--dry-run` (preview) · `--idle` (also wait for idle) | pass through |

```bash
python3 ~/Creations/nexus/nexus.py effort xhigh          # this session
python3 ~/Creations/nexus/nexus.py effort medium --when-ctx-pct 80   # conditional
```

## Notes to relay

- **Waits, never clobbers:** if you have text typed, the change is applied the moment the
  composer is clear — it does not refuse or overwrite (the v1 behavior was to refuse).
- `max` / `ultracode` are session-only levels — the live session gets the exact level;
  whatever Claude Code persists as the default is up to CC (nexus doesn't manage it).
- If the session isn't in a supported multiplexer (tmux/herdr), nexus prints a boxed
  warning and queues nothing — relay it (relaunch Claude inside a supported multiplexer).
- Track/inspect with `nexus status`. v1 (own injection + dialog watcher) is archived in
  `~/Creations/nexus/legacy/effort-set/`.
