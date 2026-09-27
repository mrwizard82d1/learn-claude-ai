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


if __name__ == "__main__":
    unittest.main()
