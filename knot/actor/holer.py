from .mover import Mover
from knot.works import Structure
from knot.tool import Setting
import random


class Holer(Mover):
    balance = 0.0

    def __init__(self, structure: Structure, setting: Setting):
        super().__init__(structure)
        self.select_tool(setting)

    def _run(self):
        self.face = None
        if self.track:
            cell = self.cell()
            walls = cell.walls
            for com in walls:
                wall = walls[com]
                if wall.can_be_door(com):
                    self.face = com
                    neighbour = wall.neighbour(com)
                    if not neighbour.mined():
                        self.go(neighbour)
                        self.face = com.opposite
                    wall.make_door(com, self.tool)
                    return
                if self.balance < random.random():
                    return
            self.track.pop()
