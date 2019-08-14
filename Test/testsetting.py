import unittest
import random
from knot.tool import Setting, Cut


class TestSetting(unittest.TestCase):
    sample = (Setting(0, 0), Setting(1000, 0), Setting(0, 1000), Setting(1000, 1000), Setting(500, 500), Setting())

    def test_choose(self):
        answers = (
            (Cut.I, Cut.I, Cut.I, Cut.I, Cut.I, Cut.I, Cut.I, Cut.I, Cut.I, Cut.I),
            (Cut.X, Cut.X, Cut.X, Cut.X, Cut.X, Cut.X, Cut.X, Cut.X, Cut.X, Cut.X),
            (Cut.I, Cut.I, Cut.I, Cut.I, Cut.I, Cut.I, Cut.I, Cut.I, Cut.I, Cut.I),
            (Cut.B, Cut.H, Cut.B, Cut.B, Cut.B, Cut.B, Cut.B, Cut.B, Cut.B, Cut.B),
            (Cut.I, Cut.I, Cut.I, Cut.I, Cut.X, Cut.I, Cut.I, Cut.X, Cut.I, Cut.B),
            (Cut.I, Cut.I, Cut.I, Cut.I, Cut.I, Cut.I, Cut.I, Cut.I, Cut.X, Cut.I)
        )
        for i in range(len(self.sample)):
            random.seed(1337)
            answer = answers[i]
            for j in range(10):
                self.assertEqual(self.sample[i].choose(), answer[j], str(i)+str(j) + " Choice should have been " + str(answer[j]))


if __name__ == '__main__':
    unittest.main()
