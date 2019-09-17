from enum import Enum
from ..crs import Coords, AxesDecorator, ComDecorator, Symmetry


@AxesDecorator(
    {'NS': [], 'EW': []},
    {'NS': (Symmetry.V, Symmetry.H), 'EW': (Symmetry.H, Symmetry.V)})
class Axis(Enum):
    NS = 0x0100
    EW = 0x0200

    def __str__(self):
        text = {Axis.NS: "NS", Axis.EW: "EW"}
        return text[self]


@ComDecorator(
    Axis,
    {'N': 'S', 'E': 'W'},
    {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'},
    {'N': ['NS', 0], 'E': ['EW', 0], 'S': ['NS', 1], 'W': ['EW', 1]}
)
class Com(Enum):
    N = 0x0001
    E = 0x0002
    S = 0x0004
    W = 0x0008

    def __str__(self):
        text = {Com.N: "North", Com.E: "East", Com.S: "South", Com.W: "West"}
        return text[self]


class Dim(Coords):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.x = x
        self.y = y

    def edge(self, com: Com, limits, wraps) -> [None, Coords]:
        dx, dy = self.x, self.y
        if com.axis == Axis.EW:
            limit = limits[0]
            wrap = wraps[0]
            dx = dx if com == Com.W else dx + 1
        else:
            limit = limits[1]
            wrap = wraps[0]
            dy = dy if com == Com.S else dy + 1
        dx = dx % limit[0] if wrap else dx
        dy = dy % limit[1] if wrap else dy
        return Dim(dx, dy) if 0 <= dx < limit[0] and 0 <= dy < limit[1] else None

    def going(self, com: Com, limit, wraps) -> [None, Coords]:
        dx, dy = self.x, self.y
        if com.axis == Axis.EW:
            dx = dx - 1 if com == Com.W else dx + 1
            dx = dx % limit[0] if wraps[0] else dx
            dy = dy % limit[1] if wraps[0] else dy
        else:
            dx = dx - 1 if com == Com.S else dx + 1
            dx = dx % limit[0] if wraps[1] else dx
            dy = dy % limit[1] if wraps[1] else dy
        return Dim(dx, dy) if 0 <= dx < limit[0] and 0 <= dy < limit[1] else None

    def tuple(self) -> tuple:
        return self.x, self.y

    @classmethod
    def com(cls):
        return Com

    @classmethod
    def axis(cls, key: int):
        return Axis.EW if key == 0 else Axis.NS if key == 1 else None

    @classmethod
    def adjust(cls, a: tuple) -> tuple:
        return None if not a else (a[0], a[0]) if len(a) == 1 else (a[0], a[1])

    @classmethod
    def adopt(cls, a: tuple):
        return None if not a else Dim(a[0], a[0]) if len(a) == 1 else Dim(a[0], a[1])

    @classmethod
    def __len__(cls):
        return 2

    def __getitem__(self, key):
        return tuple([self.x, self.y]).__getitem__(key)

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    def __repr__(self):
        return "Dim(" + str(self.x) + "," + str(self.y) + ")"

    def __eq__(self, other):
        if isinstance(other, Dim):
            return self.x == other.x and self.y == other.y
        if isinstance(other, tuple):
            return self.x == other[0] and self.y == other[1]
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, Dim):
            return self.x != other.x or self.y != other.y
        if isinstance(other, tuple):
            return self.x != other[0] or self.y != other[1]
        return NotImplemented


