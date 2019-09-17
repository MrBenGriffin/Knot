from typing import Type
from enum import Enum
from ..crs import CRS, Coords, Wallpaper, WallpaperDecorator, Symmetry, Lattice as CRSLattice
from .lattice import Lattice
from .tweak import Tweak as RTweak
from .dim import Axis, Com, Dim


@WallpaperDecorator(
    {'master': 1, 'sunset': 2, 'vanity': 2, 'mirror': 2, 'rotate': 4},
    {'master': None, 'sunset': Symmetry.H, 'vanity': Symmetry.V, 'mirror': None, 'rotate': None},
)
class Paper(Wallpaper):
    master = 1
    sunset = 2
    vanity = 3
    mirror = 4
    rotate = 5

    @staticmethod
    def select(val: str):
        sel = {'N': Paper.master, 'H': Paper.sunset, 'V': Paper.vanity, 'F': Paper.mirror, 'R': Paper.rotate}
        return sel[val]

    @classmethod
    def identity(cls):
        return Paper.master

    def __str__(self):
        text = {Paper.master: "Master", Paper.sunset: "Sunset",
                Paper.vanity: "Vanity", Paper.mirror: "Mirror", Paper.rotate: "Rotate"}
        return text[self]

    def __repr__(self):
        return self.__str__()


class Tweak(RTweak):

    def face(self, com: Com) -> [Com, None]:
        if com is None:
            return None
        if self.worker_no == 0:
            return com
        if self.paper == self.paper.rotate:
            wx = {
                1: com.cw,
                2: com.opposite,
                3: com.ccw
            }
            return wx[self.worker_no]
        if self.paper == self.paper.mirror or self.paper.symmetry == com.axis.perp:
            return com.opposite
        return com

    def dim(self, index: tuple) -> Dim:
        basis = Dim.adopt(index)
        if self.worker_no == 0:
            return basis
        if self.paper == self.paper.rotate:
            wx = {
                1: Dim(basis.y, self.coords.x - basis.x),
                2: Dim(self.coords.x - basis.x, self.coords.y - basis.y),
                3: Dim(self.coords.y - basis.y, basis.x)
            }
            return wx[self.worker_no]
        w1 = {
            self.paper.sunset: Dim(basis.x, self.coords.y - basis.y),
            self.paper.vanity: Dim(self.coords.x - basis.x, basis.y),
            self.paper.mirror: Dim(self.coords.x - basis.x, self.coords.y - basis.y),
         }
        return w1[self.paper]


class Square(CRS):

    def tweak(self, paper: Wallpaper, index: tuple, worker_no: int = 0) -> Tweak:
        return Tweak(paper, index, worker_no)

    def paper(self) -> Type[Wallpaper]:
        return Paper

    def lattice(self, size: tuple, wrap: tuple) -> CRSLattice:
        return Lattice(self, size, wrap)

    def dim(self) -> Type[Coords]:
        return Dim

    def axis(self) -> Type[Enum]:
        return Axis

    def com(self) -> Type[Enum]:
        return Com

