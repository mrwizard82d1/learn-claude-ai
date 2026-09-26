import random
import unittest

from string_calculator import add


# Test ideas (seeds for thinking — ideas, NOT promises).
# Discipline: "not done until each idea is implemented OR consciously dropped";
# but an idea may be dropped/changed as the design teaches us something.
#   [x] empty string           -> 0
#   [x] single number          -> its value        ("1" -> 1, "5" -> 5)
#   [x] two numbers, comma      -> sum              ("1,2" -> 3)
#   [ ] arbitrary count of numbers, comma-separated
#   [ ] newline as a delimiter too                  ("1\n2,3" -> 6)
#   [ ] custom delimiter header                     ("//;\n1;2" -> 3)
#   [~] negatives -> raise: DROPPED (physics, not banking — negatives carry
#       information; they are ordinary values and simply sum)
#   [ ] numbers > 1000 ignored
#   ?  open questions (park, decide when reached): surrounding whitespace?
#      trailing/leading delimiter? empty between delimiters? non-numeric input?
class StringCalculatorTests(unittest.TestCase):
    def test_empty_string_returns_zero(self):
        self.assertEqual(add(""), 0)

    def test_single_number_returns_its_value(self):
        # NOTE: the random negative here will conflict with the future
        # "negatives raise" idea — we'll consciously evolve this test then.
        cases = [
            random.randint(1, 1000),     # random positive
            0,                           # zero
            random.randint(-1000, -1),   # random negative
        ]
        for n in cases:
            with self.subTest(n=n):
                self.assertEqual(add(str(n)), n)

    def test_two_numbers_comma_separated_are_summed(self):
        # (a, b) table — see agreed case list. Negatives here are knowingly
        # temporary: the future "negatives raise" idea will rewrite rows 5-6.
        pairs = [
            (random.randint(1, 1000), random.randint(1, 1000)),    # both positive
            (0, random.randint(1, 1000)),                          # zero first
            (random.randint(1, 1000), 0),                          # zero second
            (0, 0),                                                # both zero
            (random.randint(-1000, -1), random.randint(1, 1000)),  # one negative
            (random.randint(-1000, -1), random.randint(-1000, -1)),# both negative
        ]
        for a, b in pairs:
            text = f"{a},{b}"
            with self.subTest(text=text, expected=a + b):
                self.assertEqual(add(text), a + b)

    def test_negatives_are_summed_not_rejected(self):
        # DECISION (physics, not banking): negative numbers are real and carry
        # information, so the kata's "reject negatives" idea (#7) is consciously
        # DROPPED. Negatives are ordinary values and simply sum.
        self.assertEqual(add("1,-2,3,-4"), 1 - 2 + 3 - 4)  # == -2


if __name__ == "__main__":
    unittest.main()
