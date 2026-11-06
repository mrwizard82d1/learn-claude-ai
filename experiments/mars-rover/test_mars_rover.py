import random
import unittest

from mars_rover import Completed, Grid, Halted, Heading, OffGrid, Placed, PlacedRover, Rover


class MarsRoverTests(unittest.TestCase):
    # Place a rover on a grid, asserting the placement succeeded (so a bad start fails loudly
    # here, not as an AttributeError later). Returns the PlacedRover that Grid.execute takes.
    def _placed(self, grid, rover):
        result = grid.place(rover)
        self.assertIsInstance(result, Placed)
        return result.placed

    # F1 + F2 — a newly created rover reports its position and heading.
    # (mars-rover.feature :: "A newly created rover reports its position and heading")
    # F1 + F2 — a newly created rover reports its ACTUAL position and heading,
    # across sign quadrants and all four headings.
    # (mars-rover.feature :: Scenario Outline "A newly created rover reports ...")
    def test_report_reflects_initial_conditions_across_quadrants(self):
        pos = lambda: random.randint(1, 1000)
        neg = lambda: random.randint(-1000, -1)
        cases = [
            (pos(), pos(), Heading.N),   # +x +y
            (pos(), neg(), Heading.E),   # +x -y
            (neg(), pos(), Heading.S),   # -x +y
            (neg(), neg(), Heading.W),   # -x -y
        ]
        for x, y, heading in cases:
            with self.subTest(x=x, y=y, heading=heading):
                self.assertEqual(Rover(x, y, heading).report(), f"{x} {y} {heading.value}")

    # F1 + F2 (anchor) — pin each heading to its LITERAL serialization, independent of
    # the Heading enum's value. Hard-coded, VARIED "don't-care" coords (different from
    # the other tests) for breadth: vary the incidentals so an accidental coupling shows.
    def test_each_heading_serializes_to_its_letter(self):
        cases = [
            (7, 3, Heading.N, "7 3 N"),
            (-15, 42, Heading.E, "-15 42 E"),
            (100, -250, Heading.S, "100 -250 S"),
            (-8, -9, Heading.W, "-8 -9 W"),
        ]
        for x, y, heading, expected in cases:
            with self.subTest(heading=heading, expected=expected):
                self.assertEqual(Rover(x, y, heading).report(), expected)

    # F3 — turning left rotates the heading 90 deg CCW (full cycle N->W->S->E->N),
    # position unchanged, and the ORIGINAL rover is not mutated (returns a NEW rover).
    # (mars-rover.feature :: Scenario Outline "Turning left rotates ...")
    def test_turn_left_rotates_ccw_and_is_immutable(self):
        cycle = [
            (Heading.N, Heading.W),
            (Heading.W, Heading.S),
            (Heading.S, Heading.E),
            (Heading.E, Heading.N),
        ]
        for start, end in cycle:
            x, y = random.randint(-1000, 1000), random.randint(-1000, 1000)
            with self.subTest(start=start, end=end, x=x, y=y):
                rover = Rover(x, y, start)
                turned = rover.turn_left()
                self.assertEqual(turned.heading, end)           # rotated CCW
                self.assertEqual((turned.x, turned.y), (x, y))  # position unchanged
                self.assertEqual(rover.heading, start)          # original untouched

    # F4 — turning right rotates the heading 90 deg CW (full cycle N->E->S->W->N),
    # position unchanged, original not mutated. (mars-rover.feature :: "Turning right ...")
    def test_turn_right_rotates_cw_and_is_immutable(self):
        cycle = [
            (Heading.N, Heading.E),
            (Heading.E, Heading.S),
            (Heading.S, Heading.W),
            (Heading.W, Heading.N),
        ]
        for start, end in cycle:
            x, y = random.randint(-1000, 1000), random.randint(-1000, 1000)
            with self.subTest(start=start, end=end, x=x, y=y):
                rover = Rover(x, y, start)
                turned = rover.turn_right()
                self.assertEqual(turned.heading, end)           # rotated CW
                self.assertEqual((turned.x, turned.y), (x, y))  # position unchanged
                self.assertEqual(rover.heading, start)          # original untouched

    # F3/F4 (thoroughness) — INTERLEAVED random L/R sequences (with repetitions) must land
    # where an INDEPENDENT oracle predicts. Guards against any hidden stateful coupling in
    # rotation (there should be none — the rover is immutable). Oracle uses explicit
    # per-direction maps; the impl uses modular arithmetic, so this cross-checks it.
    def test_random_interleaved_turn_sequences(self):
        left_of = {Heading.N: Heading.W, Heading.W: Heading.S,
                   Heading.S: Heading.E, Heading.E: Heading.N}
        right_of = {Heading.N: Heading.E, Heading.E: Heading.S,
                    Heading.S: Heading.W, Heading.W: Heading.N}
        for _ in range(4):
            start = random.choice(list(Heading))
            x, y = random.randint(-1000, 1000), random.randint(-1000, 1000)
            turns = [random.choice("LR") for _ in range(random.randint(2, 8))]

            expected = start                       # independent oracle
            for t in turns:
                expected = left_of[expected] if t == "L" else right_of[expected]

            rover = Rover(x, y, start)             # apply via the implementation
            for t in turns:
                rover = rover.turn_left() if t == "L" else rover.turn_right()

            with self.subTest(start=start, turns="".join(turns), expected=expected):
                self.assertEqual(rover.heading, expected)
                self.assertEqual((rover.x, rover.y), (x, y))   # turns never move

    # F5 — move forward one cell in the current heading. This is the first test to
    # exercise the coordinate convention (N=+y, E=+x, ...); its deltas map is an
    # INDEPENDENT statement of that convention. Heading unchanged; original untouched.
    # (mars-rover.feature :: Scenario Outline "Moving forward advances one cell ...")
    def test_move_forward_advances_one_cell_per_heading(self):
        deltas = {
            Heading.N: (0, 1),
            Heading.E: (1, 0),
            Heading.S: (0, -1),
            Heading.W: (-1, 0),
        }
        for heading, (dx, dy) in deltas.items():
            x, y = random.randint(-1000, 1000), random.randint(-1000, 1000)
            with self.subTest(heading=heading, x=x, y=y, dx=dx, dy=dy):
                rover = Rover(x, y, heading)
                moved = rover.move_forward()
                self.assertEqual((moved.x, moved.y), (x + dx, y + dy))  # advanced per convention
                self.assertEqual(moved.heading, heading)                # heading unchanged
                self.assertEqual((rover.x, rover.y), (x, y))            # original untouched

    # F6 — execute(commands) folds a lowercase l/r/m string over the ops, left-to-right,
    # returning the final (new) rover. Checked against an INDEPENDENT oracle that reuses
    # the turn maps + move deltas. (mars-rover.feature :: "Executing a command string ...")
    def test_execute_runs_a_random_command_string(self):
        left_of = {Heading.N: Heading.W, Heading.W: Heading.S,
                   Heading.S: Heading.E, Heading.E: Heading.N}
        right_of = {Heading.N: Heading.E, Heading.E: Heading.S,
                    Heading.S: Heading.W, Heading.W: Heading.N}
        deltas = {Heading.N: (0, 1), Heading.E: (1, 0),
                  Heading.S: (0, -1), Heading.W: (-1, 0)}
        for _ in range(4):
            x0, y0 = random.randint(-1000, 1000), random.randint(-1000, 1000)
            start = random.choice(list(Heading))
            commands = "".join(random.choice("lrm") for _ in range(random.randint(1, 12)))

            ex, ey, eh = x0, y0, start                 # independent oracle
            for c in commands:
                if c == "l":
                    eh = left_of[eh]
                elif c == "r":
                    eh = right_of[eh]
                else:  # "m"
                    dx, dy = deltas[eh]
                    ex, ey = ex + dx, ey + dy

            final = Rover(x0, y0, start).execute(commands)
            with self.subTest(start=start, commands=commands, expected=(ex, ey, eh)):
                self.assertEqual((final.x, final.y, final.heading), (ex, ey, eh))

    # F7 (anchor) — a move that would leave the grid is refused: the batch HALTS before it and
    # reports the last good rover, the index, and the refused command. Hardcoded literals.
    # (mars-rover.feature :: "A move that would leave the grid halts the batch ...")
    def test_move_off_the_edge_halts_and_reports(self):
        grid = Grid(5)
        placed = self._placed(grid, Rover(5, -2, Heading.E))
        self.assertEqual(grid.execute(placed, "m"), Halted(placed, 0, "m"))

    # F7 (forcing) — a batch that never leaves the grid COMPLETES, and the grid is transparent:
    # the final rover equals the unbounded Rover.execute result (F6 already pins that, so it is
    # the oracle). Start within +-50 and at most 12 commands, so with half_extent 100 the
    # rover cannot reach an edge. Kills the hardcoded Halted fake.
    # (mars-rover.feature :: @f7 "A batch that stays within the grid completes")
    def test_in_bounds_batch_completes_like_unbounded(self):
        grid = Grid(100)
        for _ in range(4):
            start = Rover(random.randint(-50, 50), random.randint(-50, 50),
                          random.choice(list(Heading)))
            commands = "".join(random.choice("lrm") for _ in range(random.randint(1, 12)))
            with self.subTest(start=start, commands=commands):
                self.assertEqual(grid.execute(start, commands),
                                 Completed(start.execute(commands)))

    # F7 (forcing) — a batch that LEAVES the grid and comes back is still HALTED at the refused
    # move: the check must be per-move, not on the final position. Hardcoded anchor: from (3, 0)
    # facing E in Grid(5), "mmm" reaches x=6 at command index 2 (refused); "rrm" would have
    # walked back to (5, 0), which is in bounds. Expect: last good rover (5, 0, E), index 2, "m".
    # (mars-rover.feature :: @f7 "A batch that leaves the grid and would return ...")
    def test_batch_that_leaves_and_returns_still_halts(self):
        start = Rover(3, 0, Heading.E)
        self.assertEqual(Grid(5).execute(start, "mmmrrm"),
                         Halted(Rover(5, 0, Heading.E), 2, "m"))

    # F7 (characterization) — the edge is INCLUSIVE: a move that lands exactly on |x|==N or
    # |y|==N is allowed (only N+1 is refused). All four edges, hardcoded anchors, with varied
    # don't-care coordinates. Green on arrival (the per-move check is already general), so its
    # bite is proven by mutation: change <= to < in Grid._in_bounds and this must go red.
    def test_a_move_onto_the_edge_is_allowed(self):
        cases = [
            (Rover(4, -3, Heading.E), Rover(5, -3, Heading.E)),
            (Rover(-4, 2, Heading.W), Rover(-5, 2, Heading.W)),
            (Rover(1, 4, Heading.N), Rover(1, 5, Heading.N)),
            (Rover(-2, -4, Heading.S), Rover(-2, -5, Heading.S)),
        ]
        grid = Grid(5)
        for start, expected in cases:
            with self.subTest(start=start):
                placed = self._placed(grid, start)
                self.assertEqual(grid.execute(placed, "m"), Completed(PlacedRover(expected)))

    # F7 (characterization) — a move that would cross the edge is REFUSED on all four sides
    # (both signs of both axes). From each edge cell facing outward, "m" halts at index 0 and
    # reports the unmoved rover. Hardcoded anchors, varied don't-care coordinates. Green on
    # arrival; bite proven by mutants (drop the y check / drop the x check / drop abs()).
    def test_a_move_off_any_edge_is_refused(self):
        cases = [
            Rover(5, -3, Heading.E),
            Rover(-5, 2, Heading.W),
            Rover(1, 5, Heading.N),
            Rover(-2, -5, Heading.S),
        ]
        for start in cases:
            with self.subTest(start=start):
                self.assertEqual(Grid(5).execute(start, "m"), Halted(start, 0, "m"))

    # F7 (characterization) — TURNS are never refused, even on the edge: standing on a corner
    # (both |x| and |y| equal N) turns still complete, with position unchanged. Four corners,
    # hardcoded anchors, both turn directions. Green on arrival; bite proven by mutants that
    # tighten a bound (<= -> <), which would refuse a turn because the rover is merely AT the edge.
    def test_turns_on_the_edge_are_allowed(self):
        cases = [
            (Rover(5, 5, Heading.N), "l", Rover(5, 5, Heading.W)),
            (Rover(-5, 5, Heading.E), "r", Rover(-5, 5, Heading.S)),
            (Rover(-5, -5, Heading.S), "l", Rover(-5, -5, Heading.E)),
            (Rover(5, -5, Heading.W), "r", Rover(5, -5, Heading.N)),
        ]
        for start, commands, expected in cases:
            with self.subTest(start=start, commands=commands):
                self.assertEqual(Grid(5).execute(start, commands), Completed(expected))

    # F7 (characterization) — a halt STOPS the batch: commands after the refused move are not
    # applied and cannot change the report. Same prefix "mm" from (4, 0) facing E in Grid(5)
    # refuses at index 1 (x=6); every tail yields the identical Halted(last good, 1, "m").
    # Tails include turns, more moves, and moves that would refuse again. Green on arrival;
    # bite proven by mutants (skip-and-continue; report the LAST refusal instead of the first).
    def test_a_halt_ignores_every_later_command(self):
        start = Rover(4, 0, Heading.E)
        expected = Halted(Rover(5, 0, Heading.E), 1, "m")
        for tail in ["", "lmm", "rrrmmmm", "mmmm", "lllm"]:
            with self.subTest(tail=tail):
                self.assertEqual(Grid(5).execute(start, "mm" + tail), expected)

    # F7 placement (red) — placing a rover that is OUTSIDE the grid is refused AT PLACEMENT, with
    # the rover and the bound named. Hardcoded anchor: (9, 9) is beyond Grid(5) on both axes.
    # (mars-rover.feature :: @f7 @placement "Placing a rover outside the grid is refused")
    def test_placing_a_rover_off_the_grid_is_refused(self):
        rover = Rover(9, 9, Heading.N)
        self.assertEqual(Grid(5).place(rover), OffGrid(rover, 5))

    # F7 placement (characterization) — an in-bounds rover is placed, and the PlacedRover wraps
    # that same rover. Interior cells incl. the origin (the landing site). Green on arrival; bite
    # proven by mutants (place always refuses).
    def test_placing_an_in_bounds_rover_succeeds(self):
        for rover in [Rover(0, 0, Heading.N), Rover(1, -2, Heading.S), Rover(-3, 4, Heading.W)]:
            with self.subTest(rover=rover):
                self.assertEqual(Grid(5).place(rover), Placed(PlacedRover(rover)))

    # F7 placement (characterization) — the edge is INCLUSIVE at placement too: edge cells and
    # all four corners are placed. Bite proven by the <= -> < mutant.
    def test_placing_on_the_edge_or_a_corner_succeeds(self):
        cases = [
            Rover(5, 0, Heading.E), Rover(-5, 3, Heading.W),
            Rover(2, 5, Heading.N), Rover(-1, -5, Heading.S),
            Rover(5, 5, Heading.N), Rover(-5, -5, Heading.S),
            Rover(-5, 5, Heading.E), Rover(5, -5, Heading.W),
        ]
        for rover in cases:
            with self.subTest(rover=rover):
                self.assertEqual(Grid(5).place(rover), Placed(PlacedRover(rover)))

    # F7 placement (characterization) — off the grid on ANY single side is refused (both signs,
    # both axes, one axis at a time), naming the rover and the bound. Bite proven by mutants
    # (x-check only / y-check only / no abs()).
    def test_placing_off_any_single_side_is_refused(self):
        cases = [
            Rover(6, 0, Heading.E), Rover(-6, 2, Heading.W),
            Rover(1, 6, Heading.N), Rover(-3, -6, Heading.S),
        ]
        for rover in cases:
            with self.subTest(rover=rover):
                self.assertEqual(Grid(5).place(rover), OffGrid(rover, 5))

    # F7 migration (red) — execute takes a PlacedRover and returns one: a completed batch carries
    # the FINAL PlacedRover. Hardcoded anchor: placed at (3, 0) facing E on Grid(5), "mm" ends at
    # (5, 0) — the inclusive edge. Built via place(), the real path.
    # (mars-rover.feature :: @f7 @placement — scenario to be added with the green)
    def test_execute_a_placed_rover_completes_with_a_placed_rover(self):
        grid = Grid(5)
        placed = grid.place(Rover(3, 0, Heading.E)).placed
        self.assertEqual(grid.execute(placed, "mm"),
                         Completed(PlacedRover(Rover(5, 0, Heading.E))))

    # F7 migration (red) — a PlacedRover whose batch leaves the grid is HALTED, and the halt
    # carries the last good PlacedRover (so Earth can re-plan from it without placing again).
    # Hardcoded anchor: placed at (3, 0) facing E on Grid(5); "mmm" reaches x=6 at index 2.
    def test_execute_a_placed_rover_halts_with_a_placed_rover(self):
        grid = Grid(5)
        placed = grid.place(Rover(3, 0, Heading.E)).placed
        self.assertEqual(grid.execute(placed, "mmm"),
                         Halted(PlacedRover(Rover(5, 0, Heading.E)), 2, "m"))


if __name__ == "__main__":
    unittest.main()
