import unittest
from knot.space.crs import Symmetry
from knot.space.rectilinear import Com
from knot.space.rectilinear.square import Paper


class TestAxes(unittest.TestCase):

    def test_ccw(self):
        answer = {Com.N: Com.W, Com.E: Com.N, Com.S: Com.E, Com.W: Com.S}
        for i in Com:
            self.assertEqual(i.ccw, answer[i], "CCW Should be " + str(answer[i]))

    def test_cw(self):
        answer = {Com.N: Com.E, Com.E: Com.S, Com.S: Com.W, Com.W: Com.N}
        for i in Com:
            self.assertEqual(i.cw, answer[i], "CW Should be " + str(answer[i]))

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
