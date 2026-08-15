---
name: verify-teammate
description: >
  Independently VERIFY a spawned teammate/subagent's REAL live state (model, reasoning
  effort, context fill, fast/thinking, cost, rate limits, role) from the LEAD side — by
  reading the authoritative per-session cship snapshot BY SESSION ID, not by trusting the
  agent's own self-report and not by scraping the width-dependent rendered statusline. Use
  when you need to confirm what a teammate actually IS or whether a change (e.g. an effort
  set) truly applied — "did the effort change take effect?", "what model is that agent
  really on?", "verify the subagent, don't trust what it told me", "audit the team's state".
---

# verify-teammate

Confirm a teammate agent's actual state with your own eyes, from the lead. A subagent's
self-report can be **wrong** — e.g. a Haiku teammate once reported "my effort change did NOT
apply" when it actually had, because it trusted its own blind snapshot. Verify from the
authoritative source instead.

## Source of truth: the per-session snapshot, BY SESSION ID

`~/.cship/live/<session_id>.json` is written by each session and carries **every** field in
full: `model`, `effort` (+ top-level `_effort_label`), `context_window`, `fast_mode`,
`thinking`, `cost`, `rate_limits`, `output_style`, `version`, `_captured_at`. It is
**complete and width-independent** — read it by id.

⚠️ **Do NOT parse the rendered statusline** (the `~/dir ❯ 🧠 Model (effort) …` line from
`capture-pane`). What it shows depends on the pane/terminal **width** — narrow panes hide or
truncate fields, so a field being absent there tells you nothing. The snapshot JSON is the
authoritative, render-independent source. (Aside: `cship-mid` only *sets* the statusline
center — it does not read state.)

```bash
verify_state() {  # $1 = session id
  python3 - "$1" <<'PY'
import json,sys,os
sid=sys.argv[1]; p=os.path.expanduser(f'~/.cship/live/{sid}.json')
if not os.path.exists(p): print(f'NO SNAPSHOT for {sid} (session gone / never wrote one)'); raise SystemExit
d=json.load(open(p)); m=d.get('model') or {}; e=d.get('effort') or {}; cw=d.get('context_window') or {}
print('session :', d.get('session_id'))
print('model   :', m.get('display_name'), f"[{m.get('id')}]")
print('effort  :', (e.get('level') if e else None), '/', d.get('_effort_label'))
print('context :', cw.get('context_window_size'), 'window ; exceeds_200k =', d.get('exceeds_200k_tokens'))
print('fast    :', d.get('fast_mode'), '| thinking:', d.get('thinking'), '| style:', d.get('output_style'))
print('cost    :', d.get('cost'))
print('limits  :', d.get('rate_limits'))
print('captured:', d.get('_captured_at'))
PY
}
verify_state 2cc7ae41-5159-4afe-a870-26136fcadddb
```

## Getting the session id (the id is factual; the STATE is what you verify)

Asking a teammate for its **session id** once is fine — the id comes straight from
`identify` reading env, it's not a self-assessed value. What you must NOT take on trust is its
**state** (did effort apply, which model, etc.) — that you read yourself via the snapshot.
Ways to obtain the id without trusting state:

- **From the spawn context** you already have it, or ask the teammate once to run
  `python3 ~/.claude/skills/identify/identify.py` and report only its `session_id`.
- **Lead-side, no contact:** find the teammate's pane and pid —
  `tmux -L claude-swarm-<LEADPID> list-panes -a -F '#{pane_id} #{pane_pid} #{pane_title}'` —
  read its `@label` from the pane (`capture-pane … | grep -oE '@[a-zA-Z0-9_-]+'`, short/
  width-safe) and its launch flags (`--agent-name`, `--team-name`, `--parent-session-id`).
  Then match the freshest `~/.cship/live/*.json` (by `model.id` + `agent_type` +
  `_captured_at`) to disambiguate which snapshot is that agent's.

### Reading a process's argv robustly (prefer ps-free)

`--parent-session-id` / `--agent-name` etc. live on the host `claude` process's **argv**, not
in any env var. Two ways to read it:
1. `ps -ww -p <pid> -o command= | grep -oE -- '--parent-session-id [^ ]+' | cut -d' ' -f2`
2. **ps-free (survives sandboxed teammates where `ps` is BLOCKED):** read argv via
   `sysctl KERN_PROCARGS2` (macOS, `CTL_KERN=1 / KERN_PROCARGS2=49`) with ctypes.
Prefer **not** hand-rolling this — `identify.py`'s `agent_info(pid)` already does exactly this
with the ps-free fallback and returns `{label, team, parent_session_id, agent_type, color}`.
So the one-liner "what is this teammate's parent / label" is: run `identify.py` (for the
current session) or call `agent_info(<host_pid>)`. A MAIN agent has none of these flags —
their presence is what marks a process as a subagent.

## Known traps (learned the hard way)

- **Haiku effort is snapshot-blind.** Haiku 4.5 snapshots carry `effort: null` even at
  baseline, and the Haiku statusline shows no effort label. So for a **Haiku** teammate the
  snapshot cannot confirm effort. The ONLY visible confirmation is the pane's `/effort`
  **result line** — `tmux -L <sock> capture-pane -t <pane> -p | grep -oE 'Set effort level to [a-z]+'`.
  This is the one case where you must read the pane, not the snapshot.
- **nexus effort has a false-success lag.** `/nexus /effort` can report `success` before the
  "Change effort level?" modal is confirmed, so an immediate snapshot may still show the OLD
  effort. Re-read a few seconds later before concluding it failed. See
  `[[nexus-effort-autoconfirm-modal-bug]]`.
- **Snapshot missing entirely** → the session ended (its `claude-swarm-<pid>` server is torn
  down when teammates exit) or never wrote one. Report "unknown", never guess.

## What to report

Lead with the field the user asked about (usually effort or model), state it came from the
**snapshot by id** (authoritative), and flag any trap that applied (Haiku effort read from the
pane; a re-check done for the nexus lag). If a teammate's self-report contradicts the
snapshot, trust the snapshot and say so. Related: `[[subagent-self-config-swarm-tmux]]`,
`[[swarm-watch-skill]]`, and the `/identify` skill.
