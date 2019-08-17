import unittest
from knot.tool import DummyRng


class TestDummyRng(unittest.TestCase):

    def test_random(self):
        rng = DummyRng()
        for i in (0.0, 0.25, 0.5, 0.75, 1.0):
            result = rng.random()
            expect = i
            self.assertEqual(result, expect, "rng " + str(result) + " was expecting " + str(expect))

    def test_choice(self):
        rng = DummyRng()
        seq = (1, 2)
        for i in range(5):
            result = rng.choice(seq)
            expect = (i % 2)+1
            self.assertEqual(result, expect, "rng " + str(result) + " was expecting " + str(expect))

    def test_seed(self):
        rng = DummyRng()
        for i in range(5):
            rng.seed(0)
            result = rng.random()
            expect = 0.0
            self.assertEqual(result, expect, "rng " + str(result) + " was expecting 0")


if __name__ == '__main__':
    unittest.main()
