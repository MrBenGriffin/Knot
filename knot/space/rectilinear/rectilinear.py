import typing
from abc import ABC
from enum import Enum
from ..crs import CRS, Coords, Lattice as CRSLattice
from .axes import Axis, Com
from .dim import Dim
from .lattice import Lattice


class Rectilinear(CRS, ABC):

    def dim(self) -> typing.Type[Coords]:
        return Dim

    def axis(self) -> typing.Type[Enum]:
        return Axis

    def com(self) -> typing.Type[Enum]:
        return Com

    def lattice(self, size: tuple, wrap: tuple) -> CRSLattice:
        return Lattice(Dim, size, wrap)

