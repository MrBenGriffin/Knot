import unittest
from knot.space.rectilinear.axes import Com
from knot.space.rectilinear.dim import Dim
from knot.space.rectilinear.rectangle import Paper, Tweak


class TestTweak(unittest.TestCase):
    workers = ((Paper.master, 0), (Paper.sunset, 1), (Paper.vanity, 1), (Paper.mirror, 1))

    def test_str(self):
        answer = "Sunset w1"
        tw_str = str(Tweak(Paper.sunset, (4, 4), 1))
        self.assertEqual(tw_str, answer, "Should be " + answer)

    def test_repr(self):
        answer = "Sunset w1; under (2,3)"
        tw_repr = repr(Tweak(Paper.sunset, (3, 4), 1))
        self.assertEqual(tw_repr, answer, "Should be " + answer)

    def test_face(self):
        answer_set = {
            (Paper.master, 0): {Com.S: Com.S, Com.W: Com.W, Com.N: Com.N, Com.E: Com.E},
            (Paper.sunset, 1): {Com.S: Com.N, Com.W: Com.W, Com.N: Com.S, Com.E: Com.E},
            (Paper.vanity, 1): {Com.S: Com.S, Com.W: Com.E, Com.N: Com.N, Com.E: Com.W},
            (Paper.mirror, 1): {Com.S: Com.N, Com.W: Com.E, Com.N: Com.S, Com.E: Com.W}
        }
        for tweak in self.workers:
            test = Tweak(tweak[0], (2, 2), tweak[1])
            for com in Com:
                answer = answer_set[tweak][com]
                result = test.face(com)
                self.assertEqual(result, answer,
                                 "Under (2,2); Face " + str(tweak) + ":" + str(com) + " expected " + str(answer))
            test = Tweak(tweak[0], (3, 3), tweak[1])
            for com in Com:
                answer = answer_set[tweak][com]
                result = test.face(com)
                self.assertEqual(result, answer,
                                 "Under (3,3); Face " + str(tweak) + ":" + str(com) + " expected " + str(answer))

    def tweak_test(self, tweak: tuple, basis: tuple, dim: tuple, offset: int, answers: dict):
        tweaks = str(tweak[0]) + ' w' + str(tweak[1]) + " under " + str(basis) + " for " + str(dim) + "; expected:"
        test = Tweak(tweak[0], basis, tweak[1])
        part_a = test.dim(dim)
        part_b = (answers[tweak])[offset]
        self.assertEqual(part_a, part_b, tweaks + str(part_b) + ", found: " + str(part_a))

    def test_dim_even(self):
        answers = {
            (Paper.master, 0): (Dim(0, 0), Dim(0, 1), Dim(1, 0), Dim(1, 1)),
            (Paper.sunset, 1): (Dim(0, 1), Dim(0, 0), Dim(1, 1), Dim(1, 0)),
            (Paper.vanity, 1): (Dim(1, 0), Dim(1, 1), Dim(0, 0), Dim(0, 1)),
            (Paper.mirror, 1): (Dim(1, 1), Dim(1, 0), Dim(0, 1), Dim(0, 0))
        }
        basis = (2, 2)
        for x in range(2):
            for y in range(2):
                dim = tuple((x, y))
                for tweak in self.workers:
                    self.tweak_test(tweak, basis, dim, x*2+y, answers)

    def test_dim_odd(self):
        answers = {
            (Paper.master, 0): (Dim(0, 0), Dim(0, 1), Dim(0, 2), Dim(1, 0), Dim(1, 1), Dim(1, 2), Dim(2, 0), Dim(2, 1), Dim(2, 2)),
            (Paper.sunset, 1): (Dim(0, 2), Dim(0, 1), Dim(0, 0), Dim(1, 2), Dim(1, 1), Dim(1, 0), Dim(2, 2), Dim(2, 1), Dim(2, 0)),
            (Paper.vanity, 1): (Dim(2, 0), Dim(2, 1), Dim(2, 2), Dim(1, 0), Dim(1, 1), Dim(1, 2), Dim(0, 0), Dim(0, 1), Dim(0, 2)),
            (Paper.mirror, 1): (Dim(2, 2), Dim(2, 1), Dim(2, 0), Dim(1, 2), Dim(1, 1), Dim(1, 0), Dim(0, 2), Dim(0, 1), Dim(0, 0))
        }
        basis = (3, 3)
        for x in range(3):
            for y in range(3):
                dim = tuple((x, y))
                for tweak in self.workers:
                    self.tweak_test(tweak, basis, dim, x*3+y, answers)

    def test_entry(self):
        answers = {
            0: {
                (Paper.master, 0): {4: Dim(2, 2), 5: Dim(2, 2), 6: Dim(3, 3)},
                (Paper.sunset, 1): {4: Dim(2, 1), 5: Dim(2, 2), 6: Dim(3, 2)},
                (Paper.vanity, 1): {4: Dim(1, 2), 5: Dim(2, 2), 6: Dim(2, 3)},
                (Paper.mirror, 1): {4: Dim(1, 1), 5: Dim(2, 2), 6: Dim(2, 2)},
            },
            1: {
                (Paper.master, 0): {4: Dim(2, 0), 5: Dim(2, 0), 6: Dim(3, 0)},
                (Paper.sunset, 1): {4: Dim(2, 3), 5: Dim(2, 4), 6: Dim(3, 5)},
                (Paper.vanity, 1): {4: Dim(1, 0), 5: Dim(2, 0), 6: Dim(2, 0)},
                (Paper.mirror, 1): {4: Dim(1, 3), 5: Dim(2, 4), 6: Dim(2, 5)},
            },
            2: {
                (Paper.master, 0): {4: Dim(2, 1), 5: Dim(2, 1), 6: Dim(3, 1)},
                (Paper.sunset, 1): {4: Dim(2, 2), 5: Dim(2, 3), 6: Dim(3, 4)},
                (Paper.vanity, 1): {4: Dim(1, 1), 5: Dim(2, 1), 6: Dim(2, 1)},
                (Paper.mirror, 1): {4: Dim(1, 2), 5: Dim(2, 3), 6: Dim(2, 4)},
            },
            3: {
                (Paper.master, 0): {4: Dim(2, 1), 5: Dim(2, 1), 6: Dim(3, 1)},
                (Paper.sunset, 1): {4: Dim(2, 2), 5: Dim(2, 3), 6: Dim(3, 4)},
                (Paper.vanity, 1): {4: Dim(1, 1), 5: Dim(2, 1), 6: Dim(2, 1)},
                (Paper.mirror, 1): {4: Dim(1, 2), 5: Dim(2, 3), 6: Dim(2, 4)},
            },
            4: {
                (Paper.master, 0): {4: Dim(2, 2), 5: Dim(2, 2), 6: Dim(3, 2)},
                (Paper.sunset, 1): {4: Dim(2, 1), 5: Dim(2, 2), 6: Dim(3, 3)},
                (Paper.vanity, 1): {4: Dim(1, 2), 5: Dim(2, 2), 6: Dim(2, 2)},
                (Paper.mirror, 1): {4: Dim(1, 1), 5: Dim(2, 2), 6: Dim(2, 3)},
            },
        }
        for border in range(5):
            for tweak in self.workers:
                for sz in range(4, 7):
                    basis = tuple((sz, sz))
                    test = Tweak(tweak[0], basis, tweak[1])
                    tweaks = str(tweak[0]) + ' w' + str(tweak[1]) + " in " + str(basis) + " with border " + str(border)
                    ace = (answers[border])[tweak][sz]
                    act = test.entry(border)
                    self.assertEqual(act, ace, tweaks + ": got " + str(act) + " expected " + str(ace))


if __name__ == '__main__':
    unittest.main()
