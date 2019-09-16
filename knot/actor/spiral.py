from .mover import Mover
from knot.space import Lattice
from knot.tool import Setting


class Spiral(Mover):

    def __init__(self, lattice: Lattice, setting: Setting):
        super().__init__(lattice)
        com = lattice.crs.com()
        self.com = com.S
        self.select_tool(setting)
        self.dig(self.entrance, None)

    def _run(self):
        self.face = None
        if self.track:
            cell = self.cell()
            walls = cell.walls_that_can_be_dug()
            if walls:
                self.com = self.com.ccw
                if self.com not in walls:
                    self.com = self.com.cw
                if self.com not in walls:
                    self.com = self.com.cw
                if self.com in walls:
                    self.face = self.com.opposite
                    wall = cell.walls[self.com]
                    neighbour = wall.make_door(self.com, self.tool)
                    self.go(neighbour)
                else:
                    self.track.pop()
            else:
                self.track.pop()
