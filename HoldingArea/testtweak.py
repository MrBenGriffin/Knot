import unittest

from knot.space import Tweak, Wallpaper, Com, Dim


class TestTweak(unittest.TestCase):
    tweaks = (Wallpaper.master, Wallpaper.sunset, Wallpaper.vanity, Wallpaper.mirror, Wallpaper.rot000, Wallpaper.rot090, Wallpaper.rot270, Wallpaper.rot180)
    coms = (Com.S, Com.W, Com.N, Com.E)

    def test_str(self):
        self.assertEqual(str(Tweak(Wallpaper.sunset, Dim(4, 4))), "Horizon", "Should be Horizon")

    def test_repr(self):
        self.assertEqual(repr(Tweak(Wallpaper.sunset, Dim(3, 4))), "Horizon; Dim(x=2, y=3)", "Should be Horizon; Dim(x=2, y=3)")

    def test_face(self):
        answer_set = {
            Wallpaper.master: {Com.S: Com.S, Com.W: Com.W, Com.N: Com.N, Com.E: Com.E},
            Wallpaper.sunset: {Com.S: Com.N, Com.W: Com.W, Com.N: Com.S, Com.E: Com.E},
            Wallpaper.vanity: {Com.S: Com.S, Com.W: Com.E, Com.N: Com.N, Com.E: Com.W},
            Wallpaper.mirror: {Com.S: Com.N, Com.W: Com.E, Com.N: Com.S, Com.E: Com.W},
            Wallpaper.rot000: {Com.S: Com.S, Com.W: Com.W, Com.N: Com.N, Com.E: Com.E},
            Wallpaper.rot090: {Com.S: Com.W, Com.W: Com.N, Com.N: Com.E, Com.E: Com.S},
            Wallpaper.rot270: {Com.S: Com.E, Com.W: Com.S, Com.N: Com.W, Com.E: Com.N},
            Wallpaper.rot180: {Com.S: Com.N, Com.W: Com.E, Com.N: Com.S, Com.E: Com.W}
        }
        for tweak in self.tweaks:
            test = Tweak(tweak, Dim(2, 2))
            for com in self.coms:
                self.assertEqual(test.face(com), answer_set[tweak][com], "Face " + str(tweak) + ":" + str(com) + " expected " + str(answer_set[tweak][com]))
            test = Tweak(tweak, Dim(3, 3))
            for com in self.coms:
                self.assertEqual(test.face(com), answer_set[tweak][com], "Face " + str(tweak) + ":" + str(com) + " expected " + str(answer_set[tweak][com]))

    def test_dim_even(self):
        answers = {
            Wallpaper.master:  (Dim(0, 0), Dim(0, 1), Dim(1, 0), Dim(1, 1)),
            Wallpaper.sunset: (Dim(0, 1), Dim(0, 0), Dim(1, 1), Dim(1, 0)),
            Wallpaper.vanity:  (Dim(1, 0), Dim(1, 1), Dim(0, 0), Dim(0, 1)),
            Wallpaper.mirror:  (Dim(1, 1), Dim(1, 0), Dim(0, 1), Dim(0, 0)),
            Wallpaper.rot000:  (Dim(0, 0), Dim(0, 1), Dim(1, 0), Dim(1, 1)),
            Wallpaper.rot090:  (Dim(0, 1), Dim(1, 1), Dim(0, 0), Dim(1, 0)),
            Wallpaper.rot270:  (Dim(1, 0), Dim(0, 0), Dim(1, 1), Dim(0, 1)),
            Wallpaper.rot180:  (Dim(1, 1), Dim(1, 0), Dim(0, 1), Dim(0, 0))
        }
        for x in range(2):
            for y in range(2):
                dxy = Dim(x, y)
                for tweak in self.tweaks:
                    test = Tweak(tweak, Dim(2, 2))
                    part_a = test.dim(dxy)
                    part_b = answers[tweak][x*2+y]
                    message = "Dim " + str(tweak) + ":" + str(dxy) + " expected " + str(answers[tweak][x*2+y])
                    self.assertEqual(part_a, part_b, message)

    def test_dim_odd(self):
        answers = {
            Wallpaper.master:  (Dim(0, 0), Dim(0, 1), Dim(0, 2), Dim(1, 0), Dim(1, 1), Dim(1, 2), Dim(2, 0), Dim(2, 1), Dim(2, 2)),
            Wallpaper.sunset: (Dim(0, 2), Dim(0, 1), Dim(0, 0), Dim(1, 2), Dim(1, 1), Dim(1, 0), Dim(2, 2), Dim(2, 1), Dim(2, 0)),
            Wallpaper.vanity:  (Dim(2, 0), Dim(2, 1), Dim(2, 2), Dim(1, 0), Dim(1, 1), Dim(1, 2), Dim(0, 0), Dim(0, 1), Dim(0, 2)),
            Wallpaper.mirror:  (Dim(2, 2), Dim(2, 1), Dim(2, 0), Dim(1, 2), Dim(1, 1), Dim(1, 0), Dim(0, 2), Dim(0, 1), Dim(0, 0)),
            Wallpaper.rot000:  (Dim(0, 0), Dim(0, 1), Dim(0, 2), Dim(1, 0), Dim(1, 1), Dim(1, 2), Dim(2, 0), Dim(2, 1), Dim(2, 2)),
            Wallpaper.rot180:  (Dim(2, 2), Dim(2, 1), Dim(2, 0), Dim(1, 2), Dim(1, 1), Dim(1, 0), Dim(0, 2), Dim(0, 1), Dim(0, 0)),
            Wallpaper.rot090:  (Dim(0, 2), Dim(1, 2), Dim(2, 2), Dim(0, 1), Dim(1, 1), Dim(2, 1), Dim(0, 0), Dim(1, 0), Dim(2, 0)),
            Wallpaper.rot270:  (Dim(2, 0), Dim(1, 0), Dim(0, 0), Dim(2, 1), Dim(1, 1), Dim(0, 1), Dim(2, 2), Dim(1, 2), Dim(0, 2))
        }
        for x in range(3):
            for y in range(3):
                dim = Dim(x, y)
                for tweak in self.tweaks:
                    test = Tweak(tweak, Dim(3, 3))
                    self.assertEqual(test.dim(dim), answers[tweak][x * 3 + y], "Dim " + str(tweak) + ":" + str(dim) + " expected " + str(answers[tweak][x * 3 + y]))

    def test_entry(self):
        ans0 = {
            Wallpaper.master:  {4: {4: Dim(2, 2), 5: Dim(2, 2)}, 5: {4: Dim(2, 2), 5: Dim(2, 2)}},
            Wallpaper.sunset: {4: {4: Dim(2, 1), 5: Dim(2, 2)}, 5: {4: Dim(2, 1), 5: Dim(2, 2)}},
            Wallpaper.vanity:  {4: {4: Dim(1, 2), 5: Dim(1, 2)}, 5: {4: Dim(2, 2), 5: Dim(2, 2)}},
            Wallpaper.mirror:  {4: {4: Dim(1, 1), 5: Dim(1, 2)}, 5: {4: Dim(2, 1), 5: Dim(2, 2)}},
            Wallpaper.rot000:  {4: {4: Dim(2, 2), 5: Dim(2, 2)}, 5: {4: Dim(2, 2), 5: Dim(2, 2)}},
            Wallpaper.rot090:  {4: {4: Dim(2, 1), 5: Dim(2, 2)}, 5: {4: Dim(2, 1), 5: Dim(2, 2)}},
            Wallpaper.rot180:  {4: {4: Dim(1, 1), 5: Dim(1, 2)}, 5: {4: Dim(2, 1), 5: Dim(2, 2)}},
            Wallpaper.rot270:  {4: {4: Dim(1, 2), 5: Dim(1, 2)}, 5: {4: Dim(2, 2), 5: Dim(2, 2)}}
        }
        ans23 = {
            Wallpaper.master:  {4: {4: Dim(2, 1), 5: Dim(2, 1)}, 5: {4: Dim(2, 1), 5: Dim(2, 1)}},
            Wallpaper.sunset: {4: {4: Dim(2, 2), 5: Dim(2, 3)}, 5: {4: Dim(2, 2), 5: Dim(2, 3)}},
            Wallpaper.vanity:  {4: {4: Dim(1, 1), 5: Dim(1, 1)}, 5: {4: Dim(2, 1), 5: Dim(2, 1)}},
            Wallpaper.mirror:  {4: {4: Dim(1, 2), 5: Dim(1, 3)}, 5: {4: Dim(2, 2), 5: Dim(2, 3)}},
            Wallpaper.rot000:  {4: {4: Dim(2, 1), 5: Dim(2, 1)}, 5: {4: Dim(2, 1), 5: Dim(2, 1)}},
            Wallpaper.rot090:  {4: {4: Dim(1, 1), 5: Dim(1, 2)}, 5: {4: Dim(1, 1), 5: Dim(1, 2)}},
            Wallpaper.rot180:  {4: {4: Dim(1, 2), 5: Dim(1, 3)}, 5: {4: Dim(2, 2), 5: Dim(2, 3)}},
            Wallpaper.rot270:  {4: {4: Dim(2, 2), 5: Dim(2, 2)}, 5: {4: Dim(3, 2), 5: Dim(3, 2)}}
        }
        for tweak in self.tweaks:
            for x in range(4, 6):
                for y in range(4, 6):
                    test = Tweak(tweak, Dim(x, y))
                    answer0 = ans0[tweak][x][y]
                    self.assertEqual(answer0, test.entry(0), str(tweak) + ";" + str(x) + "," + str(y) + ",0: got " + str(test.entry(0)) + " expected " + str(answer0))
                    answer2 = ans23[tweak][x][y]
                    self.assertEqual(answer2, test.entry(2), str(tweak) + ";" + str(x) + "," + str(y) + ",2: got " + str(test.entry(2)) + " expected " + str(answer2))
                    answer3 = ans23[tweak][x][y]
                    self.assertEqual(answer3, test.entry(3), str(tweak) + ";" + str(x) + "," + str(y) + ",3: got" + str(test.entry(3)) + " expected " + str(answer3))
                    answer4 = ans0[tweak][x][y]
                    self.assertEqual(answer4, test.entry(4), str(tweak) + ";" + str(x) + "," + str(y) + ",4: got" + str(test.entry(4)) + " expected " + str(answer4))


if __name__ == '__main__':
    unittest.main()
