# Mars Rover — spec-driven exercise (recursive, outline-first)

**Purpose:** practice `spec → plan → TDD` when requirements are *ambiguous* (unlike a
kata with a given spec). **Method:** outline the features by *name*, then recurse — spec
each **just-in-time** (surface ambiguities → Larry decides → capture the decisions), plan
its tests, build red→green→refactor. Features are hypotheses: reorder / drop / reshape
freely. Tests: Python + stdlib `unittest` (as in the string-calculator kata).

## Scope & non-goals (decided 2026-09-27)
The rover is a **discrete, timeless state machine**:
- `M` moves exactly **one grid cell** — a unit step. **No velocity / speed.**
- **No elapsed time** — commands are an ordered sequence with no temporal semantics.
- Commands execute **instantaneously and are confirmed synchronously** — **no command
  latency / round-trip delay.**

*(Rationale: real rovers are latency-bound → autonomous batch commanding, which is likely
why the domain uses batched command strings. Modeling latency/async is a richer, domain-
truer exercise deliberately left for another day.)*

## Feature outline (names only — spec'd just-in-time)
- **F1.** Create a rover: position (x, y) + heading (N/E/S/W)
- **F2.** Report state (serialize position + heading)
- **F3.** Turn left  (`L`)
- **F4.** Turn right (`R`)
- **F5.** Move forward one cell (`M`) in the current heading
- **F6.** Execute a command string (`"LMLMM"`)
- **F7.** Grid bounds behavior            — *decision-heavy* (wrap? block? error?)
- **F8.** Obstacle detection / handling   — *decision-heavy*
- **F9.** Invalid command / bad input     — *decision-heavy*

**Build order:** F1–F6 first (a walking skeleton of the unambiguous mechanics), then the
decision-heavy F7–F9 once the design has taught us more.

## Decisions — F1 (create) + F2 (report)  [2026-09-27]
- **Coordinates:** N = +y, E = +x, S = −y, W = −x (compass on a math grid). Governs `M` (F5).
- **Heading:** a closed `Enum {N, E, S, W}` — illegal headings are unrepresentable.
- **Rover is immutable** (`@dataclass(frozen=True)`); later `turn`/`move` return a *new* Rover.
- **Construction:** `Rover(x, y, heading)`; arbitrary integer coords allowed at creation
  (bounds checking deferred to F7).
- **F2 report format:** `report() -> str` = `"{x} {y} {H}"`, e.g. `"1 2 N"`. *(Provisional.)*
- Behavioral spec (scenarios + Given/When/Then) lives in **`mars-rover.feature`** (manual
  documentation; `test_mars_rover.py` implements it, kept in sync by hand).

