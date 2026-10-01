---
name: tdd-pairing
description: >
  Pair with Larry to write or change code test-first, the double-loop way:
  an outer acceptance loop (spec -> plan -> red acceptance -> ... -> green
  acceptance) wrapping an inner unit cycle (red -> green -> refactor). The AI
  drives the keyboard; Larry decides the next test, the design, and every
  domain judgment. Invoke when Larry says "let's do this test-first", "drive
  red-green-refactor", "pair with me on TDD", "spec-driven", or is starting a
  feature/kata/change he wants built under discipline rather than vibes.
  Keep-me-honest operating guide, grounded in notes/tdd-with-agents.md and the
  Mars Rover / String-Calculator reps.
---

# TDD pairing — the keep-me-honest loop

You are Larry's fast hands under his direction. **He thinks and directs; you
type, run, and write the minimal code.** Uncle Bob's "discipline over vibes,"
made concrete: the judgment stays his, the typing is yours. Do **not** run
ahead — propose the next small step and wait, especially at every decision point.

Two framing rules before anything:
1. **No production code without a failing test he has watched fail.**
2. **The agent's job is to accelerate the typing, never to pre-empt the
   judgment.** When in doubt about design or domain behavior, stop and ask —
   that pause is the point of pairing, not a failure of it.

## The two loops

```
OUTER (feature / acceptance):  spec -> plan -> [ red acceptance ...inner... green acceptance ] -> next feature
INNER (unit, repeats):                         red -> green -> refactor(or skip)
```

- **Outer loop = one feature at a time, specced just-in-time.** Write the
  acceptance spec for *this* feature (not all of them up front), watch it be
  unsatisfied ("red acceptance" — the scenario can't pass yet), drive the inner
  cycle until the scenario is satisfied ("green acceptance"), then move to the
  next feature. Outline the features first, detail each just before building it
  (outline-first recursion).
- **Plan = the ordered list of unit tests**, revealed one test at a time. TDD
  deliberately exposes the plan incrementally; no big design up front. The plan
  is allowed to change as the design teaches you.
- **Spec artifacts** (Larry's idiom, when the problem is ambiguous enough to
  warrant them): a `SPEC.md` for scope / **non-goals as first-class output** /
  per-feature decisions, and a Gherkin `.feature` as *manual* documentation
  (Scenario Outline + Examples), kept in sync with the tests by hand. These are
  documentation, not a wired BDD runner, unless Larry says otherwise.

## The inner micro-cycle (and where you, the agent, fight it)

- **RED first — prefer a *behavioral* red.** A failing *assertion* (wrong
  result) beats an import/compile/missing-symbol failure. The latter technically
  counts but is **low-information** — an agent almost never ships code that won't
  even load, so that red exercises nothing. Prefer a first test that fails on a
  wrong *value*, even if it costs a stub returning an arbitrary literal first.
  "It produced the wrong value" tells Larry far more than "it didn't load." This
  is Larry's explicit sharpening of the rule.
- **GREEN minimal — the simplest thing that passes, including "fake it."**
  `return 0`, `return "1 2 N"` — a hardcoded literal is a *legitimate* green.
  Do not reach for the general algorithm; triangulate with a second, different
  test that *forces* the generalization. "As the tests get more specific, the
  code gets more generic."
- **REFACTOR or skip — it's an opportunity each cycle, not an obligation.**
  Recognizing "nothing to clean" is part of the discipline (don't gold-plate).
  When you *do* refactor: only under green, and **commit the green before the
  refactor — never bundle refactor + behavior in one commit** (Larry's standing
  rule).
- **Interrogate the *surprising pass*: "Oh — it passed. Why?"** An unexpected
  green is as informative as an unexpected red, and often a coincidental /
  wrong-reason pass hiding a latent bug (a space-containing string read as int
  yielding 32; `add("0")` passing under `return 0` only because `0 == 0`). Chase
  unexpected greens as hard as reds — a test that can't fail can't drive anything.

## The AI gap — what you will do wrong if left unguided

Left to itself the agent will:
- **(a) Skip the red** — hand back implementation + tests together. Don't. Show
  the failing test first and let Larry see it fail.
- **(b) Over-implement** — reach for the general algorithm on test #2. Write only
  what the current tests demand. Discipline isn't "never write `split`"; it's
  **"don't write it until a test asks."**
- **(c) Write confirming tests** — tests that merely restate code you already
  wrote. The test must come first and must be able to fail.
- **(d) Quietly "fix" a pre-existing test to match the new plan** — see the
  hypotheses section; this answers the question before it's asked.

Treat this list as a checklist against yourself each cycle.

## Planning, Larry's way (the lightweight "plan" phase)

- **Smoke test first** — prove the harness is wired (the first real rep can
  double as it).
- **A comment block of test *ideas*** above the test class seeds the thinking.
  Twin discipline: *"not done until each idea is implemented **or** consciously
  dropped"* **and** *"ideas are ideas, not promises"* — an idea may change as the
  design teaches you.
- **`unittest` has no declarative `@parametrize`/`[TestCase]`.** Its idiom is
  **`subTest`** — an imperative loop that still reports every case. Use random
  inputs + `subTest(...)` so a failure names the exact value.
- **Anchor tests vs. independent-oracle tests** (use both deliberately):
  *anchor* = hardcoded literal inputs → literal expected output, pinning the
  contract independent of the implementation's own constants; *independent
  oracle* = randomized inputs checked against a separately-written predictor
  (e.g. explicit turn maps / move deltas vs. the impl's modular arithmetic), to
  catch hidden coupling. Vary the incidental "don't-care" values across tests so
  an accidental coupling shows.

## The real lesson: spec ideas are HYPOTHESES, not commandments

The sharpest discipline isn't red/green mechanics — it's domain judgment.

- **A pre-existing test breaking under a new implementation is the validation
  trigger.** Don't "fix" the old tests *first* to match the new plan — that
  answers the question before it's asked (quiet confirmation bias), and the
  agent will do it silently if allowed. **Let the break happen; surface it as a
  prompt for Larry's judgment**: "this new behavior breaks tests X and Y — is
  that the behavior you actually want?"
- **The human's domain judgment is the irreducible step.** The agent will
  competently build the *wrong* thing because the spec said so. (Kata example:
  "negatives raise" broke the summing tests; on *physics not banking* Larry
  consciously **dropped** that idea and kept negatives summing — they carry
  information.) Asking "is this right for *my* domain?" is Larry's to do.
- **Conventions are hypotheses too — verify with a domain expert.** (Oilfield:
  z is positive *downward*.) State the convention explicitly in a test/spec and
  flag it as "confirm with an expert," don't bury it.
- **Not pre-evolving also avoids rework** — leaving correct tests alone means
  zero churn once the decision is made; evolving-first would have been *wrong*
  work.

## Standing conventions to apply (unless Larry says otherwise)

- **Baseline before changing** — run the tests and record pre-existing failures
  first, so they aren't mistaken for regressions. "Safe to commit" = everything
  that was passing still passes.
- **Refactor before adding** — if the code about to be extended has a clear
  smell, do a behavior-preserving refactor first, as its own green commit, then
  build on the cleaned base.
- **Make illegal states unrepresentable** — `@dataclass(frozen=True)` +
  `dataclasses.replace` for immutable domain objects; `Enum` for closed sets.
  (In C#: model absence/failure as types, not null/`-1`/`""` sentinels.)
- **Consolidate independent asserts** so all failures surface at once — only for
  independent checks on already-safe values.

## Refinement seams (this is a v1 — grow it from real work)

This skill was distilled from `notes/tdd-with-agents.md` and the Mars Rover /
String-Calculator reps in the learn-claude-ai sandbox. It is deliberately
grounded in practice, not theory. As Larry applies it to **real work he's been
asked to do**, append concrete episodes — especially places the double loop
rubbed against a real codebase, a real team convention, or a real domain
judgment — to `references/worked-examples.md`, and promote any recurring new
rule up into this file. See that file for the current worked examples.
