import typing
from enum import Enum
from ..crs import CRS, Coords, Wallpaper
from .axes import Axis, Com, Paper
from .tweak import Tweak
from .dim import Dim


class Rectangle(CRS):

    def tweak(self) -> typing.Type[Tweak]:
        return Tweak

    def dim(self) -> typing.Type[Coords]:
        return Dim

    def paper(self) -> typing.Type[Wallpaper]:
        return Paper

    def axis(self) -> typing.Type[Enum]:
        return Axis

    def com(self) -> typing.Type[Enum]:
        return Com

