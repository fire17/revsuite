#!/usr/bin/env python3
"""ripple_graph.py — the pseudo dependency graph behind /ripple.

Lightweight, stdlib-only. Nodes are creations/skills; edges are directed
multi<->multi links each carrying a SET OF FLAGS (one edge can be several
kinds of link at once). Cycle-safe by construction: every traversal uses a
visited set, so loops (A<->B, self-refs, diamonds) terminate correctly.

Answers the one question that matters: "X changed — what else must be
updated, and which of those must be REPUBLISHED?"

Commands
  scan                       rebuild the graph cache from the world
  affected <node> [...]      reverse closure: who depends on these nodes
  show <node>                edges in/out of a node
  check [path ...]           map dirty paths -> nodes -> ripple report
                             (noise-filtered: .DS_Store etc. never open the gate)
  markers [--refresh]        all .project markers, lazily cached (see project_markers)
  ensure-project <slug> [--dir] [k=v ...]   create/refresh a .project marker
  backfill                   create .project for every published creation
  selftest                   prove cycle-safety on a synthetic looped graph

Edge flags (open vocabulary — new flags cost nothing):
  alias             alias skill dir -> canonical skill
  vault-copy        Creations/Skills vault copy -> live skill
  snapshot          /sas snapshot dir -> live sources
  doc-mention       SKILL.md text references another node (/name)
  declared          curated edge from a .project refs-out line
  symlink-canonical skills-dir entry is a symlink into a repo checkout
"""
import json, os, re, sys, time

HOME = os.path.expanduser("~")
CREATIONS = os.path.join(HOME, "Creations")
SKILLS = os.path.join(HOME, ".claude", "skills")
VAULT = os.path.join(CREATIONS, "Skills")
CACHE_DIR = os.path.join(CREATIONS, ".ripple")
CACHE = os.path.join(CACHE_DIR, "graph.json")


# ---------- .project markers ----------

def project_marker_path(location):
    """Return the status-file path for a .project marker at `location`.
    Supports BOTH forms: a `.project` file, or a `.project/` dir whose
    status file is `.project/status`. File is the default; dir is chosen
    with --dir or inherited if a dir already exists."""
    root = os.path.expanduser(location)
    p = os.path.join(root, ".project")
    if os.path.isdir(p):
        return os.path.join(p, "status")
    return p


def read_project_marker(location):
    """Parse a .project marker: `key: value` lines until a `---` separator,
    freeform after (preserved verbatim, never parsed). Unknown lines before
    the separator are kept as freeform too — any structure/unstructure combo
    is legal by design."""
    path = project_marker_path(location)
    if not os.path.isfile(path):
        return None
    meta, free, in_free = {}, [], False
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.rstrip("\n")
            if in_free:
                free.append(line)
            elif line.strip() == "---":
                in_free = True
            elif re.match(r"^[A-Za-z0-9_-]+:\s", line) or re.match(r"^[A-Za-z0-9_-]+:$", line):
                k, _, v = line.partition(":")
                meta[k.strip()] = v.strip()
            elif line.startswith("#") or not line.strip():
                continue
            else:
                free.append(line)
    return {"path": path, "meta": meta, "freeform": free}


def write_project_marker(location, slug, extra=None, as_dir=False):
    root = os.path.expanduser(location)
    if not os.path.isdir(root):
        return None
    pdir = os.path.join(root, ".project")
    existing = read_project_marker(location)
    if as_dir and not os.path.isdir(pdir):
        if os.path.isfile(pdir):  # upgrade file -> dir, preserving content
            content = open(pdir, encoding="utf-8").read()
            os.remove(pdir)
            os.makedirs(pdir)
            with open(os.path.join(pdir, "status"), "w", encoding="utf-8") as f:
                f.write(content)
        else:
            os.makedirs(pdir)
    path = project_marker_path(location)
    today = time.strftime("%Y-%m-%d")
    meta = existing["meta"] if existing else {}
    meta.setdefault("slug", slug)
    meta.setdefault("first_shipped", today)
    meta["last_updated"] = today
    for kv in (extra or []):
        k, _, v = kv.partition("=")
        meta[k] = v
    free = existing["freeform"] if existing else []
    with open(path, "w", encoding="utf-8") as f:
        f.write("#project v1\n")
        for k, v in meta.items():
            f.write(f"{k}: {v}\n")
        f.write("---\n")
        f.write("\n".join(free) + ("\n" if free else ""))
    return path


# ---------- marker discovery (lazy, cached, near-zero cost per call) ----------

MARKER_CACHE = os.path.join(CACHE_DIR, "markers.json")
MARKER_ROOTS = (   # (root, max depth below root) — bounded walks, never a full-disk crawl
    (CREATIONS, 3),
    (SKILLS, 2),
)
_PRUNE_DIRS = {".git", ".venv", "node_modules", "__pycache__", "target", ".save_and_ship",
               "conversation", "files"}


def _walk_markers():
    found = []
    for root, maxdepth in MARKER_ROOTS:
        if not os.path.isdir(root):
            continue
        base_depth = root.rstrip(os.sep).count(os.sep)
        for dirpath, dirs, files in os.walk(root):
            depth = dirpath.count(os.sep) - base_depth
            if depth >= maxdepth:
                dirs[:] = []
            else:
                dirs[:] = [d for d in dirs if d not in _PRUNE_DIRS and not d.startswith(".")
                           or d == ".project"]
            hit = None
            if ".project" in dirs:
                hit = {"path": os.path.join(dirpath, ".project"), "form": "dir"}
                dirs.remove(".project")
            elif ".project" in files:
                hit = {"path": os.path.join(dirpath, ".project"), "form": "file"}
            if hit:
                hit["project_root"] = dirpath
                hit["vault_mirror"] = dirpath.startswith(VAULT)
                found.append(hit)
    return sorted(found, key=lambda h: h["path"])


def project_markers(refresh=False, ttl=300):
    """Programmatic entry point: every .project marker (file or dir) on the system.

    Lazy by design — the caller pays nothing on repeat calls:
    * cache hit (age < ttl AND every cached path still exists — a handful of stat
      calls, ~microseconds) -> return cached list, no walk;
    * anything else -> one bounded walk (two roots, depth-capped, pruned), then cache.
    A DELETED marker invalidates instantly (its stat fails); a NEW marker is seen at
    the next ttl expiry or refresh=True — that's the honest price of laziness, and
    ttl=300s keeps it far fresher than any human notices. Import from other tools:
        sys.path.insert(0, os.path.expanduser("~/.claude/skills/ripple/scripts"))
        from ripple_graph import project_markers
    """
    if not refresh and os.path.isfile(MARKER_CACHE):
        try:
            cached = json.load(open(MARKER_CACHE, encoding="utf-8"))
            fresh = (time.time() - cached.get("scanned_epoch", 0)) < ttl
            if fresh and all(os.path.exists(m["path"]) for m in cached["markers"]):
                return cached["markers"]
        except Exception:
            pass  # unreadable cache -> rescan
    markers = _walk_markers()
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(MARKER_CACHE, "w", encoding="utf-8") as f:
        json.dump({"scanned_epoch": time.time(),
                   "scanned": time.strftime("%Y-%m-%d %H:%M:%S"),
                   "markers": markers}, f, indent=1)
    return markers


# ---------- change-relevance filter (a .project NEVER means auto-republish) ----------

_NOISE_BASENAMES = {".DS_Store", ".gitignore", "desktop.ini", "Thumbs.db"}
_NOISE_PARTS = {".git", "__pycache__", ".venv", "node_modules", ".pytest_cache",
                "target", ".save_and_ship", ".project", ".deify"}
_NOISE_SUFFIXES = (".pyc", ".pyo", ".log", ".tmp", ".swp", ".bak", ".lock")


def is_relevant_change(path):
    """True if a changed path plausibly touches shipped-artifact content.
    Local noise (OS droppings, caches, VCS internals, the .project marker itself,
    /sas bookkeeping) must never open the ripple gate — otherwise refreshing a
    marker would trigger the very wave the marker exists to gate."""
    parts = path.split(os.sep)
    if any(p in _NOISE_PARTS for p in parts):
        return False
    base = os.path.basename(path)
    if base in _NOISE_BASENAMES or base.endswith(_NOISE_SUFFIXES):
        return False
    return True


# ---------- graph build ----------

def add_edge(edges, src, dst, flag):
    if src == dst or not src or not dst:
        return
    key = (src, dst)
    edges.setdefault(key, set()).add(flag)


def scan():
    nodes, edges = {}, {}

    # 1) registry: one node per creation; published = publish==published
    with open(os.path.join(CREATIONS, "index.json"), encoding="utf-8") as f:
        idx = json.load(f)
    for c in idx["creations"]:
        nodes[c["slug"]] = {
            "kind": c["kind"], "published": c["publish"] == "published",
            "publish": c["publish"], "repo": c.get("repo"),
            "location": c.get("location") or "",
        }

    slug_set = set(nodes)

    # 2) live skills dir: aliases (SKILL.md symlink -> canonical dir) and
    #    canonical-into-repo symlinks
    if os.path.isdir(SKILLS):
        for name in sorted(os.listdir(SKILLS)):
            sk = os.path.join(SKILLS, name, "SKILL.md")
            if not os.path.exists(sk):
                continue
            nodes.setdefault(name, {"kind": "skill", "published": False,
                                    "publish": "n/a", "repo": None,
                                    "location": f"~/.claude/skills/{name}/"})
            if os.path.islink(sk):
                target = os.path.realpath(sk)
                m = re.match(re.escape(SKILLS) + r"/([^/]+)/SKILL\.md$", target)
                if m and m.group(1) != name:
                    add_edge(edges, name, m.group(1), "alias")
                elif target.startswith(CREATIONS):
                    # skills-dir entry tracking a repo checkout (e.g. shipit)
                    rel = os.path.relpath(target, CREATIONS).split(os.sep)[0]
                    owner = next((s for s in slug_set
                                  if nodes[s].get("location", "").replace("~", HOME).rstrip("/").endswith(rel)), None)
                    add_edge(edges, name, owner or f"~/Creations/{rel}", "symlink-canonical")

    # 3) vault copies: Creations/Skills/<name>/.provenance.json -> live skill
    if os.path.isdir(VAULT):
        for root, dirs, files in os.walk(VAULT):
            if ".provenance.json" in files:
                vname = "Skills/" + os.path.relpath(root, VAULT)
                try:
                    prov = json.load(open(os.path.join(root, ".provenance.json"), encoding="utf-8"))
                    src = prov.get("source") or prov.get("source_dir") or ""
                except Exception:
                    src = ""
                m = re.search(r"\.claude/skills/([^/]+)", str(src))
                canonical = m.group(1) if m else os.path.basename(root)
                nodes.setdefault(vname, {"kind": "vault-copy", "published": False,
                                         "publish": "n/a", "repo": None,
                                         "location": f"~/Creations/{vname}/"})
                add_edge(edges, vname, canonical, "vault-copy")
                dirs[:] = []  # don't descend past a synced skill root

    # 4) /sas snapshots: manifest sources -> snapshot node
    for entry in sorted(os.listdir(CREATIONS)):
        man = os.path.join(CREATIONS, entry, ".save_and_ship", "manifest.json")
        if os.path.isfile(man):
            snap = entry
            nodes.setdefault(snap, {"kind": "snapshot", "published": False,
                                    "publish": "n/a", "repo": None,
                                    "location": f"~/Creations/{entry}/"})
            try:
                mj = json.load(open(man, encoding="utf-8"))
            except Exception:
                continue
            for s in mj.get("skills_saved", []):
                target = s.split()[0]
                add_edge(edges, snap, target, "snapshot")

    # 5) doc-mentions: /name in one skill's SKILL.md pointing at another node
    skill_nodes = [n for n in nodes if os.path.isfile(os.path.join(SKILLS, n, "SKILL.md"))]
    names = sorted(set(skill_nodes) | slug_set, key=len, reverse=True)
    pat = re.compile(r"/(" + "|".join(re.escape(n) for n in names if re.match(r"^[a-z0-9_-]+$", n)) + r")\b")
    for n in skill_nodes:
        try:
            text = open(os.path.join(SKILLS, n, "SKILL.md"), encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        for m in set(pat.findall(text)):
            if m != n:
                add_edge(edges, n, m, "doc-mention")

    # 6) declared edges from .project refs-out ("target:flag target2:flag2")
    for slug, meta in list(nodes.items()):
        loc = meta.get("location", "")
        root = re.sub(r"\s*\(.*$", "", loc).strip()  # strip "(alias ...)" annotations
        if not root:
            continue
        pm = read_project_marker(root)
        if pm:
            meta["project_marker"] = pm["path"]
            for ref in pm["meta"].get("refs-out", "").split():
                t, _, fl = ref.partition(":")
                add_edge(edges, slug, t, fl or "declared")

    graph = {
        "scanned": time.strftime("%Y-%m-%d %H:%M:%S"),
        "nodes": nodes,
        "edges": [{"src": s, "dst": d, "flags": sorted(fl)} for (s, d), fl in sorted(edges.items())],
    }
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(CACHE, "w", encoding="utf-8") as f:
        json.dump(graph, f, indent=1, ensure_ascii=False)
    return graph


def load():
    if not os.path.isfile(CACHE):
        return scan()
    return json.load(open(CACHE, encoding="utf-8"))


# ---------- queries (all cycle-safe: visited sets) ----------

def reverse_adj(graph):
    radj = {}
    for e in graph["edges"]:
        radj.setdefault(e["dst"], []).append((e["src"], e["flags"]))
    return radj


def affected(graph, roots):
    """BFS the reverse edges from the changed nodes. Visited set makes any
    loop (mutual refs, cycles through vault/snapshot/doc edges) terminate."""
    radj = reverse_adj(graph)
    seen, out, frontier = set(roots), [], [(r, 0, []) for r in roots]
    while frontier:
        node, hop, via = frontier.pop(0)
        if hop > 0:
            info = graph["nodes"].get(node, {})
            out.append({"node": node, "hops": hop, "via": via,
                        "published": bool(info.get("published")),
                        "action": "REPUBLISH" if info.get("published") else "update-refs"})
        for src, flags in radj.get(node, []):
            if src not in seen:
                seen.add(src)
                frontier.append((src, hop + 1, flags))
    return out


def cmd_affected(args):
    graph = load()
    roots = [a for a in args if not a.startswith("-")]
    missing = [r for r in roots if r not in graph["nodes"]]
    if missing:
        print(f"unknown node(s): {missing} — run `scan` or check the name", file=sys.stderr)
        sys.exit(2)
    rows = affected(graph, roots)
    if not rows:
        print(f"{roots}: no dependents — ripple stops here.")
        return
    pub = [r for r in rows if r["published"]]
    print(f"ripple from {roots}: {len(rows)} affected, {len(pub)} need REPUBLISH\n")
    for r in sorted(rows, key=lambda r: (r["hops"], -r["published"], r["node"])):
        mark = "🚢 REPUBLISH " if r["published"] else "   update    "
        print(f"  {mark} {r['node']}  (hop {r['hops']}, via {','.join(r['via'])})")


def cmd_check(paths):
    """Map changed paths -> owning nodes (by location prefix) -> ripple.
    Relevance-gated: noise paths never open the gate, and REPUBLISH always means
    STAGED-for-one-confirmation — presence of .project alone never auto-ships."""
    graph = load()
    noise = [p for p in paths if not is_relevant_change(p)]
    paths = [p for p in paths if is_relevant_change(p)]
    if noise:
        print(f"ignored as local noise (never opens the gate): {[os.path.basename(n) or n for n in noise]}")
    if not paths:
        print("no relevant changes — gate stays closed, no ripple.")
        return
    roots = set()
    for p in paths:
        rp = os.path.realpath(os.path.expanduser(p))
        for slug, meta in graph["nodes"].items():
            loc = re.sub(r"\s*\(.*$", "", meta.get("location", "")).strip()
            if loc and rp.startswith(os.path.realpath(os.path.expanduser(loc)).rstrip("/")):
                roots.add(slug)
    if not roots:
        print("no known node owns these paths — nothing shipped is affected (or add refs to a .project)")
        return
    print(f"dirty paths map to nodes: {sorted(roots)}")
    marked = [r for r in roots if graph["nodes"][r].get("project_marker") or graph["nodes"][r].get("published")]
    if marked:
        print(f"shipped-before (gate OPEN — ripple required): {sorted(marked)}")
        pub_roots = [r for r in marked if graph["nodes"][r].get("published")]
        for r in sorted(pub_roots):
            print(f"  🚢 REPUBLISH  {r}  (dirty + published — the root itself needs an update ship)")
    cmd_affected(sorted(roots))


def cmd_selftest():
    """Synthetic looped graph: A<->B cycle, diamond into D, self-ref C."""
    g = {"nodes": {n: {"published": n in ("A", "D")} for n in "ABCD"},
         "edges": [{"src": "A", "dst": "B", "flags": ["x"]},
                   {"src": "B", "dst": "A", "flags": ["x"]},   # cycle
                   {"src": "C", "dst": "A", "flags": ["y"]},
                   {"src": "C", "dst": "B", "flags": ["y"]},   # diamond
                   {"src": "D", "dst": "C", "flags": ["z"]},
                   {"src": "C", "dst": "C", "flags": ["self"]}]}  # self-loop (ignored by add rules, tolerated by BFS)
    rows = affected(g, ["A"])
    got = {r["node"] for r in rows}
    assert got == {"B", "C", "D"}, got
    assert all(r["hops"] <= 3 for r in rows)
    rows2 = affected(g, ["B"])          # enters the cycle from the other side
    assert {r["node"] for r in rows2} == {"A", "C", "D"}, rows2
    # relevance filter: noise never opens the gate, real content does
    assert not is_relevant_change("/x/proj/.DS_Store")
    assert not is_relevant_change("/x/proj/.project/status")
    assert not is_relevant_change("/x/proj/__pycache__/m.pyc")
    assert not is_relevant_change("/x/proj/.save_and_ship/manifest.json")
    assert is_relevant_change("/x/proj/SKILL.md")
    assert is_relevant_change("/x/proj/src/main.py")
    print("selftest OK — cycles, diamonds and self-loops all terminate with correct closures; noise filter correct")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "scan":
        g = scan()
        pub = sum(1 for n in g["nodes"].values() if n.get("published"))
        print(f"scanned: {len(g['nodes'])} nodes, {len(g['edges'])} edges, {pub} published → {CACHE}")
    elif cmd == "affected":
        cmd_affected(args)
    elif cmd == "show":
        g = load()
        n = args[0]
        for e in g["edges"]:
            if e["src"] == n:
                print(f"  {n} → {e['dst']}  [{','.join(e['flags'])}]")
            if e["dst"] == n:
                print(f"  {e['src']} → {n}  [{','.join(e['flags'])}]")
    elif cmd == "check":
        cmd_check(args)
    elif cmd == "markers":
        t0 = time.time()
        ms = project_markers(refresh="--refresh" in args)
        dt = (time.time() - t0) * 1000
        live = [m for m in ms if not m["vault_mirror"]]
        for m in live:
            print(f"  {m['form']:4s}  {m['path']}")
        mirrors = len(ms) - len(live)
        print(f"{len(live)} live markers (+{mirrors} vault mirrors) in {dt:.1f}ms")
    elif cmd == "ensure-project":
        slug = args[0]
        as_dir = "--dir" in args
        extra = [a for a in args[1:] if "=" in a]
        g = load()
        loc = re.sub(r"\s*\(.*$", "", g["nodes"].get(slug, {}).get("location", "")).strip()
        p = write_project_marker(loc or ".", slug, extra, as_dir)
        print(f"marker: {p}" if p else f"SKIPPED — no directory at {loc!r} for {slug}")
    elif cmd == "backfill":
        g = scan()
        made = 0
        for slug, meta in g["nodes"].items():
            if not meta.get("published"):
                continue
            loc = re.sub(r"\s*\(.*$", "", meta.get("location", "")).strip()
            root = os.path.expanduser(loc)
            if os.path.isdir(root):
                p = write_project_marker(loc, slug, [
                    f"status=published", f"repo={meta.get('repo') or ''}"])
                if p:
                    made += 1
                    print(f"  ✔ {slug}: {p}")
            else:
                print(f"  ⚠ {slug}: location is not a directory ({loc}) — marker skipped, publish state still tracked via registry")
        print(f"backfill: {made} .project markers ensured")
        scan()  # refresh cache so declared refs are picked up
    elif cmd == "selftest":
        cmd_selftest()
    else:
        print(f"unknown command {cmd!r}\n{__doc__}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
