from typing import Type
from enum import Enum
from ..crs import CRS, Coords, Wallpaper, WallpaperDecorator, Symmetry, Lattice as CRSLattice
from .lattice import Lattice
from .tweak import Tweak as RTweak
from .dim import Axis, Com, Dim


class Tweak(RTweak):

    def face(self, com: Com) -> [Com, None]:
        if com is None:
            return None
        if self.worker_no != 0 and self.paper == self.paper.mirror or self.paper.symmetry == com.axis.perp:
            return com.opposite
        return com

    def dim(self, index: tuple) -> Dim:
        basis = Dim.adopt(index)
        if self.worker_no == 0:
            return basis
        w1 = {
            self.paper.sunset: Dim(basis.x, self.coords.y - basis.y),
            self.paper.vanity: Dim(self.coords.x - basis.x, basis.y),
            self.paper.mirror: Dim(self.coords.x - basis.x, self.coords.y - basis.y)
        }
        return w1[self.paper]


@WallpaperDecorator(
    {'master': 1, 'sunset': 2, 'vanity': 2, 'mirror': 2},
    {'master': None, 'sunset': Symmetry.H, 'vanity': Symmetry.V, 'mirror': None},
)
class Paper(Wallpaper):
    master = 1
    sunset = 2
    vanity = 3
    mirror = 4

    @staticmethod
    def select(val: str):
        sel = {'N': Paper.master, 'H': Paper.sunset, 'V': Paper.vanity, 'F': Paper.mirror, 'R': Paper.mirror}
        return sel[val]

    @classmethod
    def identity(cls):
        return Paper.master

    def __str__(self):
        text = {Paper.master: "Master", Paper.sunset: "Sunset",
                Paper.vanity: "Vanity", Paper.mirror: "Mirror"}
        return text[self]

    def __repr__(self):
        return self.__str__()


class Rectangle(CRS):

    def paper(self) -> Type[Wallpaper]:
        return Paper

    def tweak(self, paper: Wallpaper, index: tuple, worker_no: int = 0) -> Tweak:
        return Tweak(paper, index, worker_no)

    def lattice(self, size: tuple, wrap: tuple) -> CRSLattice:
        return Lattice(self, size, wrap)

    def dim(self) -> Type[Coords]:
        return Dim

    def axis(self) -> Type[Enum]:
        return Axis

    def com(self) -> Type[Enum]:
        return Com

