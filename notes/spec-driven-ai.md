# Spec-driven AI development: sources vs our practice

Running comparison. Per source: **claim · vs our practice · hypothesis to test.**
Our practice = Mars Rover (F1–F7) + `tdd-pairing` + `legacy-change`. Larry's raw impressions live in
[`spec-driven-coding-agents.md`](./spec-driven-coding-agents.md) (his words; not edited here).

## 1. DeepLearning.AI — "Spec-Driven Development with Coding Agents" (Everitt / JetBrains) — done 2026-11-25

**Claim (course page + Larry's impressions):** write a markdown spec, let the agent implement, human in the loop.
Two levels: a **project constitution** (mission · tech stack · roadmap) set once, then **per-feature**
spec → plan → implement → validate loops, with replanning between features. Same loop for **brownfield**
(generate specs from existing docs). Package your own workflow as an **agent skill**.

**vs our practice**
- Constitution ≈ our `SPEC.md` header + non-goals + conventions, but we never named it as a separate layer.
  Larry: it clarifies that the double loop (red acceptance → red/green/refactor → green acceptance) belongs to the
  **feature** level, not the project level.
- Brownfield in the course = specs *from docs*. Ours = `legacy-archaeologist` → characterization tests → seam.
  Different bet: they trust docs, we trust observed behavior. (Doc-derived specs are hypotheses; see the
  confabulation trap in `notes/legacy-workflow.md`.)
- **Gap in the course (Larry's main criticism):** tests are nearly an afterthought. The emphasis is AI
  across the whole process, not designing an effective *verification* process. Validation exists as a phase,
  but not as executable acceptance tests driving the work.
- "Build your own workflow as a skill" = what we did with `tdd-pairing`. Independent confirmation of the shape.

**Hypotheses to test**
1. A constitution layer would have saved re-orientation after the Mars Rover break (we needed a refresher).
   Test: add a short constitution to the next real project and see whether it shortens re-orientation.
2. The course's validation phase is weaker than red/green acceptance. Test with Farley (block 2): does his
   executable-specification approach fill exactly this gap?
3. Doc-derived brownfield specs vs characterization tests: which finds more wrong assumptions on a real legacy
   target? (Needs a real repo; park until work provides one.)

## 2. Farley — "Acceptance Testing Is the FUTURE of Programming" (video 1 of 3) — done 2026-11-26

Source: Larry's summary in [`acceptance-testing-future.md`](./acceptance-testing-future.md). Not independently checked
against the video; the claims below are as Larry reports them.

**Claim:** acceptance tests are the **harness / set of fixed points** for an AI implementation: they limit the
agent's variability and lower the odds of missing requirements. The developer's focus shifts from implementing a
vague spec in code to writing **executable acceptance tests**. Farley's own result: *almost* correct, needing
engineering review and hand-holding. Not unsupervised; "a viable strategy to raise the level of abstraction in
programming."

**vs our practice**
- Strongest confirmation of the outer loop in `tdd-pairing`: red acceptance → … → green acceptance. Same bet:
  the acceptance test is the contract the agent can't wander from.
- **This is the gap the Mars Rover skipped.** Our `.feature` was documentation, never executed, so our "fixed
  points" were the unit tests only. Farley's fixed points are executable. SPEC.md already records this decision.
- Farley's experiment apparently used **no unit tests**. Larry notes this differs from Bob Martin. Our practice
  uses both loops, so we sit between them.
- "Almost correct + hand-holding" matches our experience: the AI types, Larry directs and catches domain
  judgments (bounds, placement, halt rules). The acceptance tests wouldn't have supplied those; a human wrote them.

**Hypotheses to test**
1. Acceptance-only (Farley) vs double loop (ours): does the inner unit loop add anything when executable
   acceptance tests are already the harness, or only design pressure and diagnosis speed? Test: build one small
   feature both ways (Friday's optional rep) and compare defects, rework and time.
2. "Fixed points limit variability" is testable: run the same executable spec through the agent twice and
   compare the implementations. Do the passing implementations differ in ways the tests can't see?
3. Who writes the acceptance tests matters. If the AI writes them, the harness shares the AI's blind spots.
   Keep Larry as the author or reviewer of the `.feature` (consistent with "spec ideas are hypotheses").

### 2b. Farley — "How to Actually Succeed with AI Development" (video 2 of 3) — done 2026-11-26

Source: Larry's summary in [`h2-succeed-with-ai-dev.md`](./h2-succeed-with-ai-dev.md). An interview with **Guy Podjarny
(CEO, Tessl)**; only a little about Tessl's tool. Recorded as Larry reports it; I haven't seen the video.

**Claim (Larry's reading):** the same approach as video 1 in different terms. The focus is **iterative loops that
improve the software *process*, not just the software**: use expertise to improve software iteratively, and use AI to
improve the process so it uses that expertise more effectively. Treat each **change as an experiment**. One variant
phrasing: "coding the development instead of the solution" (versus the original "go from spec the developer to
spec the solution").

**vs our practice**
- "Change as an experiment" is how we've worked: spec ideas are hypotheses, mutation proves a green-on-arrival test
  bites, and `worked-examples.md` is the refinement seam. We practice it but don't name it as the principle.
- "Improve the process, not just the software" is what `tdd-pairing`, `PROGRESS.md` and memory already do: a lesson
  from one session becomes a rule in the next.
- Tessl is the same company as the essay on the Farley list, so the Tessl essay probably extends this video.

**Resolved (Larry, 2026-11-26): what the phrase means.** "Coding the development instead of the solution" is the
video's concise statement of the change AI introduces. Without AI, development is mainly an engineer writing code.
With AI, it becomes **specifying the solution and letting the AI write the code for *one implementation path* to
that solution.** (My earlier guess, "codify the process as a workflow or skill", was wrong; it is not about
`tdd-pairing`-style tooling.)

**Consequences for our practice**
- The **spec is the durable artifact; the code is one of many possible implementations.** That is the same idea as
  video 1 (acceptance tests as fixed points), seen from the other side: fixed points define the solution, and the
  implementation path is allowed to vary.
- It sharpens hypothesis 2: if code is "one path", then two runs of the same spec *should* produce different paths,
  and the spec must be strong enough that **any** passing path is acceptable. Our Mars Rover specs were not written
  to that standard. They relied on Larry's design direction during the typing, which pinned the path.
- It reframes the Rover: Larry directing the design was **choosing the path**, not just specifying the solution.
  Whether that is the right split is a question the sources raise and we haven't answered (see synthesis).

**Hypothesis to test**
4. Treating each ticket as an experiment: record a one-line hypothesis and outcome per change in `worked-examples.md`
   and see whether it improves the next change. Cheap; try it on the first real-work use of `tdd-pairing`.

**Correction (2026-11-26):** "TDD with an AI Agent: Whisking Raw Ideas into Tidy Code" is **not Farley's**. It is by
Younes (The Software Cook), about an hour. Demoted to optional; not yet watched.

### 2c. Farley — Tessl essay "Vibe Coding — Is this really the best we can do?" — done 2026-11-26

Source: Larry's summary in [`vibe-coding-not-the-best-we-can-do.md`](./vibe-coding-not-the-best-we-can-do.md).
Written by Farley and hosted by Tessl. Recorded as Larry reports it.

**Claim**
- Natural language is too vague to replace a programming language: variations occur even among human
  implementers, so results may be plausible but not repeatable.
- AI programming creates three problems: **specification** (say what we want precisely), **verification**
  (confirm we got it), **incrementalism** (keep learning in small steps when agents make large changes fast).
  "The bottleneck is not code generation... If we do not speed up assurance to match generation, we have only
  moved the constraint."
- **Executable specifications are the program.** A BDD-style spec is readable by humans and executable by
  machines, so it gives specification and verification at once. The programmer's job shifts to defining outcomes,
  edge cases and the non-functional requirements (performance, security, reliability).
- Incrementalism becomes continuous delivery: specs are **version controlled**, acceptance tests run **in a
  deployment pipeline**, and some tests may be **hidden from the AI** to stop example-only passing code.
- AI-generated tests treated as a replacement for precise intent and independent verification "become a bad trade."
- "The generated code becomes less important than the behavior we can prove."

**vs our practice**
- **"Independent verification" = our anchor vs independent-oracle distinction.** Farley's warning about
  AI-generated tests is the failure our mutation checks guarded against, where a green suite proves little.
  Same discipline, stated from the spec side.
- **Hidden tests** is a new idea for us. We never withheld tests from the agent. In `tdd-pairing` the agent sees
  all of them, so an agent could in principle fake-it to green on the visible examples. We counter that with
  triangulation and mutation, not hiding.
- **Version-controlled specs** we do (`SPEC.md`, `.feature`). **Acceptance in a pipeline** we don't: the `.feature`
  never ran, and we had no pipeline. That is the Rover gap again.
- **Tension to resolve:** "we need not inspect every generated line" vs our practice, where Larry directs and
  reviews each step. Farley's condition is "only if we have a reliable way to verify the behavior." Where that
  verification is weak (our Rover had no executable acceptance), reading the code is still the safety net.
- Matches the Podjarny interview (2b): same claim, "behavior we can prove" over "code we wrote."

**Hypotheses to test**
5. **Hidden acceptance tests:** keep a held-out set of examples the agent never sees. After the agent goes green on
   the visible tests, run the held-out set. Does it catch example-only passing? Cheap to try on a small kata.
6. **Verification speed is the real bottleneck.** On the next real ticket, time spec, generation and verification
   separately. Farley predicts verification dominates. Our Rover suggests so (most time went to decisions and
   mutation checks, not typing).

**Open:** nothing left from Farley except the optional Younes video.
## 3. Robert Martin — "Agentic Discipline" (video, published 2026-10) — done 2026-11-26

Source: Larry's notes in [`agentic-discipline.md`](./agentic-discipline.md). Recorded as Larry reports it; I haven't
seen the video, and I haven't checked whether Martin's tools run in our languages.

**Claim (Larry's reading):** Martin does **not** use acceptance tests as the harness. He constrains the agent's
**implementation** with metrics from tools he wrote: **crap, mutate, dry**. In the demo he first builds the
application with none of them (from an original, undocumented prompt), then runs **measure → fix → measure** to
raise code quality. The demo app was simple (single user, I/O rendering changing images, no real user input) yet
still left many opportunities. He also discussed building UIs for developer-specific tools, including an editor
for the "scripts" used in the video.

**Larry's synthesis:** Martin and Farley are **complementary**. Farley constrains *behavior* (acceptance tests as
fixed points; little about engineering quality). Martin constrains *code quality* (the product should be well
engineered; he doesn't try to pin the whole application's behavior). Larry wants "my process" to include both.

**vs our practice**
- **We already hold both halves, but not as one process.**
  - Farley side: the outer loop in `tdd-pairing` (red acceptance → green acceptance). Weak in practice, since the
    Rover `.feature` never executed.
  - Martin side: the **six change-quality goals** in the global `CLAUDE.md` (>90% condition coverage on changed code,
    complexity ≤10, ≤3 arguments, intent-revealing names) plus the `test-strength` skill (condition coverage,
    mutation) and the `work-order` skill. This is the measure-fix-measure idea, targeted at *changes*.
- **"Mutate" = what we hand-ran on the Rover.** We mutated, watched red, restored. Martin has a tool for it; the
  `test-strength` skill covers where a maintained tool works and where to hand-roll.
- **Martin's loop starts after the code exists.** Ours is test-first, so Martin's measures would run in the
  *refactor* step and at the end of a change. That slots in without conflict.
- Farley's "almost correct, needs hand-holding" and Martin's "agent output needs measured cleanup" agree: neither
  trusts raw generation.

**Hypotheses to test**
7. **One combined loop:** red acceptance (Farley) → inner red/green/refactor → **measure-fix-measure gate** (Martin:
   coverage, complexity, mutation, duplication) → green acceptance. Write it as an explicit step in `tdd-pairing`
   or `work-order`, then try it on one real ticket.
8. **Metrics as agent constraints:** give the agent the numeric gates up front (as `work-order` already does) and see
   whether it hits them first time or needs fix cycles. Compare with Martin's measure-fix-measure demo.
9. **Tool availability:** find which of crap / mutate / dry (or equivalents) work for Python and C#. Unverified;
   check before depending on them.

**Open:** none from Martin, beyond hypothesis 9.
## 4. Willison red/green · Reed · Spec Kit

### 4a. Harper Reed — "My LLM codegen workflow atm" (2025-02-16) — done 2026-11-27

Source: Larry's notes in [`my-llm-codegen-workflow.md`](./my-llm-codegen-workflow.md). Recorded as
Larry reports it. The plan file describes the article as the brainstorm spec → plan → execute loop; I haven't read it.

**Claim (Larry's reading):** a "tried AI on a project and it went great" report, similar to and repetitive of
others. Brownfield development is mentioned, but only briefly.

**Larry's critique:** it says little about **maintaining AI-written code long term** and nothing about **software
engineering**, meaning optimizing the "-ilities" of a codebase to meet a business goal at acceptable cost. He is
skeptical but open: AI might lower initial *and* maintenance cost enough that engineering stops mattering; he isn't
convinced.

**vs our practice and the other sources**
- Reed is the **generation-process** layer (spec → plan → execute), the same family as the DeepLearning.AI
  constitution + feature loop. Like that course, it is thin on verification and quality, which Farley (behavior) and
  Martin (code quality) supply. A three-layer picture is emerging: **process (Reed / DLAI) · behavior (Farley) ·
  quality (Martin)**. Held for the synthesis.
- Larry's "-ilities / long-term maintenance" objection is the point of the change-quality goals in `CLAUDE.md`, and
  matches Farley's non-functional requirements (performance, security, reliability) in the Tessl essay.

**Hypothesis to test**
10. **"Engineering no longer matters" is an empirical claim.** Test it on code we have: take an agent-written change,
    then make a *second* change a month later and compare effort against a hand-structured baseline. Needs real
    work; park it until `tdd-pairing` is used on a real ticket. Until then, treat the claim as unproven, as Larry does.

### 4b. Willison red/green — (pending)
### 4c. GitHub Spec Kit — (pending)

## Cross-source synthesis — (after block 4)
Where sources agree with `tdd-pairing` · where they differ · what the Rover skipped (the executable outer loop).
