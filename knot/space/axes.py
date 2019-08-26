# encoding: utf-8
from enum import IntFlag
from collections import namedtuple

Dim = namedtuple('Dim', 'x y')


class AxesDecorator:
    point_map = {}

    def __init__(self, point_map):
        AxesDecorator.point_map = point_map

    def __call__(self, enum):
        for axis, idx in AxesDecorator.point_map.items():
            enum[axis].a = None
            enum[axis].b = None
        return enum


@AxesDecorator({'NS': [], 'EW': []})
class Axis(IntFlag):
    NS = 0x0100
    EW = 0x0200


# Com Decorator class.
class ComDecorator:
    def __init__(self, reverse_map, rotate_map, axis_map):
        self.reverse_map = reverse_map
        self.rotate_map = rotate_map
        self.axis_map = axis_map

    def __call__(self, enum):
        for fwd, rev in self.reverse_map.items():
            enum[fwd].opposite = enum[rev]
            enum[rev].opposite = enum[fwd]
        for fwd, rot in self.rotate_map.items():
            enum[fwd].cw = enum[rot]
            enum[rot].ccw = enum[fwd]
        for com, axis in self.axis_map.items():
            if axis:
                enum[com].axis = Axis[axis[0]]
                if axis[1] is 0:
                    Axis[axis[0]].a = enum[com]
                else:
                    Axis[axis[0]].b = enum[com]
        return enum


@ComDecorator(
    {'N': 'S', 'E': 'W'},
    {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'},
    {'N': ['NS', 0], 'E': ['EW', 0], 'S': ['NS', 1], 'W': ['EW', 1]}
)
class Com(IntFlag):
    N = 0x0001
    E = 0x0002
    S = 0x0004
    W = 0x0008

    def __str__(self):
        text = {Com.N: "North", Com.E: "East", Com.S: "South", Com.W: "West"}
        return text[self._value_]
