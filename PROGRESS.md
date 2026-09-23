# Progress tracker — Claude Code Master Plan

**Goal (Q3 2026 business objective):** complete **all 5 phases** of
[`claude-code-learning-plan.md`](./claude-code-learning-plan.md) by **Wed 2026-09-30**.
**Cadence:** ~1 hr/day, **weekdays only**, front-loaded.
**Weekends:** off the plan. Saturday = *optional* catch-up if a weekday slipped; **Sunday always off.**
**Evidence:** commit after each session — the git log is the proof of progress for the OKR.
**▶ Next session (resume here):**
1. **The `CLAUDE.md` box on RPA** — ⚠️ **DO NOT run `/init`**: a mature ~250-line `CLAUDE.md` already exists (git-tracked, process/CI/QA/build focus) — `/init` risks clobbering it. It has **no architecture/orientation section**, so the task is to **APPEND one**: 3 executables + session model · WCF `9296` / REST `7047` / `LocalAgentSettings.json` seams · the `Sdk=Web`-service entry-point gotcha · storage single-writer · layering-leaks · pointer to `_laj/rpa-architecture/`. Do NOT duplicate its existing *deterministic-failure test* section or *dead-CommClient* note (cross-ref instead). **RPA `CLAUDE.md` is CLEAN** — Windows git (authoritative for this Windows checkout) shows no change. The ` M` seen earlier was a **WSL/`/mnt/c` autocrlf artifact** (Git-for-Windows `autocrlf=true` normalizes CRLF↔LF and shows clean; WSL git doesn't, so it flags a phantom modification). No real change, nothing lost. **Do nothing to it — and don't diagnose RPA's git state from the WSL side.**
2. *Optional skill polish:* make `architecture-view` **emit an index** templated on your own Orchid go-by (`experiments/orchid/docs_dev/README.md` — Purpose & Scope → "just sketches" caveat → 4+1 sections + TOC), and **prefer SVG** output.
3. *Parked:* harden `repro-planner` (broad Bash/Write); apply the symbol-anchor rule to it.
4. *Learning experiment (informs #1):* run **`/init` on the fresh Orchid clone** — `experiments/orchid/` (gitignored throwaway; **open a session rooted THERE**, `cd experiments/orchid && claude`, NOT this learn-claude-ai session) to see what auto-bootstrap captures on a codebase you know. **Compare three ways:** `/init` output vs your hand-written `docs_dev/README.md` vs our `architecture-view`/`legacy-archaeologist` output → "what's auto-derivable vs needs-a-human vs needs-a-deep-read." Don't commit it (git history untouched); `rm CLAUDE.md` after. Directly informs how to hand-augment RPA's `CLAUDE.md` (#1).
*(Done: RPA-diagram grading — approach validated, deep accuracy TBD as you learn RPA · `Sdk=Web`/`AddWindowsService` encode ✅ · RPA doc already lives in `_laj` ✅ · symbol-anchor rule ✅.)*

**Applied track — skill (log 2026-09-15):** harvested the review-relevant slice of
[`notes/legacy-workflow.md`](./notes/legacy-workflow.md) (the diagnosis + step 5) into **6 cue→check→why
rules** — a legacy-code reviewer's-lens *flavor* draft for Marcos's `pr-review` skill. Pasted into
`~/source/repos/skills/_laj/larry-flavor.md` (personal scratch; promote to
`pr-review/references/flavors/larry.md` once proven on real diffs + Marcos agrees the template-method
shape). Rules are hypotheses to test against live PRs; weight #3 (unexamined invariant) and #6
(Chesterton's fence) — the subtle catches the LLM misses. Rest of the note = a *separate personal
legacy-change skill*, later.

**Subagents (log 2026-09-16):** built the first custom subagents, both **read-only by construction**
(tools restricted → can't edit). `.claude/agents/note-distiller.md` (throwaway, `sonnet`, ≤5-bullet
distiller — grokked the mechanism: separate context, distilled return) and
`.claude/agents/legacy-archaeologist.md` (real: step-1 "understand first" mapper — inherits Opus for
judgment-heavy invariant-spotting; output contract tags `[observed]` vs `[inferred]` and leads with
the test-net verdict, directly countering the confabulation trap from `notes/legacy-workflow.md`).
Validated the archaeologist via a `general-purpose` **stand-in** (named agent needs a session restart
to register — `.claude/agents/` is scanned only at startup; `/agents` wizard is retired). Stand-in
nailed it on a mock "add `edit_file`" target: honest NO test-net, correct observed/inferred split,
mapped-not-designed, and caught the subtle wins (semantic blast radius ≫ code footprint; `.get()`
default silently masking wrong arg keys). Next: restart in a real legacy repo → run the named
`legacy-archaeologist` live. Later: house the full legacy workflow as a **skill** that dispatches it.

**Skill built (log 2026-09-19):** authored `architecture-view` — a Phase-1 skill-authoring rep + real
office tool. Draws 4+1 architecture diagrams (class, sequence, activity/parallel, component, package,
deployment, use-case) as **rendered PlantUML PNGs**, at a chosen altitude, delegating the read-heavy
sweep to `legacy-archaeologist`. Structure: lean `SKILL.md` + per-view `references/` (progressive
disclosure — the Marcos-relevant pattern). Disciplines baked in: observed/inferred edge marks;
"pick a slice, never the hairball"; per-view derivability (concurrency/parallel is the confabulation
danger zone); a **render step + PlantUML gotchas** ref (`rendering.md`); and an **architectural-lens**
option (`arch-models.md`) — Named model / **Unknown (default)** / Candidates-with-evidence, where
"Big Ball of Mud" is a valid verdict (don't confabulate a clean architecture). **Dry-run VALIDATED**
on the (Apache-2.0, self-authored) Orchid Python API cloned to gitignored `experiments/orchid/`:
produced a component view + a load-project→list-wells sequence, both rendered to PNG in gitignored
`_dryrun/`. Larry graded it a strong pass — it exposed the *real* dependencies (leaky facade, an
upward interop→units edge) vs his intended Imperative-Shell/Functional-Core, which motivated the
architectural-lens feature. Ship: copy `.claude/skills/architecture-view` to `~/.claude/skills/` on
BOTH hosts (WSL + Windows), fresh session to register.
Follow-up (same day): added an **evidence profile** to `arch-models.md` — quantifies the Candidates
lens as `X of N edges` per style (normalized %, explicitly NOT a probability/posterior — edges aren't
independent), computed from the observed edge inventory, debatable + updateable, with the mud fraction
doubling as a change-difficulty/coupling gauge. **Re-copy the skill to both hosts** (it changed).

**RPA run + discovery upgrade (log 2026-09-19b):** first live `architecture-view` run on RPA (in the
RPA-rooted session) MISSED the `RPA.Agent` executable and the `TrayClient`↔`RPA.Agent` **WCF** boundary
until Larry supplied it. Diagnosed: (a) WCF/IPC has NO static import edge (separate processes joined by
contract+config at runtime) — the skill's own predicted process-view blind spot; (b) prior *localized*
queries in that session anchored the altitude (context poisoning → Phase 0.3). Encoded the fix in a new
`references/discovery.md` + protocol wiring: **enumerate ALL executables/entry points first**, **hunt
IPC seams** (WCF `[ServiceContract]`+config, pipes, gRPC, REST, queues, shared DB), draw them as
explicit cross-process edges, **flag-and-ask when a seam should exist but no static edge does**, and run
discovery from a **fresh session**. Also: a user confirming a boundary is NOT evidence — ground it in
the contract/config. **Re-copy the skill to both hosts again.**

**Triage upgrade (log 2026-09-19c):** the fresh RPA discovery run found all 5 executables (recall fixed)
but over-included 2 peripheral/utility exes (red herrings) that skewed the assessment. Encoded the
precision fix in `discovery.md`: enumerate = recall, then **triage core-vs-peripheral with a stated
signal, present the list, and CONFIRM scope with the user before drawing** (core-vs-peripheral is domain
knowledge); compute the **evidence profile over the confirmed scope only** (peripheral exes skew N, not
just add nodes). Precision/recall pendulum made explicit. **Re-copy to both hosts.**

**Autonomous agent authoring (log 2026-09-21):** continued using `legacy-archaeologist` + `architecture-view`
on RPA. Also — **independently authored a new agent for real work: `repro-planner`** ("Turns a Jira bug
ticket into a MANUAL, human-executable reproduction plan before any diagnosis begins"). No hand-holding —
the pattern transferred. Design embodies the plan's disciplines: repro-before-diagnosis (= understand-
before-change / characterize-before-fix / RED-before-green — the repro plan is the human precursor to a
failing test), and "manual/human-executable" keeps the human as oracle (no confabulated repro). Composes
into a pipeline: repro-planner → (human reproduces) → legacy-archaeologist → fix behind a test. Strong
evidence toward the **Phase 1 exit** criterion (drive the whole tool surface). Open Q: does it read Jira
via the Atlassian MCP connector? (if so, that's the "connect one MCP server" practice item, in real use).

**Skill polish from grip-viewing the RPA doc (log 2026-09-21b):** viewed the RPA architecture doc via
`grip` (SVG renders fine through grip). Two output improvements prototyped in `RPA/_laj/rpa-architecture/index.md`:
(a) an **image-embedding index** so the deliverable is one viewable page (the README embedded no images);
(b) **grouped by Kruchten 4+1 views + a TOC** (Larry's ask; a view can hold several diagrams — Process has 4).
Confirmed **SVG > PNG** for these (vector: smaller + zoomable; PNG size balloons because sequence/activity
canvases get tall). Candidates to fold into the `architecture-view` skill itself: emit an embedding+TOC+4+1
index, and prefer SVG output. **Encoded now (Larry's sharp catch):** anchor evidence by **enclosing SYMBOL,
not raw line number** — lines rot silently at the next edit; a symbol survives edits and a rename is
git-recoverable; line optional+ephemeral; symbol-less files use a stable landmark. Applied to BOTH
`legacy-archaeologist` and `architecture-view`; `repro-planner` should get the same (his work agent).

## Time budget (reality check)
Remaining ≈ **~17 hours**. Weekdays Sep 8 → Wed Sep 30 (Mon Sep 7 is **Labor Day** — off) = **17 sessions** at ~1 hr ≈ 17 hrs.
→ **Fits within weekdays alone**, essentially zero slack. Front-load; a slipped weekday gets caught up on a Saturday, never by cramming Sunday.

## Resource reality
- **Phase 0 close** = a guided read-through of the toy-agent scaffold ("see it done") — no code, no API key, no cost. (The hands-on *build* stays pinned by choice.)
- **Phases 1–4** = free reading + practice done **inside your work Claude Code** (the subscription you already have), on real/work repos. **No separate API key, no cost.**
- Only possible spend: the Robert Martin "Clean AI" video (Phase 2) — you may already have the queued episode; if paywalled, the free Phase 2 resources cover it (skippable).

---

## Week 1 · Tue Sep 8 – Fri Sep 11 · Close Phase 0 + Phase 1 foundation · ~5h
*(Mon Sep 7 = Labor Day — off. September Mondays are the 7th / 14th / 21st / 28th.)*
**Phase 0**
- [x] 0.1 — Read/understand the loop
- [x] 0.3 — Connect the loop to Claude Code (context engineering)
- [x] 0.2 — closed via **guided read-through** of the scaffold ("see it done", Python + Clojure)
**Phase 1 — close the tool-breadth gap**
- [x] Read official **"Best practices for Claude Code"** end to end
- [x] **DeepLearning.AI** "Claude Code: A Highly Agentic Coding Assistant" (all lessons watched; quiz is Pro-only, skipped)
- [ ] Practice: write a real **CLAUDE.md** (`/init`, then refine) on a work repo · ~0.5h
- [ ] Practice: use **plan mode** on a real multi-file change · (in flow)

## Week 2 · Mon Sep 14 – Fri Sep 18 · Finish Phase 1 + Phase 2 · ~6h
**Phase 1 (remainder)**
- [ ] Anthropic Academy: **subagents** + **MCP** modules · ~1h
- [x] Practice: **custom subagent** — built two read-only agents (`note-distiller`, `legacy-archaeologist`); still to do: one **custom slash command** · ~0.5h
- [~] Practice: connect one **MCP server** ✅ (`repro-planner` reads Jira via the Atlassian MCP — read-only issue tools, in real use); still to do: wire one **hook**, run `claude -p "..."` · ~1h
- [x] Practice: context hygiene — used `/compact` (mid-session save) and `/clear` (to de-poison the RPA discovery run) in real use · (`/rewind` not yet tried — the one remaining)
- [ ] **Phase 1 exit:** you can drive the whole tool surface, not just familiar paths
**Phase 2 — formalize the discipline**
- [ ] Martin "Clean AI: Agentic Discipline" (your queued episode) · ~1h *(skip if paywalled)*
- [ ] Harper Reed — "My LLM codegen workflow" · 20m
- [ ] Willison — "Red/green TDD" chapter · 30m
- [ ] "TDD & AI: the gap between claim and practice" · 15m
- [ ] GitHub Spec Kit — skim · ~1h
- [ ] Practice: run one real feature **spec → plan → red → green → refactor** · ~1h

## Week 3 · Mon Sep 21 – Fri Sep 25 · Phase 3 · ~5h
- [ ] Subagents & orchestration guide · 45m
- [ ] Hamel Husain — "Your AI Product Needs Evals" · 1h
- [ ] Ronacher — "Agentic Coding Recommendations" + "Agent Design Is Still Hard" · 1h
- [ ] Boris Cherny talk — "Claude Code and the Evolution of Agentic Coding" · 18m
- [ ] Practice: **adversarial review** (implement agent + separate review subagent) · ~1h
- [ ] Practice: write one small **eval** (even checklist-based) for a repeated task · ~0.5h

## Week 4 · Mon Sep 28 – Wed Sep 30 · Phase 4 + completion · ~2h + buffer
- [ ] Subscribe to Simon Willison's blog / *Agentic Engineering Patterns*
- [ ] Read Indragie — "I Shipped a macOS App Built Entirely by Claude Code" · 20m
- [ ] Write the "stay current" habit into `notes/` (cadence + sources)
- [ ] **Buffer:** mop up anything that slipped (a Saturday, if needed)
- [ ] **DONE** — final commit marking 5-phase completion 🎉

---

## Reminders (adaptive, reviewed weekly)
Rather than 25 reminders up front: schedule **one week at a time** (weekday mornings), then
review each Friday against this file + the git log. If the week went cleanly, keep them gentle;
**if you slipped, the next week's reminders get more insistent** (and can call out exactly which
boxes are overdue, read from the repo). Setup pending: preferred **time of day** and **channel**.

## Staying on the rails (aimed at "it's easy to forget")
- Block the **same weekday hour** on your calendar — the single most reliable fix.
- **Commit after each session.** The log is both your memory and your OKR evidence.
- Start each session by opening this file and doing the next unchecked box.
