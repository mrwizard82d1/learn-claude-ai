# Claude Code Mastery Plan

**For:** Senior Software Engineer (decades of experience, physics/math background, working knowledge of neural networks). ~2 months of task-driven Claude Code use; goal is breadth and deliberate skill across analysis, design, coding, automated testing, and test.

**Preferences:** Free / low-cost first; paid only with a clear business case.

**Anchoring mental models you already hold (we build on these):**
- Robert C. Martin's thesis: *the danger of AI agents is undisciplined use* — discipline (TDD, refactoring, verification) matters more, not less, when an agent is fast.
- Pair programming where **the AI drives the keyboard and you own the thinking** — architecture, constraints, correctness, and acceptance.

> Verification note: a few items carry pricing/availability uncertainty (flagged inline). All URLs were gathered in June 2026; confirm before paying.

---

## How this plan is structured

Five phases, roughly 6–8 weeks at a few hours/week, then an ongoing habit. The ordering is deliberate for *your* profile: most engineers should start with tutorials, but you will get more leverage by first understanding **what the agent actually is** (Phase 0), because your NN/math background lets you reason about the loop rather than memorize recipes. Then we close the breadth gap on the tool itself (Phase 1), formalize the discipline you already value (Phase 2), then scale to design/testing/orchestration (Phase 3).

Each phase pairs **input** (reading/video) with **deliberate practice** in this repo as a sandbox. Task-driven learning is why your knowledge is uneven; the practice tasks here are chosen to force breadth.

---

## Phase 0 — Understand the machine (½ week, ~3–4 focused hours) — EXPANDED

*Goal: replace analogies with an accurate mental model of the agent loop. This is your unfair advantage given your background — you can reason about the mechanism instead of memorizing recipes.*

This phase is expanded into three short sessions with concrete deliverables and **steering checkpoints**. The point of detailing only this phase is so we can adjust the rest based on what these sessions reveal. Do them in order; each builds the vocabulary for the next.

### Session 0.1 — Read the loop (45 min, no coding)
- **Read:** Thorsten Ball, "How to Build an Agent" — [ampcode.com/notes/how-to-build-an-agent](https://ampcode.com/notes/how-to-build-an-agent). Read it once *without* coding along, just to absorb the shape: an LLM, a loop, a set of tools, and a context window.
- **Deliverable:** a 5–10 line note in `notes/agent-loop.md` (this repo) answering: *What are the exact steps of one iteration of the agent loop? Where does a "tool call" fit? What ends the loop?*
- **Why no code yet:** you'll get more from the build (0.2) once you already hold the conceptual skeleton.

### Session 0.2 — Build the loop (1.5–2 hrs, hands-on)
- **Do:** follow Ball's article and actually build the ~300-line agent. It's in Go; if you'd rather, reimplement in a language you prefer — the value is in wiring *model → tool-use response → execute tool → feed result back → repeat*, not the language. (If you want, I can scaffold this in the repo and pair with you on it.)
- **Deliverable:** a working toy agent that can read/edit a file via tool calls, committed under `experiments/`.
- **Steering checkpoint ➊:** tell me whether the build clarified or surprised you — especially around how the model "decides" to call a tool and how results re-enter context. Your answer tells me how deep to go on context engineering vs. tool design in later phases.

### Session 0.3 — Connect mechanism to Claude Code (45 min, reading + reflection)
- **Read:** Anthropic, "Effective context engineering for AI agents" — [anthropic.com/engineering/effective-context-engineering-for-ai-agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents). Focus on "context rot," high-signal token selection, and why a tight context beats a big one.
- **Deliverable:** append to `notes/agent-loop.md` a short mapping: *which Claude Code features (CLAUDE.md, `/clear`, `/compact`, `/rewind`, subagents) are really just context-window management of the loop I just built?*
- **Steering checkpoint ➋:** share that mapping. It's the natural launch point into Phase 1, and it tells me which tool features you already intuit vs. which need hands-on practice.

### Optional stretch (skip unless curious)
- **Geoffrey Huntley — "How to Build a Coding Agent" workshop** ([ghuntley.com/agent](https://ghuntley.com/agent/)). Reinforces the same primitives (read/list/bash/edit/search). Do this only if 0.2 left you wanting more reps; otherwise it's redundant.

**Exit criteria for Phase 0:** you can explain Claude Code to another senior engineer as "an LLM in a loop with tools and a managed context window," and you can name which of its features exist purely to manage that context. When you hit both, ping me and we'll expand Phase 1.

---

## Phase 1 — Close the breadth gap on the tool (1.5–2 weeks)

*Goal: know the whole tool surface, not just the paths your tasks happened to require. This is where "task-driven" learning leaves the biggest holes.*

| Resource | Cost | Time | Notes |
|---|---|---|---|
| **Official docs — "Best practices for Claude Code"** ([code.claude.com/docs/en/best-practices](https://code.claude.com/docs/en/best-practices)) | Free | 1–2 hrs | The canonical, maintained successor to Anthropic's original best-practices post. Read it end to end once; it's your reference map. |
| **DeepLearning.AI × Anthropic — "Claude Code: A Highly Agentic Coding Assistant"** ([deeplearning.ai/courses/...](https://www.deeplearning.ai/courses/claude-code-a-highly-agentic-coding-assistant)) | Free in beta *(flag: may move to paid — confirm)* | ~1h50m | 10 lessons, intermediate. Taught by Anthropic's Head of Technical Education. Covers explore/test/refactor/debug, CLAUDE.md, MCP (Playwright/Figma), git worktrees, PR workflows. **Best single structured course.** |
| **Anthropic Academy — "Claude Code in Action," "Introduction to subagents," "Introduction to MCP"** ([anthropic.skilljar.com](https://anthropic.skilljar.com)) | Free (certificate) | Varies | Fills specific gaps. Take subagents + MCP modules even if you skip the rest. |
| **Targeted docs deep-dives** | Free | as needed | Memory/CLAUDE.md, sub-agents, hooks, slash commands, plan mode, permissions/sandboxing — all under [code.claude.com/docs](https://code.claude.com/docs). |

**Deliberate-practice checklist (do each at least once in this repo or a work task):**
- Write a real `CLAUDE.md` with `/init`, then refine it.
- Use **plan mode** (Shift+Tab twice) for a multi-file change before any edit.
- Create one **custom subagent** and one **custom slash command**.
- Wire one **hook** (e.g., run tests/format on stop).
- Connect one **MCP server**.
- Run a non-interactive job: `claude -p "..."`.
- Practice context hygiene: `/clear`, `/compact`, `/rewind`.

---

## Phase 2 — Formalize the discipline (1.5 weeks)

*Goal: turn Martin's "discipline over vibes" into a concrete, repeatable loop. This phase directly extends what you already like.*

| Resource | Cost | Time | Notes |
|---|---|---|---|
| **Your queued Robert Martin video — "Clean AI: Agentic Discipline"** (Clean Coders, [cleancoders.com/episode/agentic-discipline-1](https://cleancoders.com/episode/agentic-discipline-1) and series) | Paid *(pricing unconfirmed — historically per-episode/subscription; watch for sales)* | ~1 hr | Finish the agent-driven episode you have. The series thesis = TDD + refactoring discipline with an agent. |
| **Harper Reed — "My LLM codegen workflow"** ([harper.blog/2025/02/16/...](https://harper.blog/2025/02/16/my-llm-codegen-workflow-atm/)) | Free | 20 min | The canonical *brainstorm spec → plan → execute* loop. The solo-engineer version of spec-driven development; maps cleanly onto plan mode. |
| **Simon Willison — "Red/green TDD" chapter** (in *Agentic Engineering Patterns*, [simonwillison.net/guides/agentic-engineering-patterns](https://simonwillison.net/guides/agentic-engineering-patterns/)) | Free | 30 min | Cleanest short intro to TDD with an agent. |
| **Critical read — "TDD & AI: the gap between claim and practice"** ([kotrotsos.medium.com/...](https://kotrotsos.medium.com/tdd-ai-the-giant-gap-between-claim-and-practice-8b3bfe5a3f7f)) | Free | 15 min | Important failure mode: agents skip the "red" phase and write tests that merely confirm existing code. Knowing this is how you keep the agent disciplined. |
| **GitHub Spec Kit** (spec-driven development toolkit) | Free | 1 hr skim | The de-facto SDD standard with Claude Code integration. Skim to see the formalized version of Harper Reed's pattern. |

**Practice:** Take one non-trivial feature and run it strictly as **spec → plan (plan mode) → red test → green → refactor**, with you reviewing at each gate. Note where the agent tried to cut a corner — that's your "discipline" muscle.

---

## Phase 3 — Design, testing & orchestration at scale (1.5 weeks)

*Goal: move from single-threaded pairing to directing multiple agents and verifying their output rigorously.*

| Resource | Cost | Time | Notes |
|---|---|---|---|
| **Subagents & orchestration guide** ([hidekazu-konishi.com/...subagents...](https://hidekazu-konishi.com/entry/claude_code_subagents_and_orchestration_guide.html)) | Free | 45 min | Delegation, parallel fan-out, custom agent definitions, git worktrees for parallel sessions. |
| **Hamel Husain — "Your AI Product Needs Evals"** ([hamel.dev/blog/posts/evals](https://hamel.dev/blog/posts/evals/)) | Free | 1 hr | The canonical evals essay: error analysis, eval levels, LLM-as-judge with human-agreement measurement. Your math background will appreciate the rigor. Essential once you trust agents with more. |
| **Armin Ronacher — "Agentic Coding Recommendations" + "Agent Design Is Still Hard"** ([lucumr.pocoo.org/2025/6/12/agentic-coding](https://lucumr.pocoo.org/2025/6/12/agentic-coding/)) | Free | 1 hr | Senior-engineer-grade treatment of tradeoffs and tooling design. |
| **Boris Cherny (Claude Code creator) — "Claude Code and the Evolution of Agentic Coding"** (AI Engineer talk; [Class Central mirror](https://www.classcentral.com/course/youtube-claude-code-the-evolution-of-agentic-coding-boris-cherny-anthropic-465473)) | Free | 18 min | Direction-of-travel from the source. |

**Practice:** Use **adversarial review** — have one agent implement and a second (a review subagent) critique it before you merge. Write one small **eval** (even a checklist-based judge) for a task you do repeatedly.

---

## Phase 4 — Make it a habit (ongoing)

*Goal: stay current; the field moves monthly.*

- **Simon Willison's blog + Agentic Engineering Patterns guide** — [simonwillison.net/tags/claude-code](https://simonwillison.net/tags/claude-code/). New chapters ~weekly. Best ongoing skeptical, well-tested source. **Subscribe.**
- **Indragie Karunaratne — "I Shipped a macOS App Built Entirely by Claude Code"** ([indragie.com/blog/...](https://www.indragie.com/blog/i-shipped-a-macos-app-built-entirely-by-claude-code)) — best project-scale context-engineering case study; read once.
- **AI Engineer YouTube channel** — selectively, for conference talks.

---

## Optional paid items — business case

| Item | Cost | Business case |
|---|---|---|
| **Frank Kane — "Claude Code: Building Faster… Prototype to Prod"** (Udemy, [link](https://www.udemy.com/course/anthropic-claude-code/)) | ~$15–25 + ~$10–20 API credits | Best-value hands-on end-to-end build (Docker/nginx/Postgres/CI/CD/security). Worth it if you want one guided production-grade build. |
| **O'Reilly subscription** (incl. Martin's "AI Agents for Clean Code" live training + Eden Marco's *Agentic Coding with Claude Code* book) | ~$49/mo or ~$499/yr | Justified only if your employer already has O'Reilly, or you'll consume several titles. The Martin live event reinforces Phase 2. |
| **Claude Certified Architect (CCA)** ([Anthropic Academy](https://anthropic.skilljar.com)) | ~$99 *(third-party-reported; verify)* | A credential, not new knowledge. Pursue only if certification carries weight in your org. Phases 0–3 cover the exam domains. |

---

## At-a-glance recommended path (free track)

1. **Phase 0:** Thorsten Ball + Anthropic context-engineering essay.
2. **Phase 1:** Official Best Practices doc + DeepLearning.AI course + Academy subagents/MCP, with the practice checklist.
3. **Phase 2:** Your queued Martin video + Harper Reed + Willison Red/green + the "gap" critique; run one feature as spec→plan→red→green→refactor.
4. **Phase 3:** Orchestration guide + Hamel Husain evals + Ronacher; practice adversarial review.
5. **Phase 4:** Subscribe to Simon Willison; revisit quarterly.

Total free-track time: ~20–25 focused hours over 6–8 weeks, almost entirely free.
