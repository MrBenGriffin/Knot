import typing
from abc import ABC, abstractmethod
from enum import Enum


class Symmetry(Enum):
    N = 1
    H = 2
    V = 3
    F = 4
    R = 5

    def __str__(self):
        text = {Symmetry.N: "normal", Symmetry.H: "horizontal semi-mirror",
                Symmetry.V: "vertical semi-mirror", Symmetry.F: "flipped symmetry", Symmetry.R: "rotated symmetry"}
        return text[self]

    @staticmethod
    def choices() -> tuple:
        return 'N', 'H', 'V', 'F', 'R'


class Wallpaper(Enum):
    """
    https://en.wikipedia.org/wiki/Wallpaper_group
    https://en.wikipedia.org/wiki/List_of_planar_symmetry_groups#Wallpaper_groups
    A wallpaper group (or plane symmetry group or plane crystallographic group)
    is a mathematical classification of a two-dimensional repetitive pattern,
    based on the symmetries in the pattern.
    Such patterns occur frequently in architecture and decorative art,
    especially in textiles and tiles as well as wallpaper.

    There are precisely seventeen groups
    p1  = 'master' (only translations; there are no rotations, reflections, or glide reflections) - oblique
    p2  = 'mirror'/'rot270' (four rotation centres of order two (180°), but no reflections or glide reflections) - oblique
    pm  = 'vanity/sunset' (no rotations but parallel reflection axes) -  rectangular
    pg  = (only glide reflections with parallel axes) - rectangular
    cm  = (symmetrically staggered rows) - rhombic
    pmm = (mirrored in both vertical and horizontal, not rotated!) - rectangular
    pmg = (mirrored and then glide reflected) - rectangular
    pgg = (reflections in two perpendicular directions, and a rotation of order two (180°) not centred on reflection axis) - rhombic
    cmm = (eg bricks in a wall 'running bond' - rhombic
    p4  = 'rot090' (The group p4 has two rotation centres of order four (90°), and one rotation centre of order two (180°) - square
    p4m = (p4 with an internal mirror)
    p4g = (p4 with a glide reflection)
    p3  = 3 different rotation centres of order three (120°), but no reflections or glide reflections - hexagonal
    p3m1 = (cf. wikipedia)- hexagonal
    p31m = (cf. wikipedia)- hexagonal
    p6   = (cf. wikipedia)- hexagonal
    p6m  = p6 with mirror - hexagonal
    """
    @staticmethod
    def select(val: Symmetry):
        pass

    @classmethod
    def identity(cls):
        return Wallpaper.select(Symmetry.N)

    @abstractmethod
    def __str__(self):
        pass


class Coords(ABC):
    @abstractmethod
    def __init__(self, *args):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __ne__(self, other):
        pass


class Tweak(ABC):
    @abstractmethod
    def __init__(self, paper: Enum, idx: Coords, worker_no: int = 0):
        pass

    @abstractmethod
    def face(self, com: Enum):
        pass

    @abstractmethod
    def dim(self, basis: typing.NamedTuple) -> typing.NamedTuple:
        pass

    @abstractmethod
    def entry(self, border: [int, None]):
        pass


class CRS(ABC):
    """
    Coordinate Reference System is an abstract base class.
    """

    @abstractmethod
    def tweak(self) -> typing.Type[Tweak]:
        pass

    @abstractmethod
    def dim(self) -> typing.Type[Coords]:
        pass

    @abstractmethod
    def axis(self) -> typing.Type[Enum]:
        pass

    @abstractmethod
    def com(self) -> typing.Type[Enum]:
        pass

    @abstractmethod
    def paper(self) -> typing.Type[Wallpaper]:
        pass


class WallpaperDecorator:
    def __init__(self, wp_map, sym_map):
        self.wp_map = wp_map
        self.sym_map = sym_map

    def __call__(self, enum):
        for thing, workers in self.wp_map.items():
            enum[thing].workers = workers
        for thing, symmetry in self.sym_map.items():
            enum[thing].symmetry = symmetry
        return enum


class AxesDecorator:
    point_map = {}

    def __init__(self, point_map, parallel_map):
        AxesDecorator.point_map = point_map
        self.parallel_map = parallel_map

    def __call__(self, enum):
        for axis, idx in AxesDecorator.point_map.items():
            enum[axis].a = None
            enum[axis].b = None
        for axis, symmetry in self.parallel_map.items():
            enum[axis].para = symmetry[0]
            enum[axis].perp = symmetry[1]
        return enum


class ComDecorator:
    def __init__(self, axis, reverse_map, rotate_map, axis_map):
        self.reverse_map = reverse_map
        self.rotate_map = rotate_map
        self.axis_map = axis_map
        self.axis = axis

    def __call__(self, enum):
        for fwd, rev in self.reverse_map.items():
            enum[fwd].opposite = enum[rev]
            enum[rev].opposite = enum[fwd]
        for fwd, rot in self.rotate_map.items():
            enum[fwd].cw = enum[rot]
            enum[rot].ccw = enum[fwd]
        for com, axis in self.axis_map.items():
            if axis:
                enum[com].axis = self.axis[axis[0]]
                if axis[1] is 0:
                    self.axis[axis[0]].a = enum[com]
                else:
                    self.axis[axis[0]].b = enum[com]
        return enum
