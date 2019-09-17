from abc import ABCMeta, abstractmethod
from ..space import Lattice
from ..tool import Setting, Cutter


class Mover(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def _run(self):
        pass

    def __init__(self, lattice: Lattice, other=None):
        self.other = other
        self.track = []
        self.levels = 1
        self.is_miner = False
        self.finished = False
        self.tool = None
        self.face = None  # This is the com from where I came.
        self.lattice = lattice
        if other is None:
            paper = lattice.crs.paper()
            self.tweak = lattice.crs.tweak(paper.identity(), lattice.size, 0)
            self.entrance = lattice.cell(self.tweak.entry(lattice.border))

    def select_tool(self, setting: Setting):
        self.is_miner = True
        self.face = None
        self.tool = Cutter(self.tweak.paper, setting, self.tweak.worker_no)

    def run(self):
        if self.is_miner and not self.track:
            self.finished = True
        else:
            self._run()

    def dig(self, cell, com=None):
        cell.open(self.tool, com)
        self.go(cell)

    def go(self, cell):
        self.track.append(cell)

    def cell(self):
        if not self.track:
            return None
        return self.track[-1]
