# To run tests, navigate to the top-level directory of
# the codebase and run:
#    python -m unittest
import unittest
import unittest.mock as mock

from dicegame.die import Die


class TestDie(unittest.TestCase):

    def test_valid(self):
        """Check all dice are between 1 and 6"""
        valid_values = list(range(1, 7))
        for i in range(100):
            d = Die()
            self.assertIn(d.value, valid_values)
        

if __name__ == "__main__":
    unittest.main()