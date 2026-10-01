# Worked examples — grounding for the tdd-pairing skill

Concrete reps the skill is distilled from. This file is the **refinement seam**:
append real-work episodes here as they happen, then promote any durable new rule
into `SKILL.md`. Keep each example short — the lesson, not a transcript.

## v1 sandbox reps (learn-claude-ai)

### String Calculator kata — `experiments/kata-string-calculator/`
- Practiced the **inner** cycle through the agent: red (behavioral) -> green
  (fake `return 0`) -> triangulate with a different value -> earned generality.
- The **negatives episode** (the central lesson): spec said "negatives raise,"
  but implementing it broke the already-passing summing tests. Rather than
  quietly fixing those tests, we let the break surface as a question. On
  *physics not banking* we **dropped** the raise-on-negative idea — negatives
  carry information (charge, displacement, temperature). Spec ideas are
  hypotheses; domain judgment is the irreducible human step.
- Surprising-pass hunting: `add("0")` passing under `return 0` only because
  `0 == 0`, not because the code was right.

### Mars Rover — `experiments/mars-rover/`
- Practiced the **outer** (acceptance) loop: `SPEC.md` (scope + non-goals:
  discrete, timeless, synchronous state machine — no velocity/elapsed-time/
  latency) + `mars-rover.feature` (manual Gherkin, Scenario Outline + Examples),
  built **one feature at a time, specced just-in-time** (outline-first recursion).
- F1+F2 fake-it: minimal constructor is a no-op; minimal `report()` hardcoded to
  `"1 2 N"`; a second test with *different* initial conditions was the forcing
  test that generalized it.
- **Anchor vs. independent-oracle** tests side by side: an anchor test pins each
  heading to its literal letter with hardcoded don't-care coords; the interleaved
  turn / `execute` tests use randomized inputs checked against independently
  written turn-maps + move-deltas (vs. the impl's `_CLOCKWISE` modular
  arithmetic).
- One **earned refactor** under green (two rotation maps -> `_CLOCKWISE` +
  `_rotate`), committed **separately** from the behavior it followed.
- Convention-as-hypothesis: the `N=+y / E=+x` coordinate convention was stated
  explicitly and flagged "confirm with a domain expert" (oilfield z-down).
- Still open (decision-heavy acceptance scenarios): F7 grid bounds
  (wrap/block/error?), F8 obstacles, F9 invalid/mixed-case input.

## Real-work episodes (append as they happen)

<!--
Template:
### <ticket / feature> — <repo>
- Context: what the change was, what codebase.
- Where the double loop helped / rubbed: ...
- New rule or refinement (if any), promoted to SKILL.md? yes/no
-->

_(none yet — this is where refinement from real work lands)_
