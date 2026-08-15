#!/usr/bin/env python3
"""Rev priorities ledger — the durable big-picture layer above session todos.

Every priority keeps the user's words VERBATIM (never edited, never rewritten),
plus rich mutable state and two append-only, timestamped note streams (USER and
AGENT). Session todo lists die with the session; this file does not.

Path resolution: --file, else <git root>/.rev/PRIORITIES.md, else ./.rev/PRIORITIES.md

Commands:
    init                                   create the ledger if absent
    add "<verbatim text>" [--label L]      add a priority (or --stdin)
    note <id> --agent "…" | --user "…"     append a timestamped note
    status <id> <active|paused|achieved|superseded|dropped> [--why "…"]
    list                                   one line per priority
    show <id>                              print a priority block
"""
import argparse, os, re, subprocess, sys
from datetime import datetime

STATUSES = ("active", "paused", "achieved", "superseded", "dropped")


def stamp():
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %z")


def ledger_path(explicit=None):
    if explicit:
        return os.path.abspath(os.path.expanduser(explicit))
    root = os.getcwd()
    try:
        out = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, timeout=5)
        if out.returncode == 0 and out.stdout.strip():
            root = out.stdout.strip()
    except Exception:
        pass
    return os.path.join(root, ".rev", "PRIORITIES.md")


def read(path):
    return open(path, encoding="utf-8").read() if os.path.exists(path) else ""


def ensure(path):
    if os.path.exists(path):
        return False
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(
            f"# REV PRIORITIES — {os.path.basename(os.path.dirname(os.path.dirname(path))) or 'workspace'}\n\n"
            "> Managed by `/rev-priority`. VERBATIM blocks are SACRED — never edited,\n"
            "> never paraphrased, never reordered. State and notes are append-friendly.\n"
            "> Notes are timestamped and append-only; nothing here is ever deleted —\n"
            f"> retired priorities get `status: superseded` or `dropped`.\n>\n"
            f"> created {stamp()}\n"
        )
    return True


def next_id(text):
    ids = [int(m) for m in re.findall(r"^## P(\d+) ", text, re.M)]
    return f"P{max(ids) + 1 if ids else 1}"


def block_span(text, pid):
    m = re.search(rf"^## {re.escape(pid)} ", text, re.M)
    if not m:
        return None
    nxt = re.search(r"^## P\d+ ", text[m.end():], re.M)
    return (m.start(), m.end() + nxt.start() if nxt else len(text))


def cmd_add(args, path):
    ensure(path)
    body = sys.stdin.read() if args.stdin else args.text
    if not body or not body.strip():
        print("nothing to add (empty text)", file=sys.stderr)
        return 2
    text = read(path)
    pid = next_id(text)
    label = args.label or " ".join(body.split()[:7])
    block = (
        f"\n## {pid} · {label}  [status: active]  (created {stamp()})\n\n"
        f"### VERBATIM — the user's words (SACRED, never edit)\n"
        f"```text\n{body.rstrip()}\n```\n\n"
        f"### state\n"
        f"- rank: {pid[1:]}\n- status: active\n- serving lanes/workflows: (none yet)\n"
        f"- artifacts: (none yet)\n- measured progress: (not yet measured)\n\n"
        f"### subgoals\n- [ ] (decompose here)\n\n"
        f"### notes (append-only, newest last)\n"
        f"- {stamp()} · AGENT: priority recorded.\n"
    )
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(block)
    print(f"{pid} added → {path}")
    return 0


def cmd_note(args, path):
    text = read(path)
    span = block_span(text, args.id)
    if not span:
        print(f"unknown priority {args.id}", file=sys.stderr)
        return 2
    who = "USER" if args.user else "AGENT"
    line = f"- {stamp()} · {who}: {(args.user or args.agent).strip()}\n"
    block = text[span[0]:span[1]].rstrip("\n") + "\n" + line + "\n"
    open(path, "w", encoding="utf-8").write(text[:span[0]] + block + text[span[1]:])
    print(f"note added to {args.id} ({who})")
    return 0


def cmd_status(args, path):
    text = read(path)
    span = block_span(text, args.id)
    if not span:
        print(f"unknown priority {args.id}", file=sys.stderr)
        return 2
    block = text[span[0]:span[1]]
    block = re.sub(r"\[status: \w+\]", f"[status: {args.status}]", block, count=1)
    block = re.sub(r"^- status: \w+$", f"- status: {args.status}", block, count=1, flags=re.M)
    why = f" — {args.why}" if args.why else ""
    block = block.rstrip("\n") + f"\n- {stamp()} · AGENT: status → {args.status}{why}\n\n"
    open(path, "w", encoding="utf-8").write(text[:span[0]] + block + text[span[1]:])
    print(f"{args.id} → {args.status}")
    return 0


def cmd_list(args, path):
    text = read(path)
    rows = re.findall(r"^## (P\d+) · (.*?)  \[status: (\w+)\]", text, re.M)
    if not rows:
        print("(no priorities yet)")
        return 0
    for pid, label, st in rows:
        print(f"{pid:4} [{st:10}] {label}")
    return 0


def cmd_show(args, path):
    text = read(path)
    span = block_span(text, args.id)
    if not span:
        print(f"unknown priority {args.id}", file=sys.stderr)
        return 2
    print(text[span[0]:span[1]].rstrip())
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init")
    a = sub.add_parser("add"); a.add_argument("text", nargs="?"); a.add_argument("--stdin", action="store_true"); a.add_argument("--label")
    n = sub.add_parser("note"); n.add_argument("id"); g = n.add_mutually_exclusive_group(required=True)
    g.add_argument("--agent"); g.add_argument("--user")
    s = sub.add_parser("status"); s.add_argument("id"); s.add_argument("status", choices=STATUSES); s.add_argument("--why")
    sub.add_parser("list"); sh = sub.add_parser("show"); sh.add_argument("id")
    args = ap.parse_args()
    path = ledger_path(args.file)
    if args.cmd == "init":
        print(("created " if ensure(path) else "exists  ") + path); return 0
    if not os.path.exists(path) and args.cmd != "add":
        print(f"no ledger at {path} — run: rev-priorities.py init", file=sys.stderr); return 2
    return {"add": cmd_add, "note": cmd_note, "status": cmd_status,
            "list": cmd_list, "show": cmd_show}[args.cmd](args, path)


if __name__ == "__main__":
    sys.exit(main())
