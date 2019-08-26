from .mover import Mover
from knot.space import Com
from knot.works import Structure
from knot.tool import Setting


class Spiral(Mover):

    def __init__(self, structure: Structure, setting: Setting):
        super().__init__(structure)
        self.com = Com.S
        self.select_tool(setting)

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
