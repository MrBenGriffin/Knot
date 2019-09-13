import unittest
from knot.space.crs import Symmetry
from knot.space.square.axes import Com, Axis, Paper


class TestAxes(unittest.TestCase):

    def test_axes_str(self):
        self.assertEqual(str(Axis.NS), "NS", "Should be NS")

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

    def test_paper_str(self):
        answer = {Paper.master: "Master", Paper.sunset: "Sunset",
                  Paper.vanity: "Vanity", Paper.mirror: "Mirror", Paper.rotate: "Rotate"}
        for item in Paper:
            self.assertEqual(str(item), answer[item], "Should be " + answer[item])

    def test_paper_identity(self):
        self.assertEqual(Paper.identity(), Paper.master, "Should be master")

    def test_paper_select(self):
        answer = {"N": "Master", "H": "Sunset",
                  "V": "Vanity", "F": "Mirror", "R": "Rotate"}
        for item in Symmetry.choices():
            self.assertEqual(str(Paper.select(item)), answer[item], "Should be " + answer[item])


if __name__ == '__main__':
    unittest.main()
