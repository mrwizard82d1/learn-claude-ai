# Mars Rover — behavioral spec (MANUAL documentation; not wired to a BDD runner).
# Rationale: practice spec -> plan -> TDD on an ambiguous problem. Scope & non-goals live
# in SPEC.md (a discrete, timeless, synchronous state machine — no velocity/time/latency).
# Scenarios below are implemented by tests in test_mars_rover.py, kept in sync by hand.

@mars-rover
Feature: Command a rover on a grid
  As a mission operator
  I want to place a rover and command it with L / R / M
  So that I can position it on the grid deterministically

  # --- Scenario headlines (the plan; each detailed just-in-time) -------------
  #   F1+F2  create & report            [detailed below]
  #   F3     turn left  (L)
  #   F4     turn right (R)
  #   F5     move forward one cell (M)
  #   F6     execute a command string ("LMLMM")
  #   F7     grid bounds behavior        -- decision-heavy (wrap? block? error?)
  #   F8     obstacle detection / handling -- decision-heavy
  #   F9     invalid command / bad input -- decision-heavy
  #   INV    (cross-cutting) every operation returns a NEW rover; the original is never mutated

  @f1 @f2
  Scenario Outline: A newly created rover reports its position and heading
    Given a rover created at position (<x>, <y>) facing <heading>
    When I ask it to report its state
    Then the report is "<x> <y> <heading>"

    # Sign quadrants x all four headings. The x/y values below are ILLUSTRATIVE — the
    # implementing test randomizes coordinates within each quadrant's sign pattern.
    # (Bounds are out of scope until F7, so arbitrary integers are fine.)
    Examples:
      | quadrant | x   | y   | heading |
      | +x +y    | 12  | 34  | N       |
      | +x -y    | 47  | -8  | E       |
      | -x +y    | -5  | 21  | S       |
      | -x -y    | -63 | -9  | W       |

  @f3
  Scenario Outline: Turning left rotates the heading 90 degrees counterclockwise
    Given a rover facing <start>
    When it turns left
    Then it is facing <end>
    And its position is unchanged
    And the original rover still faces <start>   # immutability: turn_left returns a NEW rover

    Examples: the full counterclockwise cycle
      | start | end |
      | N     | W   |
      | W     | S   |
      | S     | E   |
      | E     | N   |

  @f4
  Scenario Outline: Turning right rotates the heading 90 degrees clockwise
    Given a rover facing <start>
    When it turns right
    Then it is facing <end>
    And its position is unchanged
    And the original rover still faces <start>   # immutability: turn_right returns a NEW rover

    Examples: the full clockwise cycle
      | start | end |
      | N     | E   |
      | E     | S   |
      | S     | W   |
      | W     | N   |
