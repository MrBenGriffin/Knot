from .mover import Mover


class Clone(Mover):
    def __init__(self, structure, tweak, other):
        super().__init__(structure, tweak, other)
        self.clone_doors = True
        if other.is_miner:
            self.select_tool(other.tool.setting)

    def _run(self):
        if self.other.track:
            base = self.other.cell()
            face = self.other.face
            cell = self.structure.at(self.tweak.dim(base.dim))
            if cell:
                cell.open(self.tool, self.tweak.face(base.opened_from))
                if face is not None:
                    door = base.walls[face].door(face)
                    self.face = self.tweak.face(face)
                    next_cell = cell.walls[self.face].make_door(self.face, self.tool, door)
                    # next_cell = cell.make_door_in(self.face, self.tool, door)
                    self.go(next_cell)
        else:
            if not self.other.track:
                self.track.clear()

    def set_other(self, other):
        self.other = other
        self.track = []

