from abc import ABCMeta, abstractmethod
from ..works import Structure
from ..tool import Setting, Cutter


class Mover(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def _run(self):
        pass

    def __init__(self, structure: Structure, other=None):
        self.work_number = 0
        self.other = other
        self.shape = structure.shape
        self.track = []
        self.levels = 1
        self.is_miner = False
        self.tool = None
        self.face = None
        self.structure = structure
        if other is None:
            self.tweak = self.shape.tweak(self.shape.wallpaper.identity(), structure.size())
            self.entrance = structure.at(self.tweak.entry(structure.border))
            self.dig(self.entrance, None)

    def select_tool(self, setting: Setting):
        self.is_miner = True
        self.face = None
        self.tool = Cutter(setting, self.shape.wallpaper, self.work_number, self.shape.com)

    def run(self):
        if self.is_miner and not self.track and not self.structure.mined:
            self.structure.mined = True
        else:
            self._run()

    def dig(self, cell, com=None):
        cell.open(self, com)
        self.go(cell)

    def go(self, cell):
        self.track.append(cell)

    def finished(self):
        return not self.track

    def cell(self):
        if not self.track:
            return None
        return self.track[-1]
