import unittest
from knot.space import Com, Wallpaper, Axis
from knot.tool import Setting, Cut, Cutter, DummyRng


class TestCutter(unittest.TestCase):

    def setUp(self):
        # Setting 0 : straights_balance; 0 = All twists, 1000=all Straights
        # Setting 1 : zoomorph_balance;  0 = All twists, 1000=all Zoomorphs.
        self.setting = Setting(0, 1.00, DummyRng())  # All zoomorphs - chosen for the asymmetry.
        self.axes = (Axis.EW, Axis.NS)
        self.tweaks = (Wallpaper.master, Wallpaper.sunset, Wallpaper.vanity, Wallpaper.mirror, Wallpaper.rot000, Wallpaper.rot090, Wallpaper.rot270, Wallpaper.rot180)

    def test_make(self):
        answers = {
            None: {
                Axis.EW: {
                    Wallpaper.master: {Com.E: Cut.H, Com.W: Cut.B},
                    Wallpaper.sunset: {Com.E: Cut.B, Com.W: Cut.H},
                    Wallpaper.vanity: {Com.E: Cut.H, Com.W: Cut.B},
                    Wallpaper.mirror: {Com.E: Cut.B, Com.W: Cut.H},
                    Wallpaper.rot000: {Com.E: Cut.H, Com.W: Cut.B},
                    Wallpaper.rot090: {Com.E: Cut.B, Com.W: Cut.H},
                    Wallpaper.rot270: {Com.E: Cut.H, Com.W: Cut.B},
                    Wallpaper.rot180: {Com.E: Cut.B, Com.W: Cut.H}
                },
                Axis.NS: {
                    Wallpaper.master: {Com.N: Cut.H, Com.S: Cut.B},
                    Wallpaper.sunset: {Com.N: Cut.B, Com.S: Cut.H},
                    Wallpaper.vanity: {Com.N: Cut.H, Com.S: Cut.B},
                    Wallpaper.mirror: {Com.N: Cut.B, Com.S: Cut.H},
                    Wallpaper.rot000: {Com.N: Cut.H, Com.S: Cut.B},
                    Wallpaper.rot090: {Com.N: Cut.B, Com.S: Cut.H},
                    Wallpaper.rot270: {Com.N: Cut.H, Com.S: Cut.B},
                    Wallpaper.rot180: {Com.N: Cut.B, Com.S: Cut.H}
                }
            },
            Cut.H: {
                Axis.EW: {
                    Wallpaper.master: {Com.E: Cut.H, Com.W: Cut.B},
                    Wallpaper.sunset: {Com.E: Cut.B, Com.W: Cut.H},
                    Wallpaper.vanity: {Com.E: Cut.H, Com.W: Cut.B},
                    Wallpaper.mirror: {Com.E: Cut.H, Com.W: Cut.B},
                    Wallpaper.rot000: {Com.E: Cut.H, Com.W: Cut.B},
                    Wallpaper.rot090: {Com.E: Cut.H, Com.W: Cut.B},
                    Wallpaper.rot270: {Com.E: Cut.H, Com.W: Cut.B},
                    Wallpaper.rot180: {Com.E: Cut.H, Com.W: Cut.B}
                },
                Axis.NS: {
                    Wallpaper.master: {Com.N: Cut.H, Com.S: Cut.B},
                    Wallpaper.sunset: {Com.N: Cut.H, Com.S: Cut.B},
                    Wallpaper.vanity: {Com.N: Cut.B, Com.S: Cut.H},
                    Wallpaper.mirror: {Com.N: Cut.H, Com.S: Cut.B},
                    Wallpaper.rot000: {Com.N: Cut.H, Com.S: Cut.B},
                    Wallpaper.rot090: {Com.N: Cut.H, Com.S: Cut.B},
                    Wallpaper.rot270: {Com.N: Cut.H, Com.S: Cut.B},
                    Wallpaper.rot180: {Com.N: Cut.H, Com.S: Cut.B}
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

