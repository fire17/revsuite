#!/usr/bin/env python3
"""
identify — report the CURRENT Claude Code session id and which terminal
multiplexer is hosting it: tmux, herdr, or none.

Also reports live session state — name, model, effort, fast-mode, thinking,
context-window fill %, output style, repo, cost, rate limits, version — read from
the cship live snapshot (~/.cship/live/<session_id>.json), the authoritative,
real-time source Claude Code maintains automatically. The transcript records the
model per message but has NO effort field, so cship is the only per-session source
for effort. Exposed via session_details(snap) and get_context_window_size().

Deliberately does NOT treat a specific window/tab/pane as durable: multiplexers
reindex and a session can be moved between panes. The *multiplexer* is the stable
fact. We still resolve the current location as a convenience, but flag it as
volatile and tell you to re-resolve by pid/tty inside that multiplexer before
acting on it.

Usage: python3 ~/.claude/skills/identify/identify.py
       or import and use: get_context_window_size(session_id)
"""
import json
import os
import subprocess
import sys
from pathlib import Path


def _run(cmd, env=None):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, env=env)
    except (PermissionError, FileNotFoundError, OSError) as e:
        # A sandbox (e.g. `--dangerously-skip-permissions` teammate agents) can BLOCK
        # executing a binary like `ps` → PermissionError. Degrade gracefully (return a
        # non-zero, empty result) instead of crashing /identify — callers fall back to
        # env vars, macOS libproc (a syscall), and the cship snapshot. identify must
        # ALWAYS resolve the caller's identity, under ANY security posture.
        return subprocess.CompletedProcess(cmd, 126, "", f"{type(e).__name__}: {e}")


# ---------- ps-free process introspection (macOS libproc / sysctl via ctypes) ------
# `ps` is the fast primary path; when a sandbox blocks it, these read the same facts
# straight from the kernel (syscalls, no spawned binary). Everything DEGRADES to
# None/"" if unavailable → callers fall back to env + the cship snapshot. NEVER raises.
def _libproc():
    try:
        import ctypes
        return ctypes.CDLL("/usr/lib/libproc.dylib", use_errno=True)
    except Exception:
        return None


def _comm(pid):
    """basename of a pid's executable. `ps -o comm=` first; libproc fallback."""
    try:
        out = _run(["ps", "-o", "comm=", "-p", str(pid)]).stdout.strip()
    except Exception:
        out = ""
    if out:
        return out
    lib = _libproc()
    if lib:
        try:
            import ctypes
            buf = ctypes.create_string_buffer(1024)
            if lib.proc_pidpath(int(pid), buf, 1024) > 0:
                return buf.value.decode(errors="replace").rsplit("/", 1)[-1]
            nm = ctypes.create_string_buffer(256)
            if lib.proc_name(int(pid), nm, 256) > 0:
                return nm.value.decode(errors="replace")
        except Exception:
            pass
    return ""


def _ppid(pid):
    """parent pid. `ps -o ppid=` first; libproc proc_pidinfo(PROC_PIDTBSDINFO) fallback."""
    try:
        out = _run(["ps", "-o", "ppid=", "-p", str(pid)]).stdout.strip()
    except Exception:
        out = ""
    if out.isdigit():
        return int(out)
    lib = _libproc()
    if lib:
        try:
            import ctypes, struct
            buf = ctypes.create_string_buffer(512)
            n = lib.proc_pidinfo(int(pid), 3, ctypes.c_uint64(0), buf, 512)  # PROC_PIDTBSDINFO=3
            if n > 0:
                return struct.unpack_from("<I", buf.raw, 16)[0]              # pbi_ppid @ offset 16
        except Exception:
            pass
    return None


def _is_claude(pid):
    return _comm(pid).endswith("claude")


def _proc_args(pid):
    """Full argv of a pid (for reading --agent-* launch flags). `ps -ww -o args=` first;
    sysctl KERN_PROCARGS2 fallback (ctypes) so role/@label detection survives a ps block."""
    raw = _run(["ps", "-ww", "-o", "args=", "-p", str(pid)]).stdout.strip()
    if raw:
        return raw
    try:
        import ctypes, struct
        libc = ctypes.CDLL("/usr/lib/libc.dylib", use_errno=True)
        mib = (ctypes.c_int * 3)(1, 49, int(pid))            # CTL_KERN=1, KERN_PROCARGS2=49
        size = ctypes.c_size_t(0)
        if libc.sysctl(mib, 3, None, ctypes.byref(size), None, 0) != 0 or size.value < 4:
            return ""
        buf = ctypes.create_string_buffer(size.value)
        if libc.sysctl(mib, 3, buf, ctypes.byref(size), None, 0) != 0:
            return ""
        data = buf.raw[:size.value]
        argc = struct.unpack_from("i", data, 0)[0]
        toks = [t.decode(errors="replace") for t in data[4:].split(b"\0") if t]
        return " ".join(toks[1:argc + 1]) if len(toks) > 1 else " ".join(toks)  # skip exec path
    except Exception:
        return ""


# ---------- who am I -------------------------------------------------------

def _ancestry():
    """pids from us up to init (nearest first). ps-free capable (libproc _ppid)."""
    out, pid = [], os.getpid()
    for _ in range(40):
        pp = _ppid(pid)
        if not pp or pp in (0, 1):
            break
        pid = pp
        out.append(pid)
    return out


def _sessions_index():
    """{sessionId: pid} from ~/.claude/sessions/<pid>.json"""
    idx = {}
    for f in (Path.home() / ".claude" / "sessions").glob("*.json"):
        try:
            d = json.loads(f.read_text())
        except Exception:
            continue
        if d.get("sessionId") and d.get("pid"):
            idx[d["sessionId"]] = d["pid"]
    return idx


def current_session():
    """Return (session_id, pid). Env is authoritative for the id; the pid comes
    from the session file, falling back to whichever ancestor is a live claude."""
    idx = _sessions_index()
    sid = os.environ.get("CLAUDE_CODE_SESSION_ID") or os.environ.get("CLAUDE_SESSION_ID")
    if sid and sid in idx:
        return sid, idx[sid]
    # fallback: find a claude process in our ancestry, map pid -> session
    pid_to_sid = {p: s for s, p in idx.items()}
    for pid in _ancestry():
        if _is_claude(pid):
            return pid_to_sid.get(pid, sid), pid
    return sid, (idx.get(sid) if sid else None)


def _nearest_claude_pid():
    """The nearest `claude` process at or above us in the ancestry — i.e. the process
    we are actually running under. For a separate-process teammate/subagent this is
    the subagent's OWN `claude` (which carries the --agent-* flags); for a main agent
    it's the main `claude`. More reliable than the env→session pid, which a subagent
    can inherit from its parent (making it look like the parent)."""
    for p in _ancestry():
        if _is_claude(p):
            return p
    return None


# ---------- main agent vs subagent -----------------------------------------

# Flags Claude Code passes when it spawns a teammate/subagent as its own `claude`
# process (e.g. `--agent-name test-opus-agent --parent-session-id … --team-name …`).
# A MAIN agent has none of these. This is the ONLY source — the cship snapshot does
# not carry the agent label.
_AGENT_FLAGS = {
    "--agent-name": "name",
    "--agent-id": "id",
    "--team-name": "team",
    "--agent-color": "color",
    "--parent-session-id": "parent_session_id",
    "--agent-type": "agent_type",
}


def agent_info(pid):
    """Inspect the hosting `claude` process's launch flags to tell a SUBAGENT
    (teammate) from a MAIN agent and recover its label (e.g. '@test-opus-agent').
    Returns a dict with role ('main'|'subagent'), label, and the parsed fields."""
    info = {"role": "main", "label": None, "name": None, "id": None, "team": None,
            "color": None, "parent_session_id": None, "agent_type": None}
    if not pid:
        return info
    import shlex
    raw = _proc_args(pid)                # ps -ww -o args= first, sysctl KERN_PROCARGS2 fallback
    if not raw:
        return info
    try:
        toks = shlex.split(raw)
    except Exception:
        toks = raw.split()
    i = 0
    while i < len(toks):
        t = toks[i]
        if t in _AGENT_FLAGS:                       # --flag value
            key, val = _AGENT_FLAGS[t], (toks[i + 1] if i + 1 < len(toks) else None)
            i += 2
        elif "=" in t and t.split("=", 1)[0] in _AGENT_FLAGS:  # --flag=value
            k, val = t.split("=", 1)
            key = _AGENT_FLAGS[k]
            i += 1
        else:
            i += 1
            continue
        if val is not None:
            info[key] = val
    if any(info[k] for k in ("name", "id", "team", "parent_session_id")):
        info["role"] = "subagent"
        info["label"] = ("@" + info["name"]) if info["name"] else (info["id"] or "@subagent")
    return info


# ---------- where am I -----------------------------------------------------

def _tty_for_pid(pid):
    return _run(["ps", "-o", "tty=", "-p", str(pid)]).stdout.strip() or None


_TMUX_FIELDS = ("pane_tty", "pane_pid", "session_name", "session_id", "window_id",
                "window_index", "window_name", "pane_id", "pane_index", "@claude_session")


def find_tmux(pid):
    """Locate the tmux pane hosting `pid`; return its FULL address as a dict, or None.
    Carries BOTH the volatile indices (session:window.pane — reindex on create/close/move)
    and the STABLE ids ($session_id / @window_id / %pane_id, never reindexed for the
    server's life — target with `-t %N`), plus the `@claude_session` marker set by the
    autoname hook (the cross-restart handle keyed to the Claude session id)."""
    fmt = "\t".join("#{" + f + "}" for f in _TMUX_FIELDS)
    r = _run(["tmux", "list-panes", "-a", "-F", fmt])
    if r.returncode != 0:
        return None  # tmux not running / not installed
    tty = _tty_for_pid(pid)
    for line in r.stdout.splitlines():
        p = line.split("\t")
        if len(p) != len(_TMUX_FIELDS):
            continue
        pane_tty, pane_pid = p[0], p[1]
        if pane_pid == str(pid) or (tty and pane_tty.replace("/dev/", "") == tty):
            return {"session_name": p[2], "session_id": p[3], "window_id": p[4],
                    "window_index": p[5], "window_name": p[6], "pane_id": p[7],
                    "pane_index": p[8], "claude_session": (p[9] or None),
                    "display": f"{p[2]}:{p[5]}.{p[8]}"}   # volatile session:window.pane
    return None


# ---------- herdr namespaces (worlds) --------------------------------------
# fire17 runs several independent herdr worlds side by side: stable `herdr`
# (~/.config/herdr), the `herdr-dev` playground (~/.config/herdr-dev), and `hd`
# (the daily driver, ~/.config/hd). Each is its OWN binary + config dir + server/
# sockets; a binary SELF-SELECTS its namespace at runtime (stable = release build,
# herdr-dev = debug_assertions, hd = a compile-time-baked HERDR_NAMESPACE). To ask
# the RIGHT server "which pane hosts me?" we must run the RIGHT binary with the
# caller's HERDR_* socket overrides STRIPPED so nothing repoints it — otherwise a
# bare `herdr` follows whatever socket our env points at and reports the wrong world
# (or nothing). Data-driven: add a world = one entry, no scattered elifs.
# (Mirrors nexus.py's resolver so the two tools agree on routing.)
DEFAULT_NAMESPACE = "herdr"
HERDR_NAMESPACES = {
    "herdr":     {"config": "herdr",     "binaries": ["/opt/homebrew/bin/herdr", "herdr"]},
    "herdr-dev": {"config": "herdr-dev", "binaries": ["~/Patches/Hedr/herdr/target/debug/herdr"]},
    # hd's /opt/homebrew/bin/hd is a launcher SCRIPT, not a herdr binary — use the real
    # built binary, which carries HERDR_NAMESPACE=hd baked in at compile time (patch 0106).
    "hd":        {"config": "hd",        "binaries": ["~/Patches/Hedr/hd-build/debug/herdr"]},
}
_CONFIG_TO_NAMESPACE = {v["config"]: k for k, v in HERDR_NAMESPACES.items()}
MUX_DIR = Path.home() / ".cship" / "mux"


def _herdr_bin(namespace=None):
    """Absolute path (or bare `herdr` for PATH resolution) of the binary for `namespace`.
    Falls back to the stable binary when a world's build is missing — a missing dev/hd
    binary can only make a lookup FAIL to match (that world's panes aren't on the stable
    server), never MIS-report a wrong pane, so the fallback is safe."""
    spec = HERDR_NAMESPACES.get(namespace or DEFAULT_NAMESPACE)
    if spec:
        for b in spec["binaries"]:
            p = os.path.expanduser(b)
            if "/" not in p:            # bare name -> trust PATH
                return p
            if os.path.exists(p):
                return p
    return "herdr"


def _herdr_clean_env():
    """os.environ minus every HERDR_* var, so a herdr binary self-selects its OWN world
    instead of following an inherited HERDR_SOCKET_PATH we picked up from being launched
    inside some other herdr world. Makes binary-based routing deterministic (mirrors the
    herdr-dev launcher, which strips all HERDR_*)."""
    return {k: v for k, v in os.environ.items() if not k.startswith("HERDR_")}


def _herdr_run(cmd):
    """Run a herdr CLI command with a namespace-clean env (see _herdr_clean_env)."""
    return _run(cmd, env=_herdr_clean_env())


def _namespace_from_socket(socket_path):
    """Namespace implied by a HERDR_SOCKET_PATH, read from its `…/.config/<name>/…`
    config-dir segment. None when the path names no known world."""
    if not socket_path:
        return None
    parts = os.path.normpath(socket_path).split(os.sep)
    for i, seg in enumerate(parts):
        if seg == ".config" and i + 1 < len(parts):
            return _CONFIG_TO_NAMESPACE.get(parts[i + 1])
    return None


def resolve_namespace(sid, env=None):
    """Which herdr world hosts claude session `sid`. Resolution order:
      (a) ~/.cship/mux/<sid>.json .namespace — AUTHORITATIVE (herdr++ writes it) when present;
      (b) env HERDR_SOCKET_PATH's config-dir name — for /identify this is OUR OWN pane's env,
          which authoritatively names our own world;
      (c) stable ('herdr') default.
    Never raises; unknown/foreign values degrade to the default."""
    try:
        f = MUX_DIR / f"{sid}.json"
        if f.exists():
            ns = json.loads(f.read_text()).get("namespace")
            if ns in HERDR_NAMESPACES:
                return ns
    except Exception:
        pass
    ns = _namespace_from_socket((env or {}).get("HERDR_SOCKET_PATH"))
    if ns:
        return ns
    return DEFAULT_NAMESPACE


def _herdr_sessions(namespace=None):
    """Names of all running herdr sessions, e.g. ['default', 'Recovery', 'Recovery2'], in
    `namespace`'s world. herdr supports multiple NAMED sessions (each its own server/socket).
    Pane ids are unique only WITHIN a session and collide across them, so a bare `herdr pane …`
    silently targets whichever session the caller's env points at (usually 'default')
    — which is why we must enumerate and scope every lookup with `--session <name>`.
    Falls back to ['default'] if enumeration fails."""
    r = _herdr_run([_herdr_bin(namespace), "session", "list", "--json"])
    if r.returncode == 0:
        try:
            names = [s.get("name") for s in json.loads(r.stdout).get("sessions", [])
                     if s.get("name") and s.get("running", True)]
            if names:
                return names
        except Exception:
            pass
    return ["default"]


def _herdr_base(session, namespace=None):
    return [_herdr_bin(namespace)] + (["--session", session] if session else [])


def _herdr_pane_for_pid(pid, session, namespace=None):
    """The full pane object in `session` (within `namespace`'s world) whose foreground owns
    `pid`, or None. The pane object carries the whole address — workspace_id, tab_id,
    pane_id — not just the pane."""
    r = _herdr_run(_herdr_base(session, namespace) + ["pane", "list"])
    if r.returncode != 0:
        return None
    try:
        panes = json.loads(r.stdout).get("result", {}).get("panes", [])
    except Exception:
        return None
    for p in panes:
        pane_id = p.get("pane_id")
        if not pane_id:
            continue
        ir = _herdr_run(_herdr_base(session, namespace) + ["pane", "process-info", "--pane", pane_id])
        try:
            info = json.loads(ir.stdout).get("result", {}).get("process_info", {})
        except Exception:
            continue
        fg = {fp.get("pid") for fp in (info.get("foreground_processes") or [])}
        fg.add(info.get("foreground_process_group_id"))
        if pid in fg:
            return p                                 # full pane dict (workspace/tab/pane)
    return None


def find_herdr(pid, namespace=None):
    """Locate the herdr pane whose foreground process is `pid`, searching ACROSS every
    named herdr session IN `namespace`'s world (which binary/server we ask; see
    resolve_namespace) — a pid has exactly one controlling pane, so the match is
    unambiguous even though pane ids collide across sessions. The pane we are actually in
    is advertised by HERDR_SESSION, so we try that FIRST as an authoritative fast path,
    then scan the rest. Returns (session, pane_obj) or None — pane_obj carries the full
    workspace:tab:pane address."""
    hint = os.environ.get("HERDR_SESSION") or None
    if hint and (pane := _herdr_pane_for_pid(pid, hint, namespace)):
        return hint, pane
    for s in _herdr_sessions(namespace):
        if s == hint:
            continue
        pane = _herdr_pane_for_pid(pid, s, namespace)
        if pane:
            return s, pane
    return None


def _strip_ws(workspace, x):
    """'w1:t0' → 't0' when workspace is 'w1' (tab/pane ids embed the workspace prefix)."""
    pre = f"{workspace}:"
    return x[len(pre):] if workspace and x and x.startswith(pre) else x


def herdr_address(session, pane):
    """Build the FULL herdr address from a matched pane object. herdr addresses a pane
    absolutely by session:workspace:tab:pane — and we may be in a non-default WORKSPACE,
    not just a non-default session — so we surface every component. Returns a dict plus a
    compact display string 'session:workspace:tab:pane' (tab/pane workspace-prefix removed
    since it's shown once). `pane_ref` is the raw pane_id herdr commands actually take."""
    ws = pane.get("workspace_id")
    tab = pane.get("tab_id")
    pane_id = pane.get("pane_id")
    display = ":".join(x for x in (session, ws, _strip_ws(ws, tab), _strip_ws(ws, pane_id)) if x)
    return {
        "session": session,
        "workspace": ws,
        "tab": tab,
        "pane": pane_id,          # raw pane_id (what `herdr … pane <cmd> <pane_id>` expects)
        "pane_ref": pane_id,
        "display": display,       # session:workspace:tab:pane (deduped)
    }


def _herdr_agent_name(session, pane_id, namespace=None):
    """The STABLE herdr agent name of a pane (set by the herdr-autoname SessionStart
    hook as '<friendly> [<sid8>]'), or None. Lives on the `agent` view, not `pane list`,
    so we fetch it with one `agent get`. This name is the persistent handle that defeats
    address volatility — it resolves the pane by the Claude session id regardless of
    pane/tab index, and is re-applied on every start so it survives herdr recovery."""
    r = _herdr_run(_herdr_base(session, namespace) + ["agent", "get", pane_id])
    try:
        return json.loads(r.stdout).get("result", {}).get("agent", {}).get("name") or None
    except Exception:
        return None


def _set_herdr_fields(result, addr, namespace=None):
    """Copy the four herdr address components (+ the stable agent name + the world/namespace)
    onto result."""
    result["herdr_session"] = addr["session"]
    result["herdr_workspace"] = addr["workspace"]
    result["herdr_tab"] = addr["tab"]
    result["herdr_pane"] = addr["pane"]
    result["herdr_address"] = addr["display"]
    result["herdr_namespace"] = namespace or DEFAULT_NAMESPACE
    result["herdr_agent_name"] = _herdr_agent_name(addr["session"], addr["pane"], namespace)


def _set_tmux_fields(result, info):
    """Copy the tmux address onto result: volatile session:window.pane display + the STABLE
    ids ($session_id / @window_id / %pane_id) + the @claude_session marker."""
    result["tmux_session"] = info["session_name"]
    result["tmux_session_id"] = info["session_id"]        # $N (stable)
    result["tmux_window"] = f"{info['window_index']}:{info['window_name']}"
    result["tmux_window_id"] = info["window_id"]           # @N (stable)
    result["tmux_pane"] = info["pane_id"]                  # %N (stable — target with -t %N)
    result["tmux_pane_index"] = info["pane_index"]
    result["tmux_address"] = info["display"]               # session:window.pane (volatile)
    result["tmux_claude_session"] = info["claude_session"] # @claude_session marker


# ---------- session details (model, effort, name, … from cship) -----------

def _load_cship_snapshot(session_id=None):
    """Load the cship live snapshot for a session — the authoritative, real-time
    state maintained automatically by Claude Code. Returns the parsed dict, or
    None if unavailable (cship not running, or session has no snapshot yet)."""
    if not session_id:
        session_id = (os.environ.get("CLAUDE_CODE_SESSION_ID")
                      or os.environ.get("CLAUDE_SESSION_ID"))
    if not session_id:
        return None
    try:
        with open(os.path.expanduser(f"~/.cship/live/{session_id}.json")) as f:
            return json.load(f)
    except Exception:
        return None


def _fmt_int(n):
    try:
        return f"{int(n):,}"
    except Exception:
        return str(n)


def _fmt_reset(ts):
    """Format a Unix-epoch reset time as 'YYYY-MM-DD HH:MM (in Xh Ym)'. None if absent."""
    if not ts:
        return None
    try:
        import time as _time
        from datetime import datetime
        ts = int(ts)
        when = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")
        delta = ts - int(_time.time())
        if delta <= 0:
            return f"{when} (now)"
        h, m = divmod(delta // 60, 60)
        rel = f"in {h}h {m}m" if h else f"in {m}m"
        return f"{when} ({rel})"
    except Exception:
        return None


def session_details(snap):
    """Flatten the human-interesting fields out of a cship snapshot. Everything is
    best-effort; missing pieces come back as None. This is the ONE authoritative
    per-session source for model + effort (the transcript records model but has no
    effort field at all)."""
    if not snap:
        return {}
    model = snap.get("model") or {}
    effort = snap.get("effort") or {}
    ctx = snap.get("context_window") or {}
    cost = snap.get("cost") or {}
    rl = snap.get("rate_limits") or {}
    repo = ((snap.get("workspace") or {}).get("repo")) or {}
    return {
        "session_name": snap.get("session_name"),
        "model_id": model.get("id"),
        "model_display": model.get("display_name"),
        "effort_level": effort.get("level"),
        "effort_label": snap.get("_effort_label"),  # e.g. "ultracode" for xhigh+workflows
        "fast_mode": snap.get("fast_mode"),
        "thinking": (snap.get("thinking") or {}).get("enabled"),
        "output_style": (snap.get("output_style") or {}).get("name"),
        "context_window_size": ctx.get("context_window_size"),
        "context_used_pct": ctx.get("used_percentage"),
        "context_remaining_pct": ctx.get("remaining_percentage"),
        "exceeds_200k_tokens": snap.get("exceeds_200k_tokens"),
        "version": snap.get("version"),
        "cwd": snap.get("cwd"),
        "repo": (f"{repo.get('owner')}/{repo.get('name')}" if repo.get("name") else None),
        "cost_usd": cost.get("total_cost_usd"),
        "lines_added": cost.get("total_lines_added"),
        "lines_removed": cost.get("total_lines_removed"),
        "rate_limit_5h_pct": (rl.get("five_hour") or {}).get("used_percentage"),
        "rate_limit_5h_resets_at": (rl.get("five_hour") or {}).get("resets_at"),
        "rate_limit_7d_pct": (rl.get("seven_day") or {}).get("used_percentage"),
        "rate_limit_7d_resets_at": (rl.get("seven_day") or {}).get("resets_at"),
    }


# ---------- goal (/goal session-scoped Stop hook) --------------------------

# Claude Code does NOT persist active-goal state to any queryable file (verified:
# not in settings.json, ~/.claude.json, ~/.claude/sessions/<pid>.json, session-env/,
# or the cship snapshot). The session transcript is the ONLY source. We read the two
# structured markers CC writes there — deterministic parsing, no AI, no guessing:
#   SET  : a `type:user, isMeta:true` record whose text is
#          'A session-scoped Stop hook is now active with condition: "<CONDITION>"'
#   CLEAR: `/goal clear` command, a "Goal cleared" stdout, or an away_summary recap
#          noting the goal auto-cleared.
# The genuine goal reminder is a standalone isMeta user message that STARTS with this
# exact prefix. Requiring startswith (not just substring) is what makes detection robust
# against contamination — the skill's own docs, and any message that merely *quotes* the
# phrase (like this file, or a discussion about goals), embed it mid-text and are ignored.
_GOAL_SET = "Stop hook is now active with condition:"          # cheap prefilter substring
_GOAL_SET_PREFIX = "A session-scoped Stop hook is now active with condition:"


def goal_status(session_id=None, transcript_path=None):
    """Is a /goal currently active for the session, and what is its condition?

    Lightweight (substring-prefiltered single pass) and programmatic. Returns:
      {active: bool|None, condition: str|None, set_line, cleared_line, note}
    `active` is None only when the transcript can't be found.

    Reliability: the SET marker is authoritative. `/goal clear` and the auto-clear
    recap are detected too, but CC does not emit a guaranteed marker when a goal
    auto-clears because its condition was *met* — so a met-but-unsuperseded goal can
    still read active. This is a Claude Code limitation, not a bug here."""
    if not transcript_path:
        snap = _load_cship_snapshot(session_id)
        if snap:
            transcript_path = snap.get("transcript_path")
    if not transcript_path or not os.path.exists(transcript_path):
        return {"active": None, "condition": None,
                "set_line": None, "cleared_line": None, "note": "transcript not found"}

    import re
    last_set = (None, None)   # (line_no, condition)
    last_clear = None
    with open(transcript_path, errors="ignore") as f:
        for i, line in enumerate(f, 1):
            if "goal" not in line.lower() and _GOAL_SET not in line:
                continue
            try:
                d = json.loads(line)
            except Exception:
                continue
            if d.get("type") == "assistant":      # our own text — never authoritative
                continue
            m = d.get("message")
            c = m.get("content") if isinstance(m, dict) else (d.get("content") or m)
            if isinstance(c, list):
                c = " ".join(b.get("text", "") for b in c
                             if isinstance(b, dict) and b.get("type") == "text")
            if not isinstance(c, str) or not c:
                continue
            cs = c.lstrip()
            cl = c.lower()
            # SET (authoritative): a standalone isMeta reminder STARTING with the prefix.
            # (startswith, not substring — ignores docs/quotes that only mention it.)
            if d.get("isMeta") and cs.startswith(_GOAL_SET_PREFIX):
                cond = cs[len(_GOAL_SET_PREFIX):].lstrip()
                cond = cond[1:].split('"', 1)[0] if cond.startswith('"') else cond.split('.', 1)[0]
                last_set = (i, cond.strip())
                continue
            # CLEAR: explicit `/goal clear` — a real command record (structural, so the
            # skill docs' prose "/goal clear" can't false-trigger it).
            if "<command-name>/goal</command-name>" in c:
                ma = re.search(r"<command-args>(.*?)</command-args>", c, re.S)
                if ma and ma.group(1).strip().lower().startswith("clear"):
                    last_clear = i
                    continue
            # CLEAR: an away_summary recap noting the goal auto-cleared (a system subtype;
            # only genuine recaps carry it).
            if (d.get("subtype") == "away_summary"
                    and "goal" in cl and ("clear" in cl or "auto-clear" in cl)):
                last_clear = i

    set_line, cond = last_set
    if set_line is None:
        return {"active": False, "condition": None, "set_line": None,
                "cleared_line": last_clear, "note": "no /goal ever set"}
    active = last_clear is None or set_line > last_clear
    return {"active": active, "condition": cond if active else None,
            "last_condition": cond, "set_line": set_line, "cleared_line": last_clear,
            "note": None if active else "cleared/superseded after last set"}


# ---------- report ---------------------------------------------------------

def _location_from_env(result):
    """Populate multiplexer + location purely from ENV (no `ps`, no server scan) — a sound
    self-fallback when process introspection is sandbox-blocked (env describes OUR OWN pane).
    tmux: TMUX (`socket,pid,idx`) + TMUX_PANE (`%N`), incl. an agent-team claude-swarm socket;
    herdr: HERDR_SESSION / HERDR_WORKSPACE_ID / HERDR_TAB_ID / HERDR_PANE_ID."""
    tp, tmux = os.environ.get("TMUX_PANE"), os.environ.get("TMUX")
    if tp and tmux:
        sock = tmux.split(",")[0]
        result["multiplexer"] = "tmux"
        result["tmux_pane"] = tp
        result["tmux_socket"] = sock or None
        result["location"] = f"{(sock or 'default').rsplit('/', 1)[-1]}:{tp}"
        result["_resolved_via"] = "env (ps-free)"
        return True
    hs, hp = os.environ.get("HERDR_SESSION"), os.environ.get("HERDR_PANE_ID")
    if hs and hp:
        ws, tab = os.environ.get("HERDR_WORKSPACE_ID"), os.environ.get("HERDR_TAB_ID")
        result["multiplexer"] = "herdr"
        result["herdr_session"], result["herdr_workspace"] = hs, ws
        result["herdr_tab"], result["herdr_pane"] = tab, hp
        # Our own world, straight from our socket env (config-dir name) — no server call.
        result["herdr_namespace"] = (
            _namespace_from_socket(os.environ.get("HERDR_SOCKET_PATH")) or DEFAULT_NAMESPACE)
        result["herdr_address"] = ":".join(
            x for x in (hs, ws, _strip_ws(ws, tab), _strip_ws(ws, hp)) if x)
        result["location"] = result["herdr_address"]
        result["_resolved_via"] = "env (ps-free)"
        return True
    return False


def identify():
    sid, pid = current_session()
    # The process we actually run under. For a separate-process teammate/subagent this
    # is its OWN claude (carrying --agent-* flags); for a main agent it equals `pid`.
    # More reliable than the env→session pid, which a subagent inherits from its parent.
    pid = _nearest_claude_pid() or pid
    result = {"session_id": sid, "pid": pid, "multiplexer": "none", "location": None,
              "herdr_session": None, "herdr_workspace": None, "herdr_tab": None,
              "herdr_pane": None, "herdr_address": None, "herdr_agent_name": None,
              "herdr_namespace": None,
              "tmux_session": None, "tmux_session_id": None, "tmux_window": None,
              "tmux_window_id": None, "tmux_pane": None, "tmux_pane_index": None,
              "tmux_address": None, "tmux_claude_session": None, "also_within": []}

    # Which herdr WORLD hosts us — stable / herdr-dev / hd. Resolved from the authoritative
    # ~/.cship/mux/<sid>.json marker (herdr++ writes it) or, failing that, our OWN pane's
    # HERDR_SOCKET_PATH env. This picks the right binary/server to ask below, so a dev/hd
    # pane is reported against its own world instead of silently missed on the stable server.
    namespace = resolve_namespace(sid, os.environ)

    if pid:
        tmux_info = find_tmux(pid)                    # dict or None
        herdr_hit = find_herdr(pid, namespace)        # (session, pane_obj) or None
        addr = herdr_address(*herdr_hit) if herdr_hit else None
        # The *immediate* host is whichever one owns claude's own tty/pid.
        # (When tmux is nested inside a herdr pane, herdr's foreground is the
        #  tmux client, not claude, so find_herdr correctly returns None and we
        #  report tmux — the multiplexer you actually drive.)
        if tmux_info:
            result["multiplexer"], result["location"] = "tmux", tmux_info["display"]
            _set_tmux_fields(result, tmux_info)       # session/window/pane + stable ids
            if addr:
                _set_herdr_fields(result, addr, namespace)
                result["also_within"] = ["herdr:" + addr["display"]]
        elif addr:
            result["multiplexer"], result["location"] = "herdr", addr["display"]
            _set_herdr_fields(result, addr, namespace)  # session + workspace + tab + pane + world

    # ps-free fallback: if we couldn't resolve a pane (e.g. `ps` blocked in a sandbox, or a
    # teammate on a tmux socket we don't scan), fill the location straight from env — the
    # pane's own HERDR_*/TMUX vars are authoritative for "where am I" and need no process info.
    if result["multiplexer"] == "none":
        _location_from_env(result)

    agent = agent_info(pid)
    result["role"] = agent["role"]      # "main" | "subagent"
    result["agent"] = agent             # label/name/team/parent/type/color

    snap = _load_cship_snapshot(sid)
    details = session_details(snap)
    result["details"] = details  # nested to keep top-level keys stable for consumers

    goal = goal_status(sid, (snap or {}).get("transcript_path"))
    result["goal"] = goal

    print(json.dumps(result, ensure_ascii=False))
    print("---")
    print(f"session : {sid or '(unknown)'}")
    if details.get("session_name"):
        print(f"name    : {details['session_name']}")
    # active /goal (session-scoped Stop hook), if any
    if goal.get("active"):
        cond = goal.get("condition") or ""
        if len(cond) > 88:
            cond = cond[:85] + "…"
        print(f"goal    : ACTIVE — \"{cond}\"")
    elif goal.get("active") is None:
        print("goal    : (unknown — transcript not found)")
    else:
        print("goal    : none active")
    # main agent vs spawned subagent (teammate), + its label
    if agent["role"] == "subagent":
        print(f"role    : subagent   {agent['label']}")
        extra = []
        if agent.get("agent_type"):        extra.append(f"type {agent['agent_type']}")
        if agent.get("team"):              extra.append(f"team {agent['team']}")
        if agent.get("parent_session_id"): extra.append(f"parent {agent['parent_session_id']}")
        if agent.get("color"):             extra.append(f"color {agent['color']}")
        if extra:
            print("          " + " · ".join(extra))
    else:
        print("role    : main agent")
    print(f"pid     : {pid or '(unknown)'}")
    mux = result["multiplexer"]
    if mux == "none":
        print("host    : none — not inside tmux or herdr (plain terminal)")
    else:
        print(f"host    : {mux}")
        if mux == "herdr" and result.get("herdr_session"):
            # herdr addresses a pane absolutely by session:workspace:tab:pane. The named
            # SESSION and WORKSPACE are the durable parts you must pin (pane ids collide
            # across BOTH sessions and workspaces); the tab/pane index is volatile. Anything
            # injecting here MUST scope with `--session <name>` and the full pane_id.
            _ns = result.get("herdr_namespace") or DEFAULT_NAMESPACE
            _binhint = {"herdr": "herdr", "herdr-dev": "herdr-dev", "hd": "hd"}.get(_ns, _ns)
            print(f"world   : {_ns}   ← herdr WORLD (own binary+server); drive it with `{_binhint} … pane <cmd>`")
            print(f"address : {result['herdr_address']}   (session:workspace:tab:pane)")
            print(f"          session   = {result['herdr_session']}   ← pin with --session")
            print(f"          workspace = {result['herdr_workspace']}")
            print(f"          tab       = {result['herdr_tab']}")
            print(f"          pane      = {result['herdr_pane']}   ← pass to `herdr … pane <cmd>`")
            if result.get("herdr_agent_name"):
                # STABLE handle (claude-pane-autoname hook): survives reindex + recovery.
                print(f"agent   : {result['herdr_agent_name']}   ← STABLE — `herdr agent get \"{result['herdr_agent_name']}\"`")
            else:
                print("agent   : (unnamed — claude-pane-autoname hook not applied yet)")
            print("          ⚠️ tab/pane index is VOLATILE (reindex/move); the SESSION+WORKSPACE")
            print("          and the agent name are STABLE. Re-resolve the pane by pid before acting.")
        elif mux == "tmux" and result.get("tmux_pane"):
            # tmux addresses by session:window.pane INDICES (volatile) but assigns STABLE ids
            # $session_id/@window_id/%pane_id that never reindex for the server's life. Target
            # by %pane_id; the @claude_session marker (autoname hook) is the session-keyed handle.
            print(f"address : {result['tmux_address']}   (session:window.pane — VOLATILE indices)")
            print(f"          session = {result['tmux_session']}  ({result['tmux_session_id']})")
            print(f"          window  = {result['tmux_window']}  ({result['tmux_window_id']})")
            print(f"          pane    = {result['tmux_pane']}  (index {result['tmux_pane_index']})   ← STABLE: target `-t {result['tmux_pane']}`")
            if result.get("tmux_claude_session"):
                print(f"marker  : @claude_session={result['tmux_claude_session']}   ← STABLE, session-keyed")
            else:
                print("marker  : (none — claude-pane-autoname hook not applied yet)")
            print("          ⚠️ session:window.pane INDICES reindex on create/close/move;")
            print("          %pane_id / @window_id / $session_id are STABLE — always prefer them.")
        else:
            print(f"location: {result['location']}   ⚠️ VOLATILE (re-resolve by pid/tty)")
        if result["also_within"]:
            print(f"note    : also running within {', '.join(result['also_within'])} "
                  f"(outer layer); drive the inner {mux}.")

    # ---- live session state from cship (model, effort, name, context, …) ----
    if not snap:
        print("details : (cship snapshot unavailable — model/effort/name unknown)")
    else:
        md = details.get("model_display") or details.get("model_id") or "(unknown)"
        mid = details.get("model_id")
        print(f"model   : {md}" + (f"   [{mid}]" if mid and mid != md else ""))
        lvl, lab = details.get("effort_level"), details.get("effort_label")
        if lab and lvl and lab != lvl:
            print(f"effort  : {lab}  ({lvl})")
        else:
            print(f"effort  : {lab or lvl or '(unknown)'}")
        print(f"fast    : {'on' if details.get('fast_mode') else 'off'}")
        print(f"thinking: {'on' if details.get('thinking') else 'off'}")
        if details.get("context_window_size") is not None:
            used, rem = details.get("context_used_pct"), details.get("context_remaining_pct")
            print(f"context : {used}% used of {_fmt_int(details['context_window_size'])} tokens"
                  + (f"  ({rem}% free)" if rem is not None else ""))
        if details.get("output_style"):
            print(f"style   : {details['output_style']}")
        if details.get("repo"):
            print(f"repo    : {details['repo']}")
        if details.get("cost_usd") is not None:
            print(f"cost    : ${details['cost_usd']:.4f}  "
                  f"(+{details.get('lines_added') or 0}/-{details.get('lines_removed') or 0} lines)")
        if details.get("rate_limit_5h_pct") is not None:
            r5 = _fmt_reset(details.get("rate_limit_5h_resets_at"))
            r7 = _fmt_reset(details.get("rate_limit_7d_resets_at"))
            p5 = round(details["rate_limit_5h_pct"])
            p7 = round(details.get("rate_limit_7d_pct") or 0)
            print(f"limits  : 5h {p5:>2}%" + (f"  · resets {r5}" if r5 else ""))
            print(f"          7d {p7:>2}%" + (f"  · resets {r7}" if r7 else ""))
        if details.get("version"):
            print(f"version : {details['version']}")
    return result


# ---------- context window (future-proof, from cship) ---------------------------

def get_context_window_size(session_id=None):
    """
    Get the context window size for a session from the authoritative source (cship).

    Returns: int (context window size in tokens) or None if unable to determine.

    This is TRULY FUTURE-PROOF because:
    - cship snapshots are maintained automatically by Claude Code
    - When new Claude models are released, cship automatically has the correct window
    - No manual registry updates needed
    - Window size is determined by Claude Code itself at runtime from API metadata

    Query order:
    1. cship live snapshot (most reliable, automatic, future-proof)
    2. Returns None if not available (caller can fall back to registry if needed)
    """
    snap = _load_cship_snapshot(session_id)
    if not snap:
        return None
    try:
        # cship structure: context_window.context_window_size
        ctx_window = snap.get("context_window", {})
        if isinstance(ctx_window, dict):
            size = ctx_window.get("context_window_size")
            if size:
                return int(size)
    except Exception:
        pass

    return None


if __name__ == "__main__":
    r = identify()
    sys.exit(0 if r.get("session_id") else 1)
