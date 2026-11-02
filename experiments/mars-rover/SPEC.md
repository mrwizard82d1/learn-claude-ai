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

### Convention caveat (real-world discipline)
The coordinate and rotation conventions above are the **assumed "standard"** (compass/math).
In real work these are **domain knowledge — verify with a domain expert**, because domains
*invert the obvious*: e.g. oilfield **z is positive downward**; screen coordinates are often
**y-down**; aviation headings run clockwise-from-north. An agent will confidently assume the
textbook default and be *silently* wrong. Assumptions like these belong in the spec, flagged.

## Decisions — F3 (turn left)  [2026-09-27]
- **`L` = 90° counterclockwise:** `N → W → S → E → N`.
- **`turn_left()` returns a NEW (immutable) Rover** with the rotated heading; **position
  unchanged** (heading-only — no coupling to x/y).
- Internal rotation representation left to the tests (fake-it → triangulate).

## Decisions — F4 (turn right)  [2026-09-27]
- **`R` = 90° clockwise:** `N → E → S → W → N`. (Same expert-caveat as F3.)
- **`turn_right()` returns a NEW (immutable) Rover**; symmetric to `turn_left()`;
  heading-only, position + original preserved.
- **Earned refactor (after F4 green):** two near-identical rotation maps = the duplication
  that justifies unifying L/R into a shared rotation (ordered headings + `index ± 1 mod 4`).

## Decisions — F5 (move forward)  [2026-09-27]
- **`M` moves one cell in the heading direction** (per the coordinate convention):
  `N → (x, y+1)`, `E → (x+1, y)`, `S → (x, y−1)`, `W → (x−1, y)`.
- **`move_forward()` returns a NEW (immutable) Rover**; heading unchanged; original untouched.
- **No bounds** — F7 defers bounds; `M` may reach any integer coordinate.
- First feature to exercise the coordinate convention *behaviorally* → its test is the
  convention's guard (a mis-signed axis fails here).

## Decisions — F6 (execute a command string)  [2026-09-27]
- **`execute(commands: str)`** folds a **lowercase** `l`/`r`/`m` string over
  `turn_left` / `turn_right` / `move_forward`, left-to-right, returning the final
  (new, immutable) Rover — a composition of the immutable ops.
- **Lowercase `l`/`r`/`m`** (more visually distinct/readable). Mixed-case / uppercase /
  invalid chars are **F9** (deferred).
- **Empty string → rover unchanged.**


## Decisions — F7 (grid bounds)  [2026-11-02]
- **Why bounded:** the rover must stay within radio contact with Earth. Leaving the comms
  region loses the rover, so the bound is a safety rule, not a teaching constraint.
- **Origin = landing site** (also the fixed relay/base). Coordinates are signed; the bound is
  symmetric about the origin: one parameter, `Grid(half_extent)`.
- **Shape: square, edge inclusive** — in range iff `|x| <= N` and `|y| <= N`. A move to `N+1`
  is refused. *(Simplification: real comms range is a disc / line-of-sight region — verify
  with a domain expert. Relay assumed STATIC; a moving orbiter relay would break the
  timeless non-goal.)*
- **Wrap rejected:** teleporting across the grid is physically meaningless.
- **Rule lives in `Grid`, not `Rover`:** `Grid.execute(rover, commands)`. `Rover.execute`
  stays unbounded, so F1–F6 stay valid untouched.
- **Refused move halts the batch** and reports, so Earth can re-plan (later commands were
  planned assuming the move happened). Turns are never refused.
- **Result type, not exceptions** (stdlib frozen dataclasses):
  `Completed(rover)` | `Halted(rover, index, command)` — `rover` = last good state;
  `index` = position of the refused command in the string.
- **Open (hold for last):** start position out of bounds (placement) — a different seam.
