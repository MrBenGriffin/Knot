import typing
from ..crs import Wallpaper, WallpaperDecorator, Symmetry
from .rectilinear import Rectilinear
from .tweak import Tweak


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


class Rectangle(Rectilinear):

    def paper(self) -> typing.Type[Wallpaper]:
        return Paper

    def tweak(self) -> typing.Type[Tweak]:
        return Tweak

