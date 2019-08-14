from .mover import Mover


class Clone(Mover):
    def __init__(self, structure, tweak, other):
        super().__init__(structure, tweak, other)
        self.clone_doors = True
        if other.is_miner:
            self.select_tool(other.tool.setting)

    def _run(self):
        if len(self.other.track) > 1:
            master_cell = self.other.track[-2]
            this_cell = self.structure.at(self.tweak.dim(master_cell.dim))
            if this_cell:
                if not this_cell.mined:
                    self.dig(this_cell)
                else:
                    self.go(this_cell)
                self.track.pop(0)
                if self.other.face is not None:
                    door = master_cell.walls[self.other.face].doors[self.other.face]
                    self.face = self.tweak.face(self.other.face)
                    next_cell = this_cell.make_door_in(self.face, self, door)
                    self.dig(next_cell)
        else:
            if not self.other.track:
                self.track.clear()

    def set_other(self, other):
        self.other = other
        self.track = []

