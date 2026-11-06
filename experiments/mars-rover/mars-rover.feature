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
  #   F7     grid bounds (square, inclusive, halt-and-report)   [detailed below]
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

  @f5
  Scenario Outline: Moving forward advances one cell in the current heading
    Given a rover at position (<x>, <y>) facing <heading>
    When it moves forward
    Then its position is (<nx>, <ny>)
    And it is still facing <heading>
    And the original rover is unchanged   # immutability: move_forward returns a NEW rover

    # One cell per heading (per the N=+y / E=+x convention). Coords illustrative; the
    # implementing test randomizes the start position.
    Examples:
      | heading | x | y | nx | ny |
      | N       | 5 | 5 | 5  | 6  |
      | E       | 5 | 5 | 6  | 5  |
      | S       | 5 | 5 | 5  | 4  |
      | W       | 5 | 5 | 4  | 5  |

  @f6
  Scenario: Executing a command string applies lowercase l/r/m left-to-right
    Given a rover at position (1, 2) facing N
    When it executes "lmlmm"
    Then its state is "0 0 S"
    # The implementing test also runs RANDOM l/r/m strings checked against an independent
    # oracle (turn maps + move deltas). Empty string -> unchanged. Case/invalid chars: F9.

  @f7
  Scenario: A move that would leave the grid halts the batch and reports where
    Given a grid of half-extent 5
    And a rover at position (5, -2) facing E
    When it executes "m"
    Then the batch halts before command 0 ("m")
    And the reported rover is still at (5, -2) facing E
    # Bounds exist to keep the rover in radio contact. Edge cells are in range (inclusive);
    # a move to N+1 is refused. Turns are never refused. Later commands are NOT applied.

  @f7
  Scenario: A batch that stays within the grid completes
    Given a grid of half-extent 100
    And a rover at position (3, -43) facing E
    When it executes "mm"
    Then the batch completes
    And the rover is at (5, -43) facing E
    # Inside the bounds the grid is transparent: same result as the unbounded rover.
    # The implementing test uses RANDOM starts and command strings, checked against Rover.execute.

  @f7
  Scenario: A batch that leaves the grid and would return is still halted at the refused move
    Given a grid of half-extent 5
    And a rover at position (3, 0) facing E
    When it executes "mmmrrm"
    Then the batch halts before command 2 ("m")
    And the reported rover is at (5, 0) facing E
    # The bound is checked after EVERY move, not just at the end: "rrm" would have walked
    # back to (5, 0), but the third "m" (x=6) is already out of range. Later commands are not applied.

  @f7 @placement
  Scenario: Placing a rover outside the grid is refused
    Given a grid of half-extent 5
    And a rover at position (9, 9) facing N
    When I place the rover on the grid
    Then placement is refused as off-grid
    And the refusal names the rover and the bound 5
    # The error belongs to PLACEMENT, not to a later command. Edge cells are in range (inclusive).

  @f7 @placement
  Scenario: A completed batch reports the final placed rover
    Given a grid of half-extent 5
    And a rover placed at (3, 0) facing E
    When it executes "mm"
    Then the batch completes
    And the reported placed rover is at (5, 0) facing E
    # The result carries a PlacedRover (known to be on the grid), not a bare Rover.

  @f7 @placement
  Scenario: A halted batch reports the last good placed rover
    Given a grid of half-extent 5
    And a rover placed at (3, 0) facing E
    When it executes "mmm"
    Then the batch halts before command 2 ("m")
    And the reported placed rover is at (5, 0) facing E
    # Same outcome shape as a completed batch: the halt carries the last good PlacedRover.
