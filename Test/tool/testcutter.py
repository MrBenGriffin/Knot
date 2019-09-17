import unittest
from knot.tool import Cutter, DummyRng
from knot.space.rectilinear.square import Square
from knot.tool.setting import Setting
from knot.tool.cut import Cut


class TestCutter(unittest.TestCase):

    def setUp(self):
        self.shape = Square()
        self.axes = self.shape.axis()
        self.paper = self.shape.paper()
        # Currently only tests against SQUARE.
        # Setting 0 : straights_balance; 0 = All twists, 1000=all Straights
        # Setting 1 : zoomorph_balance;  0 = All twists, 1000=all Zoomorphs.
        self.setting = Setting(0, 1.00, DummyRng())  # All zoomorphs - chosen for the asymmetry.
        # self.axes = (axis.EW, axis.NS)
        self.workers = ((self.paper.master, 0), (self.paper.sunset, 1),
                        (self.paper.vanity, 1), (self.paper.mirror, 1),
                        (self.paper.rotate, 0), (self.paper.rotate, 1),
                        (self.paper.rotate, 3), (self.paper.rotate, 2))

    def test_make(self):
        sp = self.paper
        axis = self.shape.axis()
        com = self.shape.com()
        answers = {
            None: {
                axis.EW: {
                    (sp.master, 0): {com.E: Cut.H, com.W: Cut.B},
                    (sp.sunset, 1): {com.E: Cut.B, com.W: Cut.H},
                    (sp.vanity, 1): {com.E: Cut.H, com.W: Cut.B},
                    (sp.mirror, 1): {com.E: Cut.B, com.W: Cut.H},
                    (sp.rotate, 0): {com.E: Cut.H, com.W: Cut.B},
                    (sp.rotate, 1): {com.E: Cut.B, com.W: Cut.H},
                    (sp.rotate, 3): {com.E: Cut.H, com.W: Cut.B},
                    (sp.rotate, 2): {com.E: Cut.B, com.W: Cut.H}
                },
                axis.NS: {
                    (sp.master, 0): {com.N: Cut.H, com.S: Cut.B},
                    (sp.sunset, 1): {com.N: Cut.B, com.S: Cut.H},
                    (sp.vanity, 1): {com.N: Cut.H, com.S: Cut.B},
                    (sp.mirror, 1): {com.N: Cut.B, com.S: Cut.H},
                    (sp.rotate, 0): {com.N: Cut.H, com.S: Cut.B},
                    (sp.rotate, 1): {com.N: Cut.B, com.S: Cut.H},
                    (sp.rotate, 3): {com.N: Cut.H, com.S: Cut.B},
                    (sp.rotate, 2): {com.N: Cut.B, com.S: Cut.H}
                }
            },
            Cut.H: {
                axis.EW: {
                    (sp.master, 0): {com.E: Cut.B, com.W: Cut.H},
                    (sp.sunset, 1): {com.E: Cut.H, com.W: Cut.B},
                    (sp.vanity, 1): {com.E: Cut.B, com.W: Cut.H},
                    (sp.mirror, 1): {com.E: Cut.B, com.W: Cut.H},
                    (sp.rotate, 0): {com.E: Cut.B, com.W: Cut.H},
                    (sp.rotate, 1): {com.E: Cut.B, com.W: Cut.H},
                    (sp.rotate, 3): {com.E: Cut.B, com.W: Cut.H},
                    (sp.rotate, 2): {com.E: Cut.B, com.W: Cut.H}
                },
                axis.NS: {
                    (sp.master, 0): {com.N: Cut.B, com.S: Cut.H},
                    (sp.sunset, 1): {com.N: Cut.B, com.S: Cut.H},
                    (sp.vanity, 1): {com.N: Cut.H, com.S: Cut.B},
                    (sp.mirror, 1): {com.N: Cut.B, com.S: Cut.H},
                    (sp.rotate, 0): {com.N: Cut.B, com.S: Cut.H},
                    (sp.rotate, 1): {com.N: Cut.B, com.S: Cut.H},
                    (sp.rotate, 3): {com.N: Cut.B, com.S: Cut.H},
                    (sp.rotate, 2): {com.N: Cut.B, com.S: Cut.H}
                }
            }
        }
        for cut in answers:
            axis_answers = answers[cut]
            for axis in self.axes:
                tweak_answers = axis_answers[axis]
                for worker in self.workers:
                    answer = tweak_answers[worker]
                    cutter = Cutter(worker[0], self.setting, worker[1])
                    value = cutter.make(axis.a, cut)
                    worker_str = str(worker[0]) + '_' + str(worker[1])
                    answer_str = str(answer)
                    self.assertEqual(answer, value, str(cut) + ":" + str(axis) + ":" + worker_str + " Wall should have been " + answer_str)


if __name__ == '__main__':
    unittest.main()

