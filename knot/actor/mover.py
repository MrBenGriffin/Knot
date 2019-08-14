from abc import ABCMeta, abstractmethod
from knot.works import Structure
from knot.space import Tweak, Tw


class Mover(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def _run(self):
        pass

    # def face(self, com: Com) -> Com:

    def __init__(self, structure: Structure, tweak: Tw = None, other=None):
        self.other = other
        if tweak is None or other is None:
            self.tweak = Tweak(Tw.master, structure.cells_across, structure.cells_up)
        else:
            self.tweak = Tweak(tweak, structure.cells_across, structure.cells_up)
        self.track = []
        self.levels = 1
        self.is_miner = False
        self.structure = structure
        self.entrance = structure.at(self.tweak.entry(structure.border))
        self.dig(self.entrance)

    def run(self):
        if self.is_miner and not self.track and not self.structure.mined:
            self.structure.mined = True
        else:
            self._run()

    def dig(self, cell):
        if not cell.mined:
            cell.miner = self
            cell.mined = True
        self.go(cell)

    def go(self, cell):
        self.track.append(cell)

    def finished(self):
        return not self.track

    def cell(self):
        if not self.track:
            return None
        return self.track[-1]
