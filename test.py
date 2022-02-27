import unittest

from lexing import utils


class TestConstraints(unittest.TestCase):
    def test_constraints_integer_or_float(self):
        """Tests constraints with lexing a region of either an integer or a float."""
        self.assertEqual(
            utils.Has(".", occurrences=1) | utils.Has(int),
            utils.Constraint({"constraint": ".", "occurrences": 1}, {"constraint": int, "occurrences": None})
        )


if __name__ == '__main__':
    unittest.main()
