#!/bin/bash
# RevSuite installer — batteries included, works out of the box.
#
# Installs: the rev skills (+ their aliases and functional dependencies), the
# preferences resolver, the preferences file (only if you don't have one), and
# the no-caveman-for-subagents hook (registered in settings.json idempotently).
#
# Never clobbers your work: existing skills are skipped unless --force, and an
# existing ~/.claude/rev-prefs.toml is NEVER overwritten (it holds your prefs).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
DEST="$CLAUDE_DIR/skills"
FORCE="${1:-}"
mkdir -p "$DEST" "$CLAUDE_DIR/scripts" "$CLAUDE_DIR/hooks"

installed=0 skipped=0 skipped_names=""
for d in "$HERE"/skills/*/; do
  name="$(basename "$d")"
  if [ -e "$DEST/$name" ] && [ "$FORCE" != "--force" ]; then
    skipped=$((skipped + 1)); skipped_names="$skipped_names $name"; continue
  fi
  rm -rf "${DEST:?}/$name"
  cp -R "$d" "$DEST/$name"   # -R keeps the relative SKILL.md symlinks aliases need
  installed=$((installed + 1))
done
echo "skills: $installed installed, $skipped skipped (already present, may be STALE)"
[ -n "$skipped_names" ] && echo "  skipped:${skipped_names}"

# preferences resolver (always refreshed — it is code, not config)
cp "$HERE/scripts/rev-prefs.py" "$CLAUDE_DIR/scripts/rev-prefs.py"
echo "resolver: $CLAUDE_DIR/scripts/rev-prefs.py"

# preferences file — YOUR settings; never overwritten
if [ -e "$CLAUDE_DIR/rev-prefs.toml" ]; then
  echo "prefs:    kept existing $CLAUDE_DIR/rev-prefs.toml (not touched)"
else
  cp "$HERE/prefs/rev-prefs.toml" "$CLAUDE_DIR/rev-prefs.toml"
  echo "prefs:    installed default $CLAUDE_DIR/rev-prefs.toml"
fi

# no-caveman-for-subagents hook + idempotent settings.json registration
cp "$HERE/hooks/no-caveman-for-subagents.py" "$CLAUDE_DIR/hooks/no-caveman-for-subagents.py"
python3 - "$CLAUDE_DIR" <<'PY'
import json, os, shutil, sys, time
claude_dir = sys.argv[1]
settings = os.path.join(claude_dir, "settings.json")
cmd = f"python3 {os.path.join(claude_dir, 'hooks', 'no-caveman-for-subagents.py')}"
entry = {"matcher": "*", "hooks": [{"type": "command", "command": cmd, "timeout": 10}]}
data = {}
if os.path.exists(settings):
    shutil.copy(settings, f"{settings}.bak-{int(time.time())}")
    try:
        with open(settings) as fh:
            data = json.load(fh)
    except Exception as exc:
        print(f"hook:     settings.json unreadable ({exc}) — register it manually")
        raise SystemExit(0)
hooks = data.setdefault("hooks", {})
added = []
for event in ("SessionStart", "UserPromptSubmit"):
    arr = hooks.setdefault(event, [])
    if any("no-caveman-for-subagents" in json.dumps(x) for x in arr):
        continue
    arr.append(json.loads(json.dumps(entry)))  # appended LAST: runs after the caveman plugin
    added.append(event)
with open(settings, "w") as fh:
    json.dump(data, fh, indent=2)
    fh.write("\n")
print(f"hook:     registered on {', '.join(added)}" if added else "hook:     already registered")
PY

echo
echo "verifying preferences resolve:"
python3 "$CLAUDE_DIR/scripts/rev-prefs.py" || echo "  (resolver failed — check python3 >= 3.11 for tomllib)"
cat <<'EOF'

Done. Try it:
  /rev              rev this agent up (and answer the rev check)
  /rev down         throttle to stock linear pace until an explicit /rev up
  /rev-update       re-read + re-activate the suite after you change anything
  /highest-rev      the full HIGHREV fleet mode
Edit your preferences any time:  ~/.claude/rev-prefs.toml

Optional, for the full quality stack /highest-bar activates (impeccable,
master_engineering + its book payload, ladder-abstraction, and friends):
  git clone https://github.com/fire17/highest-bar && ./highest-bar/install.sh
EOF
