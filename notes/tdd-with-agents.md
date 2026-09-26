# TDD with an agent — discipline notes (Phase 2)

> Worked through the String Calculator kata (`experiments/kata-string-calculator/`)
> with Claude, 2026-09. The kata is incidental; the point was the *discipline* of
> driving red→green→refactor **through an agent**, and feeling where the agent fights it.

## The role split
**AI drives the keyboard; I think and direct.** I decide the next test and the design;
the agent types the test, runs it, and writes the minimal code — under my direction.
Uncle Bob's "discipline over vibes," made concrete. The agent is fast hands; the
judgment stays mine.

## The micro-cycle, and where the agent fights it
- **RED first — and prefer a *behavioral* red.** No production code until a failing test
  exists *and I've watched it fail*. An import/compile/missing-symbol failure technically
  counts, but it's **incidental** — low information, and an agent almost never ships code
  that doesn't even load, so that red barely exercises anything. Prefer a first test that
  fails on an **assertion** (a wrong *result*) — even if it costs a stub returning an
  arbitrary value first. "It produced the wrong value" tells me far more than "it didn't
  load."
- **GREEN minimal** — the *simplest* thing that passes, even "fake it" (`return 0`).
- **REFACTOR or skip** — refactor is an *opportunity* each cycle, not an obligation;
  recognizing "nothing to clean" is part of the discipline (don't gold-plate).
- **Interrogate the *surprising pass*: "Oh — it passed. Why?"** An unexpected green is as
  informative as an unexpected red — often a coincidental / wrong-reason pass hiding a
  latent bug (e.g. a string containing a space read as an integer yielding `32`; or, in
  this kata, `add("0")` passing under the dumb `return 0` merely because `0 == 0`). Chase
  unexpected greens as hard as reds — a test that can't fail can't drive anything.

The **AI gap** (left unguided, the agent will): (a) skip the red — hand back
implementation + tests together; (b) **over-implement** — reach for the general
algorithm on test #2; (c) write tests that merely *confirm* code it already wrote.
Concretely: it wanted `numbers.split(",")` while the only tests were `""→0` and a single
number. `split(",")` only became the *right* move once a **comma test demanded it** —
"as the tests get more specific, the code gets more generic." Discipline was never
"never write split"; it was **"don't write it until a test asks."**

## Planning, my way (the lightweight "plan" phase)
`spec → plan → red → green → refactor` is the outer, feature-level loop; red→green→refactor
is the inner cycle. For a kata the spec is *given* and the plan is *the ordered test list*
— and TDD deliberately **reveals that plan one test at a time** (design emerges; no
big-design-up-front). My idiom for it:
- a **smoke test** first (prove the harness is wired) — here, rep #1 doubled as that;
- a **comment block of test *ideas*** above the test class — seeds thinking. Twin
  discipline: *"not done until each idea is implemented **or** consciously dropped"* **and**
  *"ideas are ideas, not promises"* — an idea may change as the design teaches me.
- `unittest` note: it has **no** declarative `[TestCase]`/`@parametrize`; its idiom is
  **`subTest`** (an imperative loop, all cases reported). Random inputs + `subTest(...)`
  so a failure names the exact value.

## The real lesson: spec ideas are HYPOTHESES, not commandments
The sharpest moment wasn't red/green mechanics — it was the **negatives** episode.

The kata says "negatives raise, listing all offenders." I implemented it test-first…
and the green step **broke three assertions I'd already made** (single-number and comma
tests that summed negatives). That breakage is **information** — the system asking:
*"is this the behavior you actually want?"*

The answer, on **physics not banking**: no. Negative numbers are real and
**information-bearing** (charge, displacement, temperature); rejecting them is an arbitrary
teaching constraint, not a domain truth. So I **consciously dropped idea #7** and kept
negatives summing.

Three things worth remembering:
1. **A pre-existing test breaking under a new implementation is the validation trigger.**
   Don't "fix" the old tests *first* to match the new plan — that answers the question
   before it's asked (quiet confirmation bias), and the agent will do it silently if I let
   it. Let the break happen; treat it as a prompt for judgment.
2. **The human's domain judgment is the irreducible step.** The agent will competently
   build the *wrong* thing because the spec said so. Asking "is this right for my domain?"
   is mine to do.
3. **Not pre-evolving also avoided rework:** because I left the summing tests alone, they
   were already correct once I decided negatives sum — zero churn. Evolving-first would
   have been *wrong* work.

## Why this generalizes to real work
In a domain I know cold, I might spot the contradiction up front — but in unfamiliar code
I'd likely **miss it until the tests demonstrate it**, which is exactly when the signal
matters most. Same spirit as `notes/legacy-workflow.md` (verify against tests, not "looks
good") and the "TDD & AI gap": the agent accelerates the typing; the discipline and the
judgment are the parts that don't delegate.
