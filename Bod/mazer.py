import random
from Bod.mover import Mover


class Mazer(Mover):
    """
    An alternative (hybrid) to the Miner/Lister.
    This is because lister gives lots of single-cell corridors * yuck *
        (1) Act like the Miner for 16 (or 32) turns.
        (2) Act like the Lister for 1 turn.
    """

    def __init__(self, maze):
        super().__init__(maze)
        self.is_miner = True
        # self.halo = "white"
        # self.body = "black"
        self.sequence = 0
        self.forward = 0
        self.cell_index = None
        self.face = None

    def _run(self):
        self.sequence += 1
        self.face = None
        if self.track:
            if self.sequence & 15 != 0:   # cheaper than % 16
                this_cell = self.track[-1]
                walls_to_dig = this_cell.walls_that_can_be_dug()
                if walls_to_dig:
                    self.face = random.choice(walls_to_dig)
                    next_cell = this_cell.make_door_in(self.face)
                    self.dig(next_cell)
                    self.forward += 1
                else:
                    self.forward = 0
                    self.track.pop()
            else:
                self.forward = 0
                self.cell_index = random.randrange(len(self.track))
                this_cell = self.track[self.cell_index]
                walls_to_dig = this_cell.walls_that_can_be_dug()
                del self.track[self.cell_index]
                if walls_to_dig:
                    self.track.append(this_cell)
                    self.face = random.choice(walls_to_dig)
                    next_cell = this_cell.make_door_in(self.face)
                    self.dig(next_cell)
                    self.forward += 1
