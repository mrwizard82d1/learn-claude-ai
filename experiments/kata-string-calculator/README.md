# Phase 2 kata — String Calculator (TDD *with an agent*)

A classic incremental kata (Roy Osherove). We're not here to *finish* it — we're here to
practice the **discipline** of driving red→green→refactor **through an agent**, and to feel
exactly where the agent tries to skip the discipline. Many tiny steps = many reps.

## The role split (the point of Phase 2)
**AI drives the keyboard; you think and direct.** You decide the next test and the design;
the agent types the test, runs it, and writes the minimal code — under your direction. Uncle
Bob's "discipline over vibes," made concrete.

## Rules of engagement (enforce these on the agent)
1. **RED first.** No production code until a *failing* test exists **and we've watched it
   fail.** Write test → run → see red → *then* implement. Never the reverse.
2. **GREEN minimal.** Write the *simplest* code that passes — even "fake it" (return a
   constant). Resist the agent's urge to implement the whole algorithm at once.
3. **REFACTOR** only with tests green; behavior unchanged.
4. **One step at a time.** One new test per cycle. You pick it.

## The AI-gap to watch for (your own legacy-notes insight)
The agent will try to: **(a) skip the red** ("here's the implementation and tests"),
**(b) over-implement** (write the general algorithm on test #2), and **(c) write tests that
merely confirm code it already wrote** (no real red). *Your job is to stop it* — that's the
skill this kata builds. Each time it over-reaches, we name it and pull it back.

## The kata steps (you drive; don't read ahead to code)
`add(numbers: str) -> int`
1. `""` → `0`
2. `"1"` → `1`  ·  `"5"` → `5`
3. `"1,2"` → `3`
4. an unknown count of comma-separated numbers
5. newlines as delimiters too: `"1\n2,3"` → `6`
6. custom delimiter: `"//;\n1;2"` → `3`
7. negatives throw, listing all offenders
8. numbers > 1000 ignored
*(We'll likely stop well before the end — the reps matter more than completion.)*

## How we run it (fast red/green loop)
Stdlib `unittest` (zero install):
```
cd experiments/kata-string-calculator
python3 -m unittest -v          # or: python3 -m unittest test_string_calculator
```
(If you'd rather use `pytest`, that's fine too.)

## Files (created live, TDD-style — none pre-written)
- `string_calculator.py` — the implementation (starts empty; grows only to pass tests)
- `test_string_calculator.py` — the tests (one at a time)

## First step when you're back
We write **one failing test**: `add("")` returns `0`. Run it, watch it go **red**, and only
then write the one line to make it green. That's rep #1.
