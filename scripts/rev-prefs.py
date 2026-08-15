#!/usr/bin/env python3
"""Resolve fire17's rev preferences for the current context.

The rev skills (/rev, /rev-reminder, /rev-update, /highest-rev,
/workflow-model-guard) call this instead of hardcoding numbers or models, so
editing ~/.claude/rev-prefs.toml changes every agent's behavior with no skill
edits and nothing to remember.

Resolution order (later wins):
    built-in fallbacks < [defaults] < [profiles.<name>] < [projects."<prefix>"]

Anything the user says live in the conversation outranks all of it — state the
override and follow it; the file is the standing default, not a cage.

Usage:
    python3 ~/.claude/scripts/rev-prefs.py                 # resolved for cwd
    python3 ~/.claude/scripts/rev-prefs.py --project ~/x   # for another path
    python3 ~/.claude/scripts/rev-prefs.py --profile max   # layer a profile
    python3 ~/.claude/scripts/rev-prefs.py --json          # machine-readable
    python3 ~/.claude/scripts/rev-prefs.py --profiles      # list profiles
"""
import argparse
import json
import os
import sys
import tomllib

CLAUDE_DIR = os.environ.get("CLAUDE_CONFIG_DIR") or os.path.expanduser("~/.claude")
PREFS = os.path.join(CLAUDE_DIR, "rev-prefs.toml")

# Last-resort values if the file is missing or unreadable — the suite still
# works, and says loudly that it is running on fallbacks.
FALLBACK = {
    "workflow_floor": 5,
    "workflow_ceiling": 10,
    "fleet_min": 12,
    "tier2_model": "fable",
    "tier3_model": "opus-5",
    "forbidden_models": ["opus-4.8", "sonnet", "haiku"],
    "teammate_effort": "ultracode",
    "reap_done_immediately": True,
    "caveman_in_subagents": False,
    "close_out_report": "html",
}


def load():
    try:
        with open(PREFS, "rb") as fh:
            return tomllib.load(fh), None
    except FileNotFoundError:
        return {}, f"{PREFS} not found — using built-in fallbacks"
    except Exception as exc:  # malformed TOML must never block an agent
        return {}, f"{PREFS} unreadable ({exc}) — using built-in fallbacks"


def norm(path: str) -> str:
    return os.path.realpath(os.path.expanduser(path))


def resolve(doc, project, profile):
    values = dict(FALLBACK)
    source = {k: "fallback" for k in values}

    for k, v in (doc.get("defaults") or {}).items():
        values[k], source[k] = v, "defaults"

    if profile:
        block = (doc.get("profiles") or {}).get(profile)
        if block is None:
            return None, None, f"unknown profile {profile!r}"
        for k, v in block.items():
            values[k], source[k] = v, f"profile:{profile}"

    # longest matching path prefix wins
    best, best_len = None, -1
    for raw, block in (doc.get("projects") or {}).items():
        p = norm(raw)
        if (project == p or project.startswith(p.rstrip("/") + "/")) and len(p) > best_len:
            best, best_len = (raw, block), len(p)
    if best:
        raw, block = best
        for k, v in block.items():
            values[k], source[k] = v, f"project:{raw}"

    return values, source, None


def main() -> int:
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--project", default=os.getcwd())
    ap.add_argument("--profile")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--profiles", action="store_true")
    args = ap.parse_args()

    doc, warn = load()

    if args.profiles:
        names = sorted((doc.get("profiles") or {}).keys())
        print("\n".join(names) if names else "(no profiles defined)")
        return 0

    values, source, err = resolve(doc, norm(args.project), args.profile)
    if err:
        print(f"ERROR: {err}", file=sys.stderr)
        print("available profiles:", ", ".join(sorted((doc.get("profiles") or {}).keys())) or "(none)",
              file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps({"values": values, "source": source,
                          "project": args.project, "profile": args.profile,
                          "warning": warn}, indent=2))
        return 0

    if warn:
        print(f"⚠️  {warn}\n")
    print(f"REV PREFS — project {args.project}" + (f" · profile {args.profile}" if args.profile else ""))
    print(f"  band            : {values['workflow_floor']}–{values['workflow_ceiling']} live workflows per agent")
    print(f"  fleet min       : {values['fleet_min']} teammates")
    print(f"  tier 2 model    : {values['tier2_model']}   (tmux teammates)")
    print(f"  tier 3 model    : {values['tier3_model']}   (agents inside their workflows)")
    print(f"  forbidden       : {', '.join(values['forbidden_models'])}")
    print(f"  teammate effort : {values['teammate_effort']}")
    print(f"  reap done now   : {values['reap_done_immediately']}")
    print(f"  caveman in subs : {values['caveman_in_subagents']}")
    print(f"  close-out report: {values['close_out_report']}")
    overrides = {k: v for k, v in source.items() if v not in ("fallback", "defaults")}
    if overrides:
        print("  overridden by   : " + ", ".join(f"{k} ← {v}" for k, v in sorted(overrides.items())))
    print("\n(user's live instructions outrank this file — say so and follow them)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
