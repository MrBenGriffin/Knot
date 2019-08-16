import unittest
from knot.space import Com, Axis


class TestCom(unittest.TestCase):
    sample = (Com.N, Com.E, Com.S, Com.W, Com.C, Com.F)

    def test_str(self):
        self.assertEqual(str(Com.N), "North", "Should be North")

    def test_opp(self):
        self.assertEqual(Com.N.opposite, Com.S, "Opposite of North is South")

    def test_opp_var(self):
        compass = Com.E
        self.assertEqual(compass.opposite, Com.W, "Opposite of East is West")

    def test_opp_all(self):
        answer = (Com.S, Com.W, Com.N, Com.E, Com.F, Com.C)
        for i in range(len(self.sample)):
            self.assertEqual(self.sample[i].opposite, answer[i], "Opposite should be " + str(answer[i]))

    def test_ccw(self):
        answer = (Com.W, Com.N, Com.E, Com.S, Com.F, Com.C)
        for i in range(len(self.sample)):
            self.assertEqual(self.sample[i].ccw, answer[i], "CCW Should be " + str(answer[i]))

    def test_cw(self):
        answer = (Com.E, Com.S, Com.W, Com.N, Com.F, Com.C)
        for i in range(len(self.sample)):
            self.assertEqual(self.sample[i].cw, answer[i], "CW Should be " + str(answer[i]))

    def test_axis(self):
        #        ( Com.N,   Com.E,   Com.S,   Com.W,   Com.C,   Com.F)
        answer = (Axis.NS, Axis.EW, Axis.NS, Axis.EW, Axis.CF, Axis.CF)
        for i in range(len(self.sample)):
            self.assertEqual(self.sample[i].axis, answer[i], "Axis of " + str(i) + " should be " + str(answer[i]))

    def test_axes(self):
        sample = (Axis.NS, Axis.EW, Axis.CF)
        ans_a = (Com.N, Com.E, Com.C)
        ans_b = (Com.S, Com.W, Com.F)
        for i in range(len(sample)):
            self.assertEqual(ans_a[i], sample[i].a, "Axis of " + str(i) + " should be " + str(ans_a[i]))
            self.assertEqual(ans_b[i], sample[i].b, "Axis of " + str(i) + " should be " + str(ans_b[i]))


if __name__ == '__main__':
    unittest.main()
