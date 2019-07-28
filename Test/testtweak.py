import unittest
from Maze.tweak import Tweak, Tw
from Maze.com import Com
from Maze.util import Dim


class TestTweak(unittest.TestCase):
    tweaks = (Tw.master, Tw.horizon, Tw.vanity, Tw.mirror, Tw.rot000, Tw.rot090, Tw.rot270, Tw.rot180)
    coms = (Com.S, Com.W, Com.N, Com.E)

    def test_str(self):
        self.assertEqual(str(Tweak(Tw.horizon, 4, 4)), "Horizon", "Should be Horizon")

    def test_face(self):
        answer_set = {
            Tw.master: {Com.S: Com.S, Com.W: Com.W, Com.N: Com.N, Com.E: Com.E},
            Tw.horizon: {Com.S: Com.N, Com.W: Com.W, Com.N: Com.S, Com.E: Com.E},
            Tw.vanity: {Com.S: Com.S, Com.W: Com.E, Com.N: Com.N, Com.E: Com.W},
            Tw.mirror: {Com.S: Com.N, Com.W: Com.E, Com.N: Com.S, Com.E: Com.W},
            Tw.rot000: {Com.S: Com.S, Com.W: Com.W, Com.N: Com.N, Com.E: Com.E},
            Tw.rot090: {Com.S: Com.W, Com.W: Com.N, Com.N: Com.E, Com.E: Com.S},
            Tw.rot270: {Com.S: Com.E, Com.W: Com.S, Com.N: Com.W, Com.E: Com.N},
            Tw.rot180: {Com.S: Com.N, Com.W: Com.E, Com.N: Com.S, Com.E: Com.W}
        }
        for tweak in self.tweaks:
            test = Tweak(tweak, 2, 2)
            for com in self.coms:
                self.assertEqual(test.face(com), answer_set[tweak][com], "Face " + str(tweak) + ":" + str(com) + " expected " + str(answer_set[tweak][com]))
            test = Tweak(tweak, 3, 3)
            for com in self.coms:
                self.assertEqual(test.face(com), answer_set[tweak][com], "Face " + str(tweak) + ":" + str(com) + " expected " + str(answer_set[tweak][com]))

    def test_dim_even(self):
        answers = {
            Tw.master:  (Dim(0, 0), Dim(0, 1), Dim(1, 0), Dim(1, 1)),
            Tw.horizon: (Dim(0, 1), Dim(0, 0), Dim(1, 1), Dim(1, 0)),
            Tw.vanity:  (Dim(1, 0), Dim(1, 1), Dim(0, 0), Dim(0, 1)),
            Tw.mirror:  (Dim(1, 1), Dim(1, 0), Dim(0, 1), Dim(0, 0)),
            Tw.rot000:  (Dim(0, 0), Dim(0, 1), Dim(1, 0), Dim(1, 1)),
            Tw.rot090:  (Dim(0, 1), Dim(1, 1), Dim(0, 0), Dim(1, 0)),
            Tw.rot270:  (Dim(1, 0), Dim(0, 0), Dim(1, 1), Dim(0, 1)),
            Tw.rot180:  (Dim(1, 1), Dim(1, 0), Dim(0, 1), Dim(0, 0))
        }
        for x in range(2):
            for y in range(2):
                dim = Dim(x, y)
                for tweak in self.tweaks:
                    test = Tweak(tweak, 2, 2)
                    self.assertEqual(test.dim(dim), answers[tweak][x*2+y], "Dim " + str(tweak) + ":" + str(dim) + " expected " + str(answers[tweak][x*2+y]))

    def test_dim_odd(self):
        answers = {
            Tw.master:  (Dim(0, 0), Dim(0, 1), Dim(0, 2), Dim(1, 0), Dim(1, 1), Dim(1, 2), Dim(2, 0), Dim(2, 1), Dim(2, 2)),
            Tw.horizon: (Dim(0, 2), Dim(0, 1), Dim(0, 0), Dim(1, 2), Dim(1, 1), Dim(1, 0), Dim(2, 2), Dim(2, 1), Dim(2, 0)),
            Tw.vanity:  (Dim(2, 0), Dim(2, 1), Dim(2, 2), Dim(1, 0), Dim(1, 1), Dim(1, 2), Dim(0, 0), Dim(0, 1), Dim(0, 2)),
            Tw.mirror:  (Dim(2, 2), Dim(2, 1), Dim(2, 0), Dim(1, 2), Dim(1, 1), Dim(1, 0), Dim(0, 2), Dim(0, 1), Dim(0, 0)),
            Tw.rot000:  (Dim(0, 0), Dim(0, 1), Dim(0, 2), Dim(1, 0), Dim(1, 1), Dim(1, 2), Dim(2, 0), Dim(2, 1), Dim(2, 2)),
            Tw.rot180:  (Dim(2, 2), Dim(2, 1), Dim(2, 0), Dim(1, 2), Dim(1, 1), Dim(1, 0), Dim(0, 2), Dim(0, 1), Dim(0, 0)),
            Tw.rot090:  (Dim(0, 2), Dim(1, 2), Dim(2, 2), Dim(0, 1), Dim(1, 1), Dim(2, 1), Dim(0, 0), Dim(1, 0), Dim(2, 0)),
            Tw.rot270:  (Dim(2, 0), Dim(1, 0), Dim(0, 0), Dim(2, 1), Dim(1, 1), Dim(0, 1), Dim(2, 2), Dim(1, 2), Dim(0, 2))
       }
        for x in range(3):
            for y in range(3):
                dim = Dim(x, y)
                for tweak in self.tweaks:
                    test = Tweak(tweak, 3, 3)
                    self.assertEqual(test.dim(dim), answers[tweak][x*3+y], "Dim " + str(tweak) + ":" + str(dim) + " expected " + str(answers[tweak][x*3+y]))


if __name__ == '__main__':
    unittest.main()
