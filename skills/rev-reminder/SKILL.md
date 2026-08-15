---
name: rev-reminder
description: The rev GEARBOX for any agent, main or subagent. Bare "/rev" means REV UP — it asks "hows it going? is there a good reason you have less than 5 ultracode workflows open currently?", then revs up now and holds it high. "/rev up" is the same said explicitly. "/rev down" means slow to stock-agent linear pace — no new ultracode workflows, conserve tokens — and it PERSISTS until an explicit /rev up, suspending the floor-of-5 law meanwhile. Both directions propagate to every agent and workflow you manage, and an agent that throttled others must remember to send them the up when it receives one. Also takes TARGETS — "/rev up subagentA", "/rev down subagentB", or both in one message — where the named agents are the subject and you are the messenger, relaying the order without changing your own gear. Works with or without /highest-rev loaded — mid-chat, inside subagents, and as the nudge an observer sends a lagging or over-spending agent. Use on /rev, /rev up, /rev down, /rev-reminder, "rev check", "rev up", "slow down", "conserve tokens", "back to normal speed".
argument-hint: "[up | down] [agent names…] — bare /rev revs you up"
---

# /rev-reminder — the rev check and the rev throttle

Read the argument first. **Bare `/rev` means REV UP** — answer the question
below, then rev up; the check exists to sharpen the action, never to replace
it. Works the same whether you are a main agent or a subagent.

| form | meaning |
|---|---|
| `/rev` (bare) | **REV UP yourself** (+ answer the check, + propagate down) |
| `/rev up` | same, said explicitly |
| `/rev down` | **THROTTLE DOWN** — stock linear pace, persists until an explicit up |
| `/rev up <agent…>` | relay UP to those agents — not to yourself |
| `/rev down <agent…>` | relay DOWN to those agents — keep them on your roster |
| mixed, e.g. `/rev up A and /rev down B` | execute each independently, in order, and report each |

**Targeted forms — the routing rules.** When agents are named, they are the
subject and you are the messenger: send each one the matching `/rev up` or
`/rev down` (SendMessage, or your harness's channel), do NOT change your own
gear unless you are named too, and report exactly who you reached. Resolve
names against your own roster / `ListAgents`; if a name is ambiguous, unknown,
or belongs to a session you do not command, say so and ask — never guess a
target, and never silently apply a targeted order to yourself. Any agent you
send DOWN goes on your throttle roster; any you send UP comes off it.

> **hows it going ? is there a good reason you have less than 5 ultracode
> workflows open currently ?**

Answer that first, honestly, before anything else. Then act — on a bare `/rev`
the action is: rev up now.

## First: load the user's preferences (they are the authority)

```bash
python3 ~/.claude/scripts/rev-prefs.py        # add --profile <name> if one was asked for
```

Every number, model, and toggle below comes from `~/.claude/rev-prefs.toml` via
that resolver — the band, the fleet size, the models per tier. **The values
printed in this skill are only the current defaults for reference; the file is
the truth**, and it may have changed since. Read it, then use what it says.
Anything the user says live in the conversation outranks the file — follow the
live instruction and say that you are.

## The band (fire17's SPAWN LAW, verbatim)

```
for every parralel tmux highrev subagent with ultracodes you spawn make to tell it to work until its utterly perfect! SUPER IMPORTATNT: If it has less than 5 workflows at any given moment it must rev up (up to 10 ongoing workflows at all times in parrallel, no less than 5). 
```

**Floor · ceiling · live, right now, per agent** — the numbers are
`workflow_floor` and `workflow_ceiling` from the prefs (defaults 5 and 10).
Under the floor = rev up THIS cycle, not next. Over the ceiling = hold new
launches and let the band drain; stacking past it to look busy is the mirror
defect.

**"Live" means running.** Queued-but-not-started, finished, and
about-to-be-authored do not count. Count what is actually executing.

**And close what is done — without being asked.** fire17's standing order,
verbatim: *"close all subagents that are done (and remember to always do this
so i dont have to keep asking you)"*. A done subagent still open is a defect
in the same check as an empty band: report `done-but-open: <n>` and make it 0
now. A finished agent left running is not rev — it is drag.

**Rev is never an excuse to cheapen a tier.** If you are a HIGHREV teammate,
every agent inside your workflows uses the prefs' `tier3_model` — explicitly
written and verified to have resolved to that model after launch — and never
anything in `forbidden_models`. More workflows, not weaker ones.

## If you are under the floor without a good reason — rev up NOW

1. **Split what you are already doing.** Any lane with independent parts is
   several workflows, not one — decompose by outcome, not by phase.
2. **Launch the work you were saving for later.** Research, verification,
   hardening, docs, and edge-case sweeps parallelize immediately and rarely
   collide.
3. **Use worktrees for anything that mutates files in parallel** — disjoint
   file ownership per lane, commit a checkpoint before fanning out (worktrees
   only carry committed files), merge back as soon as a lane lands.
4. **Keep asking: what can we do to rev up? TO THE MAX!** More simultaneous
   ultracode dynamic workflows. STEP ON IT.
5. If you manage other agents, the same law is theirs — remind each to gauge
   its OWN workflows and hold its own band. Every agent manages the agents it
   is responsible for.

## Legitimate reasons to be under the floor — say them, don't assume them

Being under 5 is fine in these cases, but only if you **state which one, in one
line, unprompted**:

- **Winding down.** The work is genuinely almost finished — fewer than 5
  independent units remain. Say what is left and the ETA.
- **Blocked on an exclusive resource.** One-at-a-time GPU/device/port/daemon or
  a single-writer file; you hold or await the token. Waiting on a declared
  token is NOT idleness — but unused capacity elsewhere while you wait still is.
- **Capacity or rate limits.** 5h/7d limits or machine headroom will not carry
  more; name the number you read.
- **Spin-down / mode ended.** The fleet is draining on purpose.
- **Throttled down.** A `/rev down` is in effect — say since when. This one
  needs no further justification; it is an order, not a shortfall.
- **Nothing left that parallelizes honestly.** The remaining work is one
  strictly serial chain. Say why it cannot be split — this is the rarest one
  and the easiest to use as an excuse, so justify it concretely.

An unstated reason is not a reason. "I was about to" is not a reason.

## `/rev` / `/rev up` — more parallelism, now and onward

1. **Spawn now, not next cycle.** Launch more ultracode workflows immediately —
   go to the top of the band (10), not the floor.
2. **Hold it high in every following step.** This is not a one-shot burst; the
   raised rev is your new default until told otherwise. Re-check it each cycle.
3. **If a `/rev down` was in effect, it is CANCELLED** — the floor-of-5 law and
   the full band are back in force this moment.
4. **Propagate down.** Every agent you manage gets `/rev up` too, and each of
   them does all of the above. Clear your throttle roster as you send it.
5. Answer with the block below plus one line: `throttle: UP — <n> agents told`.

## `/rev down` — stock linear pace, until told otherwise

For conserving tokens, stretching a limit window, freeing the machine, or any
reason the user does not have to explain.

1. **Open no new ultracode workflows.** None. Work like a stock agent: one
   thing at a time, linear, no fan-out.
2. **Do not kill what is already running** — let in-flight workflows and lanes
   land, then simply do not replace them. Never destroy work to slow down.
3. **The floor of 5 is SUSPENDED** while down. Being under the band is correct
   here, and it is not a rev defect — this is the one state where a low count
   needs no justification. (Everything else still binds: done subagents still
   get closed, reports still get written, honesty still applies.)
4. **It PERSISTS.** Stay down across cycles, across resyncs, across new tasks —
   until an explicit `/rev up`. A doctrine re-read (`/rev-update`) does NOT
   cancel a throttle. Neither does finishing a task and starting another.
5. **Propagate down, and REMEMBER WHO.** Tell every agent you manage — and
   their workflows — to slow down the same way, and keep a throttle roster of
   exactly who you told. When you later receive `/rev up`, you owe every one of
   them the up message. An agent left throttled after the fleet revved is your
   failure, not theirs.
6. Answer with the block below plus one line: `throttle: DOWN — <n> agents told,
   roster kept`.

## Reply in this shape (one block, always)

```
REV CHECK — <agent/lane>
order: <what you were sent, verbatim> → <self | relayed to: A, B>
throttle: UP | DOWN (since <when>) | none | unchanged (targeted order, not for me)
live workflows: <n> (band 5–10)   done-but-open subagents: <n> (must be 0)
verdict: IN BAND | UNDER FLOOR — revving now | UNDER FLOOR — legitimate: <which reason> | THROTTLED DOWN — floor suspended
what is running: <one line each>
action: <what you are launching right now, or what remains + ETA; plus who you are closing>
```

Then do the thing you just said. The report is not the work.

> Guidelines changed since you loaded them? Run `/rev-update` (alias
> `/rev-sync`) — it re-reads the rev skills from disk and makes you adopt the
> new rules immediately.
>
> Sprawled across many workflows and lanes when one focused push would do?
> Run `/rev-collapse` (`/collapse`) — harvest everything so nothing is wasted,
> fold it all into ONE workflow, close the rest, then max rev on the next thing.
>
> Stuck, hedging, or hearing yourself make excuses? Run `/affirm`
> (`/rev-affirm`) — self-belief plus a mandatory new angle, so the next attempt
> can fail differently. Widening the band is the fuel: divergent attempts in
> parallel beat sequential retries of the same idea.
