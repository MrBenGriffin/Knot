from itertools import product
from abc import ABC, abstractmethod
from .cell import Cell
from .wall import Wall


# https://en.wikipedia.org/wiki/Wallpaper_group#The_seventeen_groups
class Lattice(ABC):

    def __init__(self, dim, size: tuple, wrap: tuple):
        self.size = dim.adjust(size)
        a_wrap = dim.adjust(wrap)
        a_range = tuple(val if wrap[idx] else val + 1 for idx, val in enumerate(self.size))
        wall_dims = tuple(self.size[:i] + (adj,) + self.size[i + 1:] for i, adj in enumerate(a_range))
        wall_coords = tuple(product(*(range(0, i) for i in wall_dim)) for wall_dim in wall_dims)
        cell_coords = product(*(range(0, i) for i in self.size))
        walls = {dim.axis(i): {j: Wall() for j in l} for i, l in enumerate(wall_coords)}
        self.cells = {i: Cell(i, {c: (walls[c.axis][dim.adopt(i).edge(c, wall_dims, a_wrap).tuple()]) for c in dim.com()}) for i in cell_coords}

    def cell(self, index) -> [None, Cell]:
        return None if index.tuple() not in self.cells else self.cells[index.tuple()]

    @abstractmethod
    def code(self) -> str:
        pass

    @abstractmethod
    def unicode(self) -> str:
        pass
