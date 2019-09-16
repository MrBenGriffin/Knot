from knot.space import Lattice
from .mover import Mover
from knot.tool import Setting


class Holer(Mover):
    balance = 0.0

    def __init__(self, lattice: Lattice, setting: Setting):
        super().__init__(lattice)
        self.select_tool(setting)
        self.dig(self.entrance, None)

    def _run(self):
        self.face = None
        if self.track:
            cell = self.cell()
            walls = cell.walls
            for com in walls:
                wall = walls[com]
                if wall.can_be_door(com):
                    self.go(wall.cell(com))
                    self.face = com.opposite
                    wall.make_door(com, self.tool)
                    return
            self.track.pop()
