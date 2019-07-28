from Bod.mover import Mover
from Maze.cell import Cell


class Joiner(Mover):
    def __init__(self, maze):
        super().__init__(maze)
        self.is_miner = True
        self.face = None
        self.dead_ends = []
        self.collection = []

    def _run(self):
        if self.track:
            self.face = None
            cell = None
            this_cell = self.track[-1]
            if this_cell.miner not in self.collection:
                self.collection.append(this_cell.miner)
            neighbours = this_cell.neighbours()
            for com in neighbours:
                neighbour = neighbours[com]
                if neighbour.miner and neighbour.miner not in self.collection:
                    self.face = com
                    cell = this_cell.make_door_in(self.face, self)
                    self.dig(cell)
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
            self.maze.joined = True
