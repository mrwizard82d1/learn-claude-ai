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

**Open:** the other two Farley videos ("How to Actually Succeed with AI Development", "TDD with an AI Agent") and the
Tessl essay are still to come. Update this section after them.
## 3. Uncle Bob "Clean AI" — (pending)
## 4. Willison red/green · Reed · Spec Kit — (pending)

## Cross-source synthesis — (after block 4)
Where sources agree with `tdd-pairing` · where they differ · what the Rover skipped (the executable outer loop).
