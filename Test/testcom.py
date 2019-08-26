import unittest
from knot.space import Com, Axis


class TestCom(unittest.TestCase):

    def test_str(self):
        self.assertEqual(str(Com.N), "North", "Should be North")

    def test_opp(self):
        self.assertEqual(Com.N.opposite, Com.S, "Opposite of North is South")

    def test_opp_var(self):
        compass = Com.E
        self.assertEqual(compass.opposite, Com.W, "Opposite of East is West")

    def test_opp_all(self):
        answer = {Com.N: Com.S, Com.E: Com.W, Com.S: Com.N, Com.W: Com.E}
        for i in Com:
            self.assertEqual(i.opposite, answer[i], "Opposite should be " + str(answer[i]))

    def test_ccw(self):
        answer = {Com.N: Com.W, Com.E: Com.N, Com.S: Com.E, Com.W: Com.S}
        for i in Com:
            self.assertEqual(i.ccw, answer[i], "CCW Should be " + str(answer[i]))

    def test_cw(self):
        answer = {Com.N: Com.E, Com.E: Com.S, Com.S: Com.W, Com.W: Com.N}
        for i in Com:
            self.assertEqual(i.cw, answer[i], "CW Should be " + str(answer[i]))

    def test_axis(self):
        answer = {Com.N: Axis.NS, Com.E: Axis.EW, Com.S: Axis.NS, Com.W: Axis.EW}
        for i in Com:
            self.assertEqual(i.axis, answer[i], "Axis of " + str(i) + " should be " + str(answer[i]))

    def test_axes(self):
        ans_a = {Axis.NS: Com.N, Axis.EW: Com.E}
        ans_b = {Axis.NS: Com.S, Axis.EW: Com.W}
        for i in Axis:
            self.assertEqual(ans_a[i], i.a, "Axis of " + str(i) + " should be " + str(ans_a[i]))
            self.assertEqual(ans_b[i], i.b, "Axis of " + str(i) + " should be " + str(ans_b[i]))


if __name__ == '__main__':
    unittest.main()
