import typing
from abc import ABC
from enum import Enum
from ..crs import CRS, Coords
from .axes import Axis, Com
from .dim import Dim


class Rectilinear(CRS, ABC):

    def dim(self) -> typing.Type[Coords]:
        return Dim

    def axis(self) -> typing.Type[Enum]:
        return Axis

    def com(self) -> typing.Type[Enum]:
        return Com

