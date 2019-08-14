import unittest
from knot.space import Com


class TestCom(unittest.TestCase):
    sample = (Com.N, Com.E, Com.S, Com.W, Com.C, Com.F, Com.X)

    def test_str(self):
        self.assertEqual(str(Com.N), "North", "Should be North")

    def test_opp(self):
        self.assertEqual(Com.N.opposite, Com.S, "Opposite of North is South")

    def test_opp_var(self):
        compass = Com.E
        self.assertEqual(compass.opposite, Com.W, "Opposite of East is West")

    def test_opp_all(self):
        answer = (Com.S, Com.W, Com.N, Com.E, Com.F, Com.C, Com.X)
        for i in range(len(self.sample)):
            self.assertEqual(self.sample[i].opposite, answer[i], "Opposite should be " + str(answer[i]))

    def test_ccw(self):
        answer = (Com.W, Com.N, Com.E, Com.S, Com.F, Com.C, Com.X)
        for i in range(len(self.sample)):
            self.assertEqual(self.sample[i].ccw, answer[i], "CCW Should be " + str(answer[i]))

    def test_cw(self):
        answer = (Com.E, Com.S, Com.W, Com.N, Com.F, Com.C, Com.X)
        for i in range(len(self.sample)):
            self.assertEqual(self.sample[i].cw, answer[i], "CW Should be " + str(answer[i]))


if __name__ == '__main__':
    unittest.main()
