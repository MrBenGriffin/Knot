# encoding: utf-8
import typing
from ..space.crs import Wallpaper, Coords
from .setting import Setting
from .cut import Cut


class Cutter:

    def __init__(self, setting: Setting = Setting(), paper: Wallpaper = None, work_number: int = 0, com=None):
        self.work_number = work_number
        self.setting = setting
        self.paper = paper
        self.com = com

    def make(self, cell_dir, cut: Cut = None) -> dict:
        result = {}
        if cut is None:
            cut = self.setting.choose()
            result[cell_dir] = cut
            result[cell_dir.opposite] = cut.opposite
        else:
            # TODO:: I need to fix this
            # This seems backward, but it's not.  The cell is already digging the opposite wall,
            # and so doesn't need to worry about that part.  But the EW will look odd if unaffected by the mirror.
            # It's still not a true mirror image, as types are always CCW oriented.
            # if (self.paper is Wallpaper.sunset and cell_dir.axis is Axis.EW) or \
            #         (self.paper is Wallpaper.vanity and cell_dir.axis is Axis.NS):
            #     result[cell_dir.opposite] = cut
            #     result[cell_dir] = cut.opposite
            # else:
            result[cell_dir] = cut
            result[cell_dir.opposite] = cut.opposite
        return result
