# Progress tracker — Claude Code Master Plan

**Goal (Q3 2026 business objective):** complete **all 5 phases** of
[`claude-code-learning-plan.md`](./claude-code-learning-plan.md) by **Wed 2026-09-30**.
**Cadence:** ~1 hr/day, **weekdays only**, front-loaded.
**Weekends:** off the plan. Saturday = *optional* catch-up if a weekday slipped; **Sunday always off.**
**Evidence:** commit after each session — the git log is the proof of progress for the OKR.
**▶ Next session:** build a simple **custom subagent** (you're jazzed about it). Then the **`CLAUDE.md`** exercise — do it on a *legacy* repo you maintain (see [`notes/legacy-workflow.md`](./notes/legacy-workflow.md)).

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
- [ ] **DeepLearning.AI** "Claude Code: A Highly Agentic Coding Assistant" (10 lessons) · ~2h
- [ ] Practice: write a real **CLAUDE.md** (`/init`, then refine) on a work repo · ~0.5h
- [ ] Practice: use **plan mode** on a real multi-file change · (in flow)

## Week 2 · Mon Sep 14 – Fri Sep 18 · Finish Phase 1 + Phase 2 · ~6h
**Phase 1 (remainder)**
- [ ] Anthropic Academy: **subagents** + **MCP** modules · ~1h
- [ ] Practice: one **custom subagent** + one **custom slash command** · ~0.5h
- [ ] Practice: wire one **hook**; connect one **MCP server**; run `claude -p "..."` · ~1h
- [ ] Practice: context hygiene — `/clear`, `/compact`, `/rewind` in real use · (in flow)
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
