from .mover import Mover
from knot.space import Com
from knot.works import Structure
from knot.tool import Setting


class Spiral(Mover):

    def __init__(self, structure: Structure, setting: Setting):
        super().__init__(structure)
        self.com = Com.N
        self.select_tool(setting)

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
                    next_cell = this_cell.make_door_in(self.face, self)
                    self.dig(next_cell)
                else:
                    self.track.pop()
            else:
                self.track.pop()
