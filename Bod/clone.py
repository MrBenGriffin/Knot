from Bod.mover import Mover
# from Maze.util import Com

class Clone(Mover):
    def __init__(self, maze, tweak, other):
        super().__init__(maze)
        self.is_miner = True
        self.tweak = tweak
        self.other = other
        self.halo = "white"
        self.body = "gray"
        self.face = None
        self.clone_doors = True

    def _run(self):
        if len(self.other.track) > 1:
            master_cell = self.other.track[-2]
            this_cell = self.tweak.cell(self.maze, master_cell)
            if this_cell:
                # print(str(master_cell.dim)) + "; " + str(self.other.face) + this_cell.dim
                if not this_cell.mined:
                    self.dig(this_cell)
                else:
                    self.go(this_cell)
                self.track.pop(0)
                if self.other.face is not None:
                    door = master_cell.walls[self.other.face].doors[self.other.face]
                    self.face = self.tweak.choose(self.other.face)
                    next_cell = this_cell.make_door_in(self.face, door)
                    self.dig(next_cell)
        else:
            if not self.other.track:
                self.track.clear()