import random
import unittest

from mars_rover import Heading, Rover


class MarsRoverTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
