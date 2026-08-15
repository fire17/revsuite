---
name: master_engineering
description: The MASTER ENGINEERING doctrine — every principle from The Senior's book ("Master Engineering — Principles for Junior, Senior & Unicorn Developers, Designers, Architects, and Small-to-Enterprise High-End Engineers and Managers", ~/Creations/Lively/the_senior/MASTER_ENGINEERING.md) compressed into quick reminders, each with an exact page + section reference into the book for expansion. Load this whenever engineering work of ANY kind begins or gets reviewed — building, designing, planning, architecting, coding, testing, shipping, operating, debugging an incident, adopting a library/dependency, writing a design doc, delegating work to people or AI agents, or judging "is this done?" — or when the user types /master_engineering or /sol, mentions "the book", "master engineering", "The Senior", "Sol's principles", asks "how should I approach this properly", wants engineering best practices, or a junior/newcomer needs to think like a master engineer. Also load it BEFORE starting any non-trivial task to use as a design lens, and at the end as acceptance criteria. When a specific topic is given as an argument, focus that domain and follow its references into the book for the deep dive.
argument-hint: "[topic or question — e.g. shipping, delegation, github, testing, planning]"
---

# 🏛 /master_engineering — the pocket edition of the book

This skill is the **field kit** distilled from the ~34-page book **MASTER ENGINEERING** by Sol Adler ("The Senior" — 60 years, 20 companies). Every principle below is a one-line reminder with an exact reference `[p.N §X.Y]` into the book. The reminders are enough to *act* like a master; the references are the smart index for when you need the full reasoning, the war story, or the method in detail.

**The book (level 2 depth):** `/Users/magic/Creations/Lively/the_senior/MASTER_ENGINEERING.md`
- Sections are headed `## <chapter>.<section>` (e.g. `## 5.2`) and `## <letter>.<n>` for appendices (e.g. `## C.3`); pages are marked `*· page N ·*`.
- To expand any reference: `Read` the book and jump by section heading — e.g. for `[p.9 §5.2]` grep/search `## 5.2`. One command, exact landing.

**The binder (level 3 depth):** twenty per-company volumes (`master_engineering_principles_of_<company>.md`, same folder, indexed in its `README.md`) — the raw source doctrine per company (SpaceX, Jane Street, Stripe, Google, …) when you want a whole culture's method, not one principle.

## How to apply this skill

1. **Before the task** — scan the section matching your lifecycle stage below; let it shape the plan (design lens).
2. **During** — when a decision matches a reminder, follow its reference and read that book section before deciding (it's one Read; the book section carries the *why* and the failure story that motivates it).
3. **After, before saying "done"** — run the matching checklist at the bottom as acceptance criteria.
4. **With an argument** (e.g. `/master_engineering shipping`) — jump to that domain's block, read its book sections, and answer/act from them, citing `[p.N §X.Y]` so the human can follow.
5. **When advising a junior** — give the reminder AND the reference; the pointer teaches them the book exists and where their answer lives.

---

## ⚖️ THE TEN LAWS — memorize these [p.33]

1. **Question the requirement before the solution** — it has a name attached; argue with the name.
2. **Delete before you optimize** — question → delete → simplify → accelerate → automate, in order.
3. **Write it down** — the document is where the decision happens; the name is the design.
4. **Make illegal states unrepresentable** — constraints in the construction, not the inspection.
5. **Assume failure and design its container** — hope is not architecture.
6. **The interface is the product** — promises in decades; implementations rented by the quarter.
7. **Test like you fly** — any difference from production measures your hopes.
8. **Ship on a dial, never a switch** — flags, ramps, rehearsed rollbacks; config is code.
9. **Spec outcomes, delegate the how, verify by sampling** — trust is calibrated evidence.
10. **Context scales; control doesn't** — mechanisms over intentions; blameless truth at speed.

---

## 🧠 FOUNDATIONS — the mind and the pen

**The Craftsman's Mind [p.4 Ch.1]**
- Requirements have *names* — go argue with the name; half are fossils the author would retract. `[p.4 §1.1]`
- The deleted part has no bugs, no latency, no meetings. Delete before optimizing, always in the five-step order. `[p.4 §1.2]`
- Taste is trainable: collect the ten best pieces of engineering you've met and know *why* each is good. `[p.4 §1.3]`
- Never claim success you didn't observe. "Tests pass" ≠ "it works" — run the real thing. `[p.4 §1.4]`

**Writing Is Thinking [p.5 Ch.2]**
- Non-trivial work gets a design note BEFORE code; the rejected-alternatives section is the valuable part. `[p.5 §2.1]`
- Press-release test: write the announcement first — boring announcement = boring feature. `[p.5 §2.2]`
- Naming is design: a guessable API means the work was done; an awkward name means the concept is wrong. `[p.5 §2.3]`
- If it changed what you built, it lives in a findable document, not chat scrollback. `[p.5 §2.4]`

## 🔍 UNDERSTAND & PLAN

**Understand Before You Build [p.7 Ch.3]**
- Watch users' hands, not their documents; the workaround IS the requirement. Read a system before changing it. `[p.7 §3.1]`
- Prototype the scariest assumption first — ugly, timeboxed, disposable. You're *buying information*. `[p.7 §3.2]`
- Data is always dirtier than claimed — profile before trusting; instrument before wondering. `[p.7 §3.3]`
- Compute the speed-of-light ceiling BEFORE optimizing; know the size of the prize. `[p.7 §3.4]`
- Search for prior art before building anything — someone already built most of what you need. `[p.7 §3.5]` → full method in App. C below.

**Plan Like a Gambler, Decide Like a Surgeon [p.8 Ch.4]**
- Sort decisions by reversibility: two-way doors fast with 70% info; one-way doors slow and paranoid. `[p.8 §4.1]`
- State odds + downside in numbers; write kill criteria BEFORE starting, while calm. `[p.8 §4.2]`
- Under pressure cut SCOPE — never quality (loan-shark debt), never dates (trust erosion). The moat gets years; features get weeks. `[p.8 §4.3]`
- Retire the scariest risk in week one — a demo built before the risk is retired demos an imaginary product. `[p.8 §4.4]`
- Plan for 10x on paper, build for 3x in code. `[p.8 §4.5]`

## 🏗 DESIGN & ARCHITECTURE [pp.9–10 Ch.5]

- Make illegal states unrepresentable; parse, don't validate — cross the boundary once, carry proof in the structure. `[p.9 §5.1]`
- Design the failure before the feature: every remote call gets timeout + fallback + circuit breaker; every design doc states its blast radius and degradation ladder. `[p.9 §5.2]`
- Interfaces are decades, implementations are quarters: every mutation idempotent, version from day one, errors designed like features. `[p.9 §5.3]`
- ~2 innovation tokens per project — spend on the moat; buy everything else boring. `[p.9 §5.4]`
- Trade machine time for human correctness; when a bug class recurs, redesign the *primitive*. `[p.9 §5.5]`
- Data outlives code: raw lands immutable, snapshots not overwrites, provenance on every derived fact, transactions wherever two writers meet. Ontology mistakes cost years > schema months > code days. `[p.10 §5.6]`
- Design for deletion: the migration is done when the old path is GONE. `[p.10 §5.7]`

## ⌨️ DEVELOP [p.11 Ch.6]

- Small revertible diffs, landed daily — velocity is integration frequency, not typing speed. `[p.11 §6.1]`
- Boring-and-obviously-correct beats clever-and-probably-correct; pride in cleverness is a code smell. `[p.11 §6.2]`
- Push every checkable property into a machine check; in review always ask "what construction makes this bug impossible?" `[p.11 §6.3]`
- Instrument as you build; log *decisions* not events; answer the 2am question in your logs now. `[p.11 §6.4]`
- **The five-minute rules** `[p.11 §6.5]`: UTC always · money = integers in minor units · name the units · retries idempotent + backoff + jitter · every queue gets a depth alarm · delete dead code immediately · clocks lie.

## ✅ VERIFY [p.12 Ch.7]

- Know your rung on the hierarchy of evidence (compiles → unit → integration → staging → 1% prod → a year of prod); never claim a rung you haven't reached. `[p.12 §7.1]`
- Property tests find what your imagination filtered; fuzz every parser; differential-test replacements against the old oracle. `[p.12 §7.2]`
- Untested fallbacks are fiction; an unrestored backup is a hypothesis; drill the kill switches. `[p.12 §7.3]`
- Monsters (real-world pathologies) live in CI forever; perf budgets are tests; flaky tests get product-bug seriousness. `[p.12 §7.4]`

## 🚀 SHIP [p.13 Ch.8]

- Everything behind a flag; dark launch; ramp 1%→5%→25% along the axis of whose-work-gets-damaged. `[p.13 §8.1]`
- The rollback is the license to ship: rehearsed, faster than a human notices; abort criteria written while calm. `[p.13 §8.2]`
- Config is code — same review/canary/rollback pipeline, especially the "trivial" change; no global config on Fridays. `[p.13 §8.3]`
- The launch begins the learning; docs + changelog + migration ship WITH the feature or it's leaked, not released. `[p.13 §8.4]`

## 🛠 OPERATE & MAINTAIN [p.14 Ch.9]

- Define "working" from the user's side (SLI), alert on burn-rate — never on machine moods; every alert actionable + runbook-linked. `[p.14 §9.1]`
- Error budget: reliability as an agreed number — under budget ship, over budget harden. The velocity war becomes arithmetic. `[p.14 §9.2]`
- Blameless is epistemology: ask what the SYSTEM permitted; action items are mechanisms, never "be careful"; repeat incident = the real failure. `[p.14 §9.3]`
- Toil is a bug (twice manually = automation ticket); if it hurts, do it more often until it stops hurting. `[p.14 §9.4]`
- Delete the undefended service; deprecate only with a paved path out; guard the weekly ops review with your life. `[p.14 §9.5]`

## 👥 PEOPLE, DELEGATION, MANAGEMENT

**Working With Others [p.16 Ch.10]**
- Review propagates taste (that's the product; bugs are byproduct); review the code, never the coder; read the diff twice — once for what it does, once for what it forgets. `[p.16 §10.1]`
- Own outcomes, not tickets; cross any boundary to fix a real thing; you build it, you run it. `[p.16 §10.2]`
- Code wins arguments — debate >1 hour? build both. Speak in measurements; disagree-and-commit, recorded. `[p.16 §10.3]`
- Bad-news speed is the health metric of a culture; reward the bearer, every time. `[p.16 §10.4]`

**Delegation & Leverage — humans AND AI agents [pp.17–18 Ch.11]**
- Delegation fails at the SPEC, not the worker. The five disciplines: outcome-spec with acceptance test · boundary contract (explicit in/out, nothing implied) · the escalation clause ("stuck or wrong → say so and STOP") · verify independently by sampling, calibrated to track record · match task tier to worker tier. `[p.17 §11.1]`
- Economics of the hour: whose hour, what does it cost, is there a cheaper hour of acceptable quality? The senior's best hour writes the spec that lands a hundred cheaper hours. `[p.17 §11.2]`
- Machines obey the same five disciplines — but the spec is MORE load-bearing (models fill gaps with confidence, not common sense) and verification must be independent of self-report ("it works" is a claim, not evidence). `[p.18 §11.3]`
- Build leverage in order: tools → documents → people/machines. Write the tribal knowledge down, THEN hand off. `[p.18 §11.4]`

**Managing & Leading [p.19 Ch.12]**
- Context scales, control doesn't; every approval gate confesses failed context; the org chart is an architecture — design it. `[p.19 §12.1]`
- Mechanisms over intentions: find the chronic argument, make it a number (the error budget is the masterpiece); paved roads beat mandates. `[p.19 §12.2]`
- The manager's whole job: set context · write it down · remove obstacles. Everything else is theater. Protect the boring mechanisms. `[p.19 §12.3]`

## 📈 CAREER & SELF

- **Altitudes [p.21 Ch.13]**: Junior = reps, whole-and-verified, escalate early (trap: speed ≠ velocity). Senior = outcomes through design/specs/teaching (trap: hoarding the interesting work). Unicorn = primitive rethinks with conservative everything-else (revolutionaries with boring infrastructure win).
- **Time/Cost/Energy [p.22 Ch.14]**: head for thinking, storage for storing · protect making-blocks; batch meetings · know what things cost (multiply meeting salaries; wince) · peak hours on peak problems · sustainable pace outperforms heroics.
- **The Long Game [p.23 Ch.15]**: rent technologies, own invariants · decision journal, update fast and cheerfully · reputation = people believe what you say (one inflated demo spends a decade) · teach to find what you can't defend · the muffin tin: curiosity WITH discipline.

## 🏆 THE BEST IN THE ROOM — mastery, proven [pp.24–25 Ch.16]

- Masters are made of **compounding loops**, not talent: decision journal · collected excellence · postmortems-as-curriculum · teaching. Learning rate is the only durable advantage — the era erodes every other one. `[p.24 §16.1]`
- Mastery keeps **receipts a skeptic could audit**: systems still running · the calibration log (you said 80% — were you right 80%?) · zero *repeat* incidents · yearly self-benchmarks against the frontier. Invite the disconfirming test of your own skill. `[p.24 §16.2]`
- Differentiate on the **whole loop** (be handed outcomes, not tasks) and **at the seams** between specialties — this era's widest seam is intelligence/operations. One deep moat + broad composability. `[p.25 §16.3]`
- Best ≠ smartest: the best engineer is the one whose presence **raises the room's expected value**. If you're reliably the smartest in the room, your learning rate is zero — change rooms. `[p.25 §16.4]`
- SOTA is a treadmill, not a title: run the triage funnel on *techniques* quarterly · rebuild one belief per quarter · learn the era's defining tool seriously · **measure your leverage over machine intelligence** — auditable multiplication is what "best of our era" provably looks like. `[p.25 §16.5]`

## 🔐 SECURITY & TRUST [pp.26–27 App.A]

- Threat-model at design time; assume adversarial input always; fuzz what parses strangers' bytes. `[p.26 §A.1]`
- Non-negotiables: secrets vaulted never in code · least privilege · memory-safe at hostile boundaries · fail-closed/fail-open decided on purpose · access control IN the data model. `[p.26 §A.2]`
- Privacy is per-data-class architecture (what may leave the machine, which tier may touch it). `[p.27 §A.3]`
- Verify trust with arithmetic: reconciliation, audit logs, canary credentials. `[p.27 §A.4]`

## 🎨 DESIGN / PRODUCT [p.28 App.B]

- The default is the decision; options are apologies. `[p.28 §B.1]`
- Watch hands, silently — every question asked aloud is a bug. `[p.28 §B.2]`
- Latency is emotion: <100ms = your hand, >1s = a form; optimistic UI. `[p.28 §B.3]`
- Prototype ten, then subtract until it breaks; progressive disclosure. `[p.28 §B.4]`
- Errors, empty states, and degraded states ARE the product. `[p.28 §B.5]`

## 🐙 GITHUB / PRIOR ART / DEPENDENCIES [pp.29–31 App.C]

- Prime directive: find-evaluate-compose before building; innovation tokens only on the unsolved. `[p.29 §C.1]`
- Search several angles: qualifiers (`pushed:>`, `stars:>`) · error-message-verbatim code search · the dependents graph · tastemakers' stars · awesome-lists + big-neighbor issues. `[p.29 §C.2]`
- **The triage funnel** — cheap gates before expensive: 30s gate (README/alive/LICENSE FIRST/provenance vs typosquats) → 5min gate (issue tracker = honest docs; maintainer latency to strangers; read the tests + one core file — debuggable at 2am?) → 30min gate (spike finalists on YOUR real data; sample data always works, which is what makes it a lie) → half-page decision note. `[p.30 §C.3]`
- Every dependency is a HIRE: interview → onboard (pin, lock, why-note, watch releases) → yearly re-review → succession plan. Vendor-vs-depend decided consciously. `[p.30 §C.4]`
- Supply chain is a trust boundary: install scripts, transitive deps, typosquats; new deps first run in CI under least privilege. `[p.30 §C.5]`
- Star with intent (your stars = a private pre-trusted search engine); issue-first development; read one great repo per quarter; never pay for the same search twice — write the decision note. `[p.31 §C.6]`
- Upstream your patches (a private fork is debt you carry forever); master the great bug report. `[p.31 §C.7]`

---

## 🗺 THE SMART INDEX — "I need…" → open the book here

| Situation | Go to | Why it's worth the read |
|---|---|---|
| Starting ANY non-trivial task | p.4 §1.1–1.2, p.7 §3.2, p.8 §4.2 | The question/delete/derisk/kill-criteria opening moves — an hour here saves the quarter |
| Told to build a feature | p.5 §2.1–2.2, p.7 Ch.3 | Design-note + press-release test + watching real users; kills wrong-product risk before code |
| Choosing a library, tool, or framework | pp.29–31 App.C | The complete funnel with per-gate kill criteria — an afternoon to a verified, documented choice |
| Writing a design doc | p.5 §2.1, p.9 §5.2, p.26 §A.1 | Alternatives-considered, blast-radius section, threat model — the three sections reviewers actually need |
| Designing a data model / schema | p.10 §5.6 | The cost hierarchy (ontology>schema>code) and the immutable/provenance/snapshot laws — cheapest insurance in the book |
| About to optimize something | p.7 §3.4, p.4 §1.2 | Speed-of-light first, delete first — most optimization is fiddling below an unchecked ceiling |
| A bug class keeps recurring | p.9 §5.5, p.11 §6.3 | The primitive-rethink move + make-it-impossible constructions; stop fixing instances |
| Preparing a release | p.13 Ch.8 + p.34 checklist | Ramp/rollback/abort-criteria method — the difference between calm shipping and brave shipping |
| Production incident NOW | p.34 "When it breaks", then p.14 §9.3 | Command structure + symptom-first containment, then the postmortem that fixes the class |
| Setting up monitoring/alerts | p.14 §9.1–9.2 | SLI-from-user's-side + burn-rate alerting + error budgets — ends alert fatigue and the velocity war at once |
| Delegating to a person | p.17 §11.1–11.2 | The five disciplines + hour economics; delegation fails at the spec, and specs are learnable |
| Delegating to an AI agent/model | p.18 §11.3 | The two machine-specific amendments (spec gaps filled with confidence; independent verification) — saves real money |
| Managing a team / chronic arguments | p.19 Ch.12 | Context-not-control + make-the-argument-a-number; the three-job manager model |
| Code review (giving or getting) | p.16 §10.1, p.11 §6.1 | Review-as-taste-propagation + diff-size-as-reviewability-budget; changes how you review forever |
| Handling money, time, or units in code | p.11 §6.5 | The seven five-minute rules — each one is a prevented court date or 2am page |
| Building UI / anything users touch | p.28 App.B | Defaults, latency-as-emotion, error/empty/degraded states — the taste half of engineering |
| Security review / handling secrets or PII | pp.26–27 App.A | The non-negotiables list + per-class privacy routing — audit yourself before someone else does |
| Testing strategy for a component | p.12 Ch.7 | Hierarchy of evidence + property/fuzz/differential methods — know what your green checkmarks actually prove |
| Career advice (own or a report's) | p.21 Ch.13, p.23 Ch.15 | The altitude traps (each one is the previous virtue overextended) + the invariants worth owning |
| Becoming (and proving you're) the best in the room | pp.24–25 Ch.16 | The compounding loops + the receipts protocol — mastery as auditable evidence, not vibes; how to differentiate and stay state-of-the-art |
| Feeling overloaded / no deep work | p.22 Ch.14 | Making-blocks, cost-of-meetings arithmetic, energy > time — the personal ops manual |
| Why any of this matters | p.35 The Last Page | The confession: every principle was paid for by breaking something. Read it once a year |
| A term someone used ("idiot index"?) | p.32 App.D | The Vocabulary — all 30 named ideas, one line each |
| A whole company's culture/method | binder README.md | Twenty volumes — e.g. SpaceX for deletion/testing, Jane Street for correctness, Stripe for APIs, Google for ops |

---

## 📋 THE FIVE CHECKLISTS (acceptance criteria — full text at p.34)

**Before code:** who needs this + still true? · scariest assumption + cheapest killing experiment? · half-page design note? · one-way or two-way door? · what can be deleted instead?
**Before shipping:** blast radius? · flag + ramp plan? · abort criteria (metric/threshold/decider)? · rollback REHEARSED? · docs/changelog/migration included? · will the 2am logs suffice?
**When it breaks:** symptom first, contain before diagnosing · one commander · live timeline · postmortem asks what the system permitted · fix the class, not the instance.
**Before delegating (human or AI):** outcome spec + acceptance test? · boundary contract? · escalation clause verbatim? · tier matched honestly? · verification independent of self-report?
**Before adopting a dependency:** searched several angles first? · license + provenance FIRST? · alive (commits/releases/maintainer latency)? · issues/tests/core-file read? · spiked on real data? · pinned + locked + decision note written?

---

*"That's what 'as if I'd been sitting beside you' actually means: when something cracks, you hear an old voice ask — what does the system permit? what did you delete this week? did you actually run it? — and you already know what to do."* — The Last Page `[p.35]`
