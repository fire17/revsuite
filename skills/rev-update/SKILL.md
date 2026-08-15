---
name: rev-update
description: THE REV SUITE CHANGED — re-read and re-ACTIVATE the rev skills from disk (never from memory/context, which may be stale), see what the new guidelines expect of you, change your behavior to match immediately, propagate the same to every agent you manage, and report the delta. Deliberately carries NO copy of the rules themselves, so it never goes stale when the rev system changes. Send it to any agent — a HIGHREV orchestrator, a teammate, an ordinary chat, or a whole fleet. Use when the user types /rev-update or /rev-sync, says "the rev skill changed", "re-read the rev rules", "resync the doctrine", or an observer tells an agent its guidelines are out of date.
argument-hint: "[optional: which skill changed / what to look for]"
---

# /rev-update — the rev suite changed, resync NOW

**Assume your copy is stale.** The rules moved after your context was built.
What you "know" about them may be the old version. Go to disk.

## 1. Re-read AND re-activate the whole suite

```bash
ls ~/.claude/skills/rev*/SKILL.md ~/.claude/skills/highest-rev/SKILL.md \
   ~/.claude/skills/workflow-model-guard/SKILL.md 2>/dev/null
```

Read every file that lists (the glob catches rev skills added since this one was
written), then **activate** the ones that apply to you — invoking binds you,
reading only informs you. Then re-resolve the user's preferences, which set the
suite's actual values and may have changed on their own:

```bash
python3 ~/.claude/scripts/rev-prefs.py     # add --profile <name> if one is in effect
``` If an argument named a specific skill or change, start
there, then still check the rest; these move together.

The files are the authority. Never answer from recollection, and never assume a
skill you loaded earlier this session is still current.

## 2. Work out what changed for YOU

Not "what do they say" — **"what do they now expect of me that I am not doing?"**
Read the new and edited lines as instructions addressed to you: your gear, your
parallelism, your models, your reporting, your housekeeping, whatever the suite
now covers.

## 3. Adopt immediately

- Everything you start from here on complies. No grace period, no "next round",
  never launch-then-fix.
- Anything already in flight is corrected at its next natural boundary — never
  kill work mid-landing to satisfy a document.
- Nothing already delivered is silently rewritten; if it no longer meets the
  bar, say so and propose the fix.
- **A standing order you were given still stands.** A resync re-reads rules; it
  does not cancel an instruction someone gave you. Keep it and say so.

## 4. Propagate

Send `/rev-update` to every agent you are responsible for — teammates and the
agents inside your workflows. Each does this same pass on itself. The suite
reaches every tier or it reaches none.

## 5. Report the delta

```
REV UPDATE — <agent/lane>
re-read + activated: <files, one line each on what changed>
now out of compliance on: <list, or "nothing">
changing right now: <concrete actions>
correcting at next boundary: <in-flight items + when>
standing orders still in effect: <e.g. a throttle, or "none">
propagated to: <agents, or "none — no reports">
```

Then do it. A resync that changes no behavior was not a resync.
