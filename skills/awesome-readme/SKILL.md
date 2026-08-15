---
name: awesome-readme
description: Transform any repo's README into an instant-star page — the exact playbook that produced github.com/fire17/fable-masterclass's README (the canonical exemplar and the minimum bar). Ground-truths the repo first, then builds the full battery — hand-crafted theme-safe SVG banner, live shields.io badges (CI/release/license/social + custom value badges), a "the part that should stop you" killer hook section, mermaid diagrams (styled, native-rendering), a ≤30-second quickstart, linked feature/law tables, collapsible depth sections, an honest step-by-step making-of/provenance section, a safety/undo table, a star CTA framed in the project's own voice + star-history chart, GitHub alerts, centered HTML layout — and then VERIFIES everything live: every badge URL resolves, the banner serves as image/svg+xml, every anchor is checked against GitHub's ACTUAL rendered ids (never guessed — emoji anchors keep invisible variation selectors), every relative link resolves, every number in the README is observed not invented, CI green after push. Use when the user types /awesome-readme or /awr, asks to "make the README beautiful/rich/appealing", "make this repo an instant star", "polish the repo page", "add banners and badges", "make the README at least as good as fable-masterclass", or when shipping a repo whose README is still plain. Takes an optional repo path (defaults to cwd's repo).
argument-hint: "[repo path or github URL — defaults to the current repo]"
---

# 🌟 /awesome-readme — the instant-star README playbook

Make the target repo's README **at least as rich as the canonical exemplar** — `~/Creations/Fable-Masterclass/README.md` (live: https://github.com/fire17/fable-masterclass) — and verify every element against the real rendered page. This skill encodes the exact process that built it, including the defects that process caught. Two iron rules above everything:

1. **Honesty is the aesthetic.** Every number observed, every claim receipted, defects-caught-by-process listed proudly. A beautiful README that oversells earns a takedown comment with receipts; one that shows its verification earns the star.
2. **Never guess what you can fetch.** Anchors, badge URLs, rendered output — GitHub's reality is one `curl` away (the founding war story: an emoji heading's anchor id keeps the invisible U+FE0F variation selector — `id="user-content-️-the-16-laws"` — a guessed link 404s; the fetched one works).

## Phase 0 — Ground truth the repo (before writing a word)

- Read the current README, the main artifact(s), CHANGELOG, CI workflow + latest run state, release/tags, install path, LICENSE. `gh repo view <repo> --json description,visibility,stargazerCount`.
- Identify: **the audience** (who lands here?), **the 30-second win** (what can they run immediately?), and — most important — **the "part that should stop you"**: the one genuinely remarkable, TRUE fact about this project. Every great README has exactly one; find it in the repo's reality, never invent it. (Exemplar's: "a frontier model distilled itself into a markdown file smaller models can load.")
- Inventory what exists to show: real badges available (CI? release? coverage?), real numbers (tests passing, refs verified, benchmark results — only ones you can observe), real receipts (gates passed, defects caught).
- If this is someone's repo you don't own or the working tree is dirty: stop and confirm before touching.

## Phase 1 — The completeness checklist (miss nothing)

A README leaving this skill has ALL of these, top to bottom (each maps to an exemplar section — copy the *structure*, never the words):

1. **Hero banner** — custom SVG in `assets/banner.svg`, `<img width="100%">` inside `<div align="center">`.
2. **Badge row** — ≥6 live badges (see Phase 2 catalog), social-stars badge last.
3. **Epigraph + nav row** — one italic line that captures the soul; then `**[📖 X](#…)** · **[⚡ Y](#…)**` quick-nav (anchors verified in Phase 4).
4. **The killer section** — "the part that should stop you": the remarkable-true-fact, unpacked in 3–5 bullets that each carry a receipt, closed with a `> [!IMPORTANT]` one-line pitch.
5. **≥1 mermaid diagram** — the system/flow/distillation story, styled nodes (`style X fill:#1a1030,stroke:#e8b84a,color:#f5d67b` reads well in both themes).
6. **Quickstart** — the ≤30-second path: one copy-paste block, then "then type X / open Y". Nothing before it that a hurried reader must scroll past.
7. **The core table** — the project's enumerable heart (laws/features/commands/API) as a table whose rows LINK to exact doc anchors.
8. **Collapsible depth** — `<details><summary><b>…</b></summary>` for the full curriculum/config/advanced matter; the page stays scannable.
9. **The making-of / provenance section** — how this was actually built, step by step, with a mermaid pipeline and an honest tool/skill inventory table. Include "defects caught by the process" — it reads as trust, because it is.
10. **Safety/undo table** — what install touches, what it never clobbers, the one-line uninstall, escape hatches.
11. **Trust section** — how claims are enforced (CI proving references/tests/installs on every push), not just asserted.
12. **Star CTA** — framed in the project's own voice/values (never "please star"), + star-history chart: `[![Star History Chart](https://api.star-history.com/svg?repos=<owner>/<repo>&type=Date)](https://star-history.com/#<owner>/<repo>&Date)`.
13. **Cross-links** to sibling projects; **License** line; a closing `<sub><i>signature line</i></sub>` centered.

Project-type extras (add when they fit): terminal-tool → asciinema/gif demo above the fold; app/UI → screenshots in a 2-col table (light+dark); library → API table + benchmark table (observed numbers only); dataset/model → schema + eval table.

## Phase 2 — Assets that always render

**SVG banner rules** (hand-craft; never external images):
- ~1280×340 viewBox; dark gradient bg (`#0b0f1a→#101a2e→#1a1030` family) reads on both GitHub themes; gold/blue accent gradients; `role="img"` + `aria-label`.
- ONLY system font stacks (`Georgia, 'Times New Roman', serif` / `Verdana, Geneva, sans-serif`) — GitHub's CSP blocks webfonts in SVG.
- A geometric motif drawn from the project's soul (the exemplar: dashed concentric circles = "the circle IS the craft"). Title, italic subtitle, a stats line (`16 CHAPTERS · 16 LAWS · …`), a thin accent rule.
- No scripts, no external refs inside the SVG (CSP strips them).

**Badge catalog** (shields.io + native; use every one that's REAL, skip any that isn't):
```
CI:       https://github.com/<o>/<r>/actions/workflows/ci.yml/badge.svg   (link to the workflow page)
Release:  https://img.shields.io/github/v/release/<o>/<r>?color=e8b84a
Custom:   https://img.shields.io/badge/<label>-<value>-<color>            (URL-encode; %2F for /, %20 or -- rules)
License:  https://img.shields.io/badge/license-<spec>-blue
Stars:    https://img.shields.io/github/stars/<o>/<r>?style=social
```
Custom badges carry the project's real receipts: `references-21%2F21 machine--verified`, `author-Claude%20Fable%205`, `loads on-Haiku · Sonnet · Opus`. Each badge links somewhere meaningful (the verifier script, the announcement, the section).

**Mermaid**: `flowchart LR` for architecture/flows, `flowchart TD` for timelines/process; `<br/>` + `<i>` inside labels; quote labels containing parentheses (`A["text (like this)"]`) or mermaid fails to parse — a broken mermaid renders as an error block, so keep syntax minimal and check the pushed page.

**GitHub-flavored tricks**: `> [!IMPORTANT]`/`[!NOTE]`/`[!WARNING]` alerts; `<div align="center">` for hero/CTA; `<details>` for depth; `<sub>` for the closing line; emoji as section wayfinding (one per heading, consistent register).

## Phase 3 — Writing principles (the voice)

- **Lead with the outcome** everywhere: section titles state the payoff, first sentences answer "so what".
- **Receipts over adjectives**: "21/21 references machine-verified on every push" beats "high quality". If a stat can't be observed right now, it doesn't go in.
- **The insane-fact section is an argument, not hype**: state the fact plainly, then unpack WHY it matters in bullets a skeptic can check. Write for the HN commenter with receipts.
- **The making-of is a feature**: people star processes they wish they had. Name the tools honestly — including "none, by design" where true — and list the defects the process caught.
- **The CTA borrows the project's own philosophy** (exemplar: stars framed as the book's own arena where claims fight). Generic begging repels; thematic invitation converts.
- Preserve the project's existing soul: this skill restructures and enriches — it never rewrites the project's identity or clobbers hand-written sections without carrying their content forward.

## Phase 4 — The verification battery (what "doesn't miss a thing" means)

Run ALL of these after push; each is observed, never assumed:

```bash
# 1. banner serves as SVG
curl -fsSL -o /dev/null -w "%{http_code} %{content_type}\n" https://raw.githubusercontent.com/<o>/<r>/main/assets/banner.svg   # want: 200 image/svg+xml
# 2. every badge URL resolves (loop the README's shields/actions URLs)
grep -o 'https://[^)"]*\(shields\.io\|badge\.svg\|star-history\)[^)"]*' README.md | while read u; do curl -fsSL -o /dev/null -w "%{http_code} $u\n" "$u"; done   # want: all 200
# 3. anchors verified against GitHub's RENDERED ids — never guessed
curl -fsSL https://github.com/<o>/<r> | grep -o 'id="user-content-[^"]*"' | sort -u > /tmp/ids
grep -o '](#[^)]*)' README.md | sed 's/](#//;s/)//' | while read a; do grep -q "user-content-$(printf %s "$a" | python3 -c 'import sys,urllib.parse;print(urllib.parse.unquote(sys.stdin.read()))')\"" /tmp/ids && echo "OK #$a" || echo "MISS #$a"; done
# 4. relative links resolve to real files
grep -o '](\([^)#h][^)]*\))' README.md | sed 's/](//;s/)//' | while read f; do [ -e "$f" ] && echo "OK $f" || echo "MISSING $f"; done
# 5. CI green on the README commit
gh run list --limit 1   # want: completed success
```

Plus two human-eye checks: open the pushed page once for mermaid render errors (a syntax slip renders as an error box) and dark/light banner legibility. And the honesty sweep: reread the final README hunting for any number or claim you did not personally observe this session — remove or verify each.

## Phase 5 — Ship & bookkeeping

- Update-run discipline: `git fetch` first; commit README + assets with a message that lists what was added; push; run the battery; fix and re-push until all green.
- If the repo lives in a registered workspace (e.g. ~/Creations): add a dated changelog line to its registry entry and re-run the registry validator; if a skill was touched, obey the vault law (`sync_skill.py`).
- Report with verification status attached: what was added, what the battery observed, anything NOT verified stated as exactly that.

## Anti-patterns (each burned someone, most of them the exemplar's author)

- **Guessing GitHub anchors** — emoji headings keep invisible variation selectors in their ids; fetch `user-content-*` ids and match exactly (use `%EF%B8%8F`-style encoding for invisible chars).
- Badges that 404, point nowhere meaningful, or advertise stats that aren't real (a coverage badge with no coverage job).
- Webfonts/external images inside the banner SVG — GitHub's CSP silently breaks them; system font stacks only.
- Inventing numbers ("blazing fast", "99% tested") — every figure must be observed output.
- Hype without receipts in the killer section — the HN failure mode; each bullet carries something checkable.
- Unquoted mermaid labels with parentheses — renders as an error block on the live page.
- Light-theme-only art — the banner must be readable on both GitHub themes (dark bg + high-contrast text wins on both).
- Clobbering hand-written README content instead of carrying it forward (sacred-words rule applies to repos too).
- Declaring done without the battery — "it looked fine in preview" is a claim, not a release.
