from Bod.mover import Mover
from Maze.util import Com


class Spiral(Mover):

    def __init__(self, maze, tweak):
        super().__init__(maze, tweak)
        self.is_miner = True
        self.face = None
        self.com = Com.N

    def _run(self):
        self.face = None
        if self.track:
            this_cell = self.track[-1]
            walls_to_dig = this_cell.walls_that_can_be_dug()
            if walls_to_dig:
                self.com = self.com.ccw
                if self.com not in walls_to_dig:
                    self.com = self.com.cw
                if self.com not in walls_to_dig:
                    self.com = self.com.cw
                if self.com in walls_to_dig:
                    self.face = self.com
                    next_cell = this_cell.make_door_in(self.face)
                    self.dig(next_cell)
                else:
                    self.track.pop()
            else:
                self.track.pop()
