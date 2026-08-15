#!/usr/bin/env python3
"""cship-data — read a Claude Code session's live cship snapshot, fast.

A session continuously writes its full state to ~/.cship/live/<session_id>.json.
This resolves a session by ID (O(1) direct read) or by NAME (glob + match,
freshest wins) and prints a summary, raw JSON, or a single dotted field.

Usage:
  cship-data <name_or_id>            # human summary
  cship-data <name_or_id> --json     # raw snapshot JSON
  cship-data <name_or_id> --field model.id   # one dotted field (scripting)
  cship-data --list                  # list all sessions (id, name, age)

Exit codes: 0 ok, 1 not found / no arg, 2 field missing.
"""
import json
import os
import sys
import glob
import time

LIVE = os.path.expanduser("~/.cship/live")


def _load(path):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return None


def _is_uuid_like(s):
    # session ids are 8-4-4-4-12 hex; accept full id or a >=8 char hex prefix
    core = s.replace("-", "")
    return len(core) >= 8 and all(c in "0123456789abcdefABCDEF" for c in core)


def resolve(token):
    """Return (data, path) for token, or (None, None). ID path avoids globbing."""
    # 1) Exact id -> direct file read, O(1)
    direct = os.path.join(LIVE, f"{token}.json")
    if os.path.exists(direct):
        return _load(direct), direct

    # 2) Scan once; collect candidates by id-prefix, exact name, substring name
    cands = []  # (rank, captured_at, data, path)
    tok_l = token.lower()
    for path in glob.glob(os.path.join(LIVE, "*.json")):
        d = _load(path)
        if not d:
            continue
        sid = (d.get("session_id") or "")
        name = (d.get("session_name") or "")
        cap = d.get("_captured_at") or 0
        if _is_uuid_like(token) and sid.replace("-", "").lower().startswith(tok_l.replace("-", "")):
            rank = 0  # id-prefix match is strongest
        elif name.lower() == tok_l:
            rank = 1  # exact name
        elif tok_l in name.lower() and name:
            rank = 2  # substring name
        else:
            continue
        cands.append((rank, cap, d, path))
    if not cands:
        return None, None
    # best rank, then freshest
    cands.sort(key=lambda c: (c[0], -c[1]))
    best = cands[0]
    return best[2], best[3]


def dig(d, dotted):
    cur = d
    for part in dotted.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return None, False
    return cur, True


def summary(d, path):
    m = d.get("model") or {}
    e = d.get("effort") or {}
    cw = d.get("context_window") or {}
    cost = d.get("cost") or {}
    rl = d.get("rate_limits") or {}
    fh = (rl.get("five_hour") or {})
    sd = (rl.get("seven_day") or {})
    age = ""
    cap = d.get("_captured_at")
    if cap:
        try:
            age = f"  ({int(time.time()) - int(cap)}s ago)"
        except Exception:
            pass
    print(f"session : {d.get('session_id')}")
    print(f"name    : {d.get('session_name')}")
    print(f"model   : {m.get('display_name')} [{m.get('id')}]")
    print(f"effort  : {e.get('level')}  (label: {d.get('_effort_label')})")
    print(f"context : {cw.get('used_percentage')}% used  ({cw.get('total_input_tokens')} in / window {cw.get('context_window_size')})  exceeds_200k={d.get('exceeds_200k_tokens')}")
    print(f"fast    : {d.get('fast_mode')} | thinking: {(d.get('thinking') or {}).get('enabled') if isinstance(d.get('thinking'), dict) else d.get('thinking')} | style: {(d.get('output_style') or {}).get('name')}")
    print(f"cwd     : {d.get('cwd')}")
    print(f"cost    : ${cost.get('total_cost_usd')}  (+{cost.get('total_lines_added')}/-{cost.get('total_lines_removed')} lines)")
    print(f"limits  : 5h {fh.get('used_percentage')}%  7d {sd.get('used_percentage')}%")
    print(f"version : {d.get('version')}")
    print(f"captured: {cap}{age}")
    print(f"snapshot: {path}")


def list_all():
    rows = []
    now = int(time.time())
    for path in glob.glob(os.path.join(LIVE, "*.json")):
        d = _load(path)
        if not d:
            continue
        cap = d.get("_captured_at") or 0
        rows.append((cap, d.get("session_id") or "", d.get("session_name"),
                     (d.get("model") or {}).get("display_name")))
    rows.sort(key=lambda r: -r[0])
    print(f"{'AGE':>7}  {'SESSION ID':36}  {'MODEL':12}  NAME")
    for cap, sid, name, model in rows:
        age = f"{now - cap}s" if cap else "?"
        print(f"{age:>7}  {sid:36}  {str(model):12}  {name}")
    return 0


def main(argv):
    args = argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return 0 if args else 1
    if args[0] in ("--list", "-l", "ls"):
        return list_all()

    token = args[0]
    mode = None
    field = None
    if "--json" in args:
        mode = "json"
    if "--field" in args:
        i = args.index("--field")
        if i + 1 < len(args):
            field = args[i + 1]
            mode = "field"
        else:
            print("--field needs a dotted path", file=sys.stderr)
            return 2

    d, path = resolve(token)
    if d is None:
        print(f"NO SNAPSHOT for '{token}' (session gone / never wrote one / name not found)", file=sys.stderr)
        return 1

    if mode == "json":
        print(json.dumps(d, indent=2))
    elif mode == "field":
        val, ok = dig(d, field)
        if not ok:
            print(f"field '{field}' not present", file=sys.stderr)
            return 2
        print(val if not isinstance(val, (dict, list)) else json.dumps(val))
    else:
        summary(d, path)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
