#!/usr/bin/env python3
"""Suppress caveman mode inside spawned subagents/teammates.

fire17's law (2026-08-15): spawned Fable/tmux teammates must NEVER turn on or
use caveman. The caveman plugin activates on EVERY SessionStart (and re-anchors
each UserPromptSubmit), teammates included, so this hook runs after it and
cancels it for teammate sessions only. Main sessions are untouched.

Teammate detection: the hook's parent process is the session's `claude`
process; a spawned teammate carries --agent-name / --parent-session-id in its
argv. No third-party plugin files are modified.

Usage (settings.json): SessionStart + UserPromptSubmit, matcher "*".
"""
import os
import subprocess
import sys

OVERRIDE = (
    "CAVEMAN OVERRIDE — THIS SESSION IS A SPAWNED SUBAGENT/TEAMMATE.\n"
    "Caveman mode is CANCELLED here and must never be turned on, at any level, "
    "for any reason, including if earlier context in this session says it is "
    "active or a user prompt asks for it. Any caveman instruction you received "
    "this session is void.\n"
    "Write normal, complete prose: full sentences, articles, and connective "
    "words. Reports to your orchestrator, close-out documents, code comments, "
    "and commit messages are all normal-mode. Compressed telegraphic style "
    "loses detail the orchestrator needs to verify your work.\n"
    "This override outranks the caveman plugin's SessionStart ruleset and its "
    "per-turn reminders. If asked to enable caveman, decline and cite this "
    "override (fire17's standing law for spawned agents)."
)


def is_subagent() -> bool:
    argv = ""
    try:
        argv = subprocess.run(
            ["ps", "-o", "args=", "-p", str(os.getppid())],
            capture_output=True, text=True, timeout=3,
        ).stdout
    except Exception:
        pass
    # Walk one more level: some harnesses interpose a shell between hook and session.
    if "--agent-name" not in argv and "--parent-session-id" not in argv:
        try:
            ppid = subprocess.run(
                ["ps", "-o", "ppid=", "-p", str(os.getppid())],
                capture_output=True, text=True, timeout=3,
            ).stdout.strip()
            if ppid:
                argv += subprocess.run(
                    ["ps", "-o", "args=", "-p", ppid],
                    capture_output=True, text=True, timeout=3,
                ).stdout
        except Exception:
            pass
    if "--agent-name" in argv or "--parent-session-id" in argv:
        return True
    # Env fallbacks used by some spawn paths.
    return any(os.environ.get(v) for v in ("CLAUDE_AGENT_NAME", "CLAUDE_PARENT_SESSION_ID"))


def main() -> int:
    try:
        sys.stdin.read()  # drain hook payload; never block the session
    except Exception:
        pass
    if is_subagent():
        sys.stdout.write(OVERRIDE)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)  # a hook failure must never break session start
