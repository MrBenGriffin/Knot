# encoding: utf-8
# import typing
from ..space.crs import Wallpaper
from .setting import Setting
from .cut import Cut
from .tool import Tool


class Cutter(Tool):

    def __init__(self, paper: Wallpaper = None, setting: Setting = Setting(), work_number: int = 0):
        self.paper = paper
        self.work_number = work_number
        self.setting = setting

    def make(self, cell_dir, cut: Cut = None) -> dict:
        result = {}
        if cut is None:
            cut = self.setting.choose()
            result[cell_dir] = cut
            result[cell_dir.opposite] = cut.opposite
        else:
            # It's still not a true mirror image, as types are always CCW oriented.
            if self.paper.symmetry == cell_dir.axis.para:
                result[cell_dir] = cut
                result[cell_dir.opposite] = cut.opposite
            else:
                result[cell_dir] = cut.opposite
                result[cell_dir.opposite] = cut
        return result
