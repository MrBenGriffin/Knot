from .mover import Mover
from knot.space import Lattice


class Joiner(Mover):
    def __init__(self, lattice: Lattice, other: Mover):
        super().__init__(lattice)
        self.dead_ends = []
        self.collection = []
        self.tool = other.tool
        self.collection.append(self.tool)
        self.entrance = other.entrance
        self.dig(self.entrance, None)

    def _run(self):
        if not self.finished and self.track:
            self.face = None
            cell = None
            this_cell = self.cell()
            if this_cell.tool not in self.collection:
                self.collection.append(this_cell.tool)
            walls = this_cell.walls
            for com in walls:
                neighbour = walls[com].cell(com)
                if neighbour and neighbour.tool not in self.collection:
                    self.go(neighbour)
                    cell = walls[com].make_door(com, self.tool)
                    self.face = com.opposite
                    self.finished = True
                    break  # because we can only have one face for clones.
            if not cell:
                exits = this_cell.exits()
                while exits and not cell:
                    cell = this_cell.move(exits.pop())
                    if cell in self.track or cell in self.dead_ends:
                        cell = None
                if cell:
                    self.track.append(cell)
                else:
                    self.dead_ends.append(self.track.pop())
        else:
            self.finished = True
