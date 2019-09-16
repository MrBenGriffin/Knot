import unittest
from knot.tool import Setting, Cut, DummyRng


class TestSetting(unittest.TestCase):
    # zoomorph_balance;  0 = All twists, 1000=all Zoomorphs.
    # straights_balance; 0 = All twists, 1000=all Straights
    # (0,0): all twists, (1000, X) all straights, (0,1000) is all zoo

    def test_choose(self):
        sample = (Setting(1.0, 0), Setting(1.0, 1.0), Setting(0, 0), Setting(0, 0.5), Setting(0, 1.0),  Setting(.15, 0.5))
        answers = (
            #    0      1      2      3      4      5      6      7      8      9
            (Cut.I, Cut.I, Cut.I, Cut.I, Cut.I, Cut.I, Cut.I, Cut.I, Cut.I, Cut.I),  # 0
            (Cut.I, Cut.I, Cut.I, Cut.I, Cut.I, Cut.I, Cut.I, Cut.I, Cut.I, Cut.I),  # 1
            (Cut.X, Cut.X, Cut.X, Cut.X, Cut.X, Cut.X, Cut.X, Cut.X, Cut.X, Cut.X),  # 2
            (Cut.H, Cut.X, Cut.B, Cut.X, Cut.X, Cut.H, Cut.X, Cut.B, Cut.X, Cut.X),  # 3
            (Cut.H, Cut.B, Cut.H, Cut.B, Cut.H, Cut.B, Cut.H, Cut.B, Cut.H, Cut.B),  # 4
            (Cut.I, Cut.X, Cut.X, Cut.I, Cut.X, Cut.X, Cut.I, Cut.X, Cut.X, Cut.I)   # 5
         )
        for i in range(len(sample)):
            setting = sample[i]
            setting.rng = DummyRng(0)
            answer = answers[i]
            for j in range(10):
                self.assertEqual(answer[j], setting.choose(), str(i)+str(j) + " Choice should have been " + str(answer[j]))


if __name__ == '__main__':
    unittest.main()
