# encoding: utf-8
from knot.space import Com, Orientation, Tw
from .setting import Setting
from .cut import Cut


class Cutter:

    def __init__(self, setting: Setting = Setting, tweak: Tw = Tw.master):
        self.setting = setting
        self.tweak = tweak

    def make(self, orient: Orientation, cell_dir: Com, cut: Cut = None) -> dict:
        result = {}
        if cut is None:
            cut = self.setting.choose()
            result[cell_dir] = cut
            result[cell_dir.opposite] = cut.opposite
        else:
            # This seems backward, but it's not.  The cell is already digging the opposite wall,
            # and so doesn't need to worry about that part.  But the EW will look odd if unaffected by the mirror.
            # It's still not a true mirror image, as types are always CCW oriented.
            if (self.tweak is Tw.horizon and orient is Orientation.EW) or \
                    (self.tweak is Tw.vanity and orient is Orientation.NS):
                result[cell_dir.opposite] = cut
                result[cell_dir] = cut.opposite
            else:
                result[cell_dir] = cut
                result[cell_dir.opposite] = cut.opposite
        return result
