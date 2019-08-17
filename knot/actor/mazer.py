import random
from .mover import Mover
from knot.works import Structure
from knot.tool import Setting


class Mazer(Mover):
    """
    An alternative (hybrid) to the Miner/Lister.
    This is because lister gives lots of single-cell corridors * yuck *
        (1) Act like the Miner for 16 (or 32) turns.
        (2) Act like the Lister for 1 turn.
    """
    cutoff = 15

    def __init__(self, structure: Structure, setting: Setting):
        super().__init__(structure)
        self.sequence = 0
        self.cell_index = None
        self.faces = []
        self.select_tool(setting)

    def work(self, cell) -> bool:
        walls = cell.walls_that_can_be_dug()
        if walls:
            face = random.choice(walls)
            wall = cell.walls[face]
            next_cell = wall.make_door(face, self.tool)
            self.go(next_cell)
            self.face = face.opposite
            return True
        else:
            return False

    def _run(self):
        self.sequence += 1
        self.face = None
        if self.track:
            if self.sequence < Mazer.cutoff:
                cell = self.cell()
                if not self.work(cell):
                    self.track.pop()
            else:
                self.sequence = 0
                self.cell_index = random.randrange(len(self.track))
                cell = self.track[self.cell_index]
                if not self.work(cell):
                    del self.track[self.cell_index]

