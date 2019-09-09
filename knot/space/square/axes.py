# encoding: utf-8
from enum import Enum
from ..crs import Wallpaper, AxesDecorator, ComDecorator, WallpaperDecorator


@AxesDecorator({'NS': [], 'EW': []})
class Axis(Enum):
    NS = 0x0100
    EW = 0x0200


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
        return text[self._value_]


@WallpaperDecorator({'master': 1, 'sunset': 2, 'vanity': 2, 'mirror': 2, 'rotate': 4})
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

