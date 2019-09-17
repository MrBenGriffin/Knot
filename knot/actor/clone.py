from knot.space import Lattice, Wallpaper
from .mover import Mover


class Clone(Mover):
    def __init__(self, lattice: Lattice, other: Mover, paper: Wallpaper, number):
        super().__init__(lattice, other)
        self.clone_doors = True
        self.lattice = lattice
        self.tweak = lattice.crs.tweak(paper, lattice.size, number)
        if other.tool:
            self.select_tool(other.tool.setting)
        self.entrance = lattice.cell(self.tweak.entry(lattice.border))
        self.dig(self.entrance, None)

    def _run(self):
        if self.other.track:
            # Master has already moved to a cell dug the wall.
            # Master only sets a face if it dug.
            if self.other.face:
                # Clone will need to find the correct tweaked cell that master is in first.
                # base.opened_from should also be the same as other.face
                base = self.other.cell()
                base_dir = self.other.face
                cut = base.walls[base_dir].door(base_dir.opposite)
                # Now Get the tweaked coordinates
                work_dim = self.tweak.dim(base.dim)
                # Now get the cell.
                cell = self.lattice.cell(work_dim)
                if cell:
                    self.track.clear()
                    self.go(cell)
                    # Face is tricky, because it is looking backward (where I came FROM).
                    # So the master WENT in the opposite direction (other.face.opposite)
                    # We tweak THAT to work out which way we should go.
                    # And then make the hole behind us. (in the opposite).
                    # The two opposites DO NOT cancel each other out!
                    self.face = self.tweak.face(base_dir.opposite).opposite
                    cell.walls[self.face].make_door(self.face, self.tool, cut)
                self.finished = self.other.finished
        else:
            if not self.other.track:
                self.track.clear()

    def set_other(self, other):
        self.other = other
        self.finished = False
        self.track = []

