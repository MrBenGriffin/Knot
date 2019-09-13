import unittest
from knot.tool import Cutter, DummyRng
from knot.space import Shape
from knot.tool.setting import Setting
from knot.tool.cut import Cut


class TestCutter(unittest.TestCase):

    def setUp(self):
        self.shape = Shape.squared
        # enum[name].tweak = crs.tweak()
        # enum[name].dim = crs.dim()
        # enum[name].axis = crs.axis()
        # enum[name].com = crs.com()
        # enum[name].wallpaper = crs.paper()
        self.axes = self.shape.axis
        self.paper = self.shape.wallpaper
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
        axis = self.shape.axis
        sp = self.paper
        com = self.shape.com
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
                    (sp.master, 0): {com.E: Cut.H, com.W: Cut.B},
                    (sp.sunset, 1): {com.E: Cut.B, com.W: Cut.H},
                    (sp.vanity, 1): {com.E: Cut.H, com.W: Cut.B},
                    (sp.mirror, 1): {com.E: Cut.H, com.W: Cut.B},
                    (sp.rotate, 0): {com.E: Cut.H, com.W: Cut.B},
                    (sp.rotate, 1): {com.E: Cut.H, com.W: Cut.B},
                    (sp.rotate, 3): {com.E: Cut.H, com.W: Cut.B},
                    (sp.rotate, 2): {com.E: Cut.H, com.W: Cut.B}
                },
                axis.NS: {
                    (sp.master, 0): {com.N: Cut.H, com.S: Cut.B},
                    (sp.sunset, 1): {com.N: Cut.H, com.S: Cut.B},
                    (sp.vanity, 1): {com.N: Cut.B, com.S: Cut.H},
                    (sp.mirror, 1): {com.N: Cut.H, com.S: Cut.B},
                    (sp.rotate, 0): {com.N: Cut.H, com.S: Cut.B},
                    (sp.rotate, 1): {com.N: Cut.H, com.S: Cut.B},
                    (sp.rotate, 3): {com.N: Cut.H, com.S: Cut.B},
                    (sp.rotate, 2): {com.N: Cut.H, com.S: Cut.B}
                }
            }
        }
        for cut in answers:
            axis_answers = answers[cut]
            for axis in self.axes:
                tweak_answers = axis_answers[axis]
                for worker in self.workers:
                    answer = tweak_answers[worker]
                    cutter = Cutter(self.setting, worker[0], worker[1], self.shape.com)
                    value = cutter.make(axis.a, cut)
                    self.assertEqual(answer, value, str(cut) + ":" + str(axis) + ":" + str(worker) + " Wall should have been " + str(answer))


if __name__ == '__main__':
    unittest.main()

