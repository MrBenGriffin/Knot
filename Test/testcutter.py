import unittest
from knot.space import Com, Tw, Axis
from knot.tool import Setting, Cut, Cutter, DummyRng


class TestCutter(unittest.TestCase):

    def setUp(self):
        # Setting 0 : straights_balance; 0 = All twists, 1000=all Straights
        # Setting 1 : zoomorph_balance;  0 = All twists, 1000=all Zoomorphs.
        self.setting = Setting(0, 1.00, DummyRng())  # All zoomorphs - chosen for the asymmetry.
        self.axes = (Axis.EW, Axis.NS)
        self.tweaks = (Tw.master, Tw.sunset, Tw.vanity, Tw.mirror, Tw.rot000, Tw.rot090, Tw.rot270, Tw.rot180)

    def test_make(self):
        answers = {
            None: {
                Axis.EW: {
                    Tw.master: {Com.E: Cut.H, Com.W: Cut.B},
                    Tw.sunset: {Com.E: Cut.B, Com.W: Cut.H},
                    Tw.vanity: {Com.E: Cut.H, Com.W: Cut.B},
                    Tw.mirror: {Com.E: Cut.B, Com.W: Cut.H},
                    Tw.rot000: {Com.E: Cut.H, Com.W: Cut.B},
                    Tw.rot090: {Com.E: Cut.B, Com.W: Cut.H},
                    Tw.rot270: {Com.E: Cut.H, Com.W: Cut.B},
                    Tw.rot180: {Com.E: Cut.B, Com.W: Cut.H}
                },
                Axis.NS: {
                    Tw.master: {Com.N: Cut.H, Com.S: Cut.B},
                    Tw.sunset: {Com.N: Cut.B, Com.S: Cut.H},
                    Tw.vanity: {Com.N: Cut.H, Com.S: Cut.B},
                    Tw.mirror: {Com.N: Cut.B, Com.S: Cut.H},
                    Tw.rot000: {Com.N: Cut.H, Com.S: Cut.B},
                    Tw.rot090: {Com.N: Cut.B, Com.S: Cut.H},
                    Tw.rot270: {Com.N: Cut.H, Com.S: Cut.B},
                    Tw.rot180: {Com.N: Cut.B, Com.S: Cut.H}
                }
            },
            Cut.H: {
                Axis.EW: {
                    Tw.master: {Com.E: Cut.H, Com.W: Cut.B},
                    Tw.sunset: {Com.E: Cut.B, Com.W: Cut.H},
                    Tw.vanity: {Com.E: Cut.H, Com.W: Cut.B},
                    Tw.mirror: {Com.E: Cut.H, Com.W: Cut.B},
                    Tw.rot000: {Com.E: Cut.H, Com.W: Cut.B},
                    Tw.rot090: {Com.E: Cut.H, Com.W: Cut.B},
                    Tw.rot270: {Com.E: Cut.H, Com.W: Cut.B},
                    Tw.rot180: {Com.E: Cut.H, Com.W: Cut.B}
                },
                Axis.NS: {
                    Tw.master: {Com.N: Cut.H, Com.S: Cut.B},
                    Tw.sunset: {Com.N: Cut.H, Com.S: Cut.B},
                    Tw.vanity: {Com.N: Cut.B, Com.S: Cut.H},
                    Tw.mirror: {Com.N: Cut.H, Com.S: Cut.B},
                    Tw.rot000: {Com.N: Cut.H, Com.S: Cut.B},
                    Tw.rot090: {Com.N: Cut.H, Com.S: Cut.B},
                    Tw.rot270: {Com.N: Cut.H, Com.S: Cut.B},
                    Tw.rot180: {Com.N: Cut.H, Com.S: Cut.B}
                }
            }
        }
        for cut in answers:
            axis_answers = answers[cut]
            for axis in self.axes:
                tweak_answers = axis_answers[axis]
                for tweak in self.tweaks:
                    answer = tweak_answers[tweak]
                    cutter = Cutter(self.setting, tweak)
                    value = cutter.make(axis.a, cut)
                    self.assertEqual(answer, value, str(cut) + ":" + str(axis) + ":" + str(tweak) + " Wall should have been " + str(answer))


if __name__ == '__main__':
    unittest.main()

