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


@AxesDecorator({'NS': [], 'EW': [], 'CF': []})
class Axis(IntFlag):
    NS = 0x0100
    EW = 0x0200
    CF = 0x0400


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
            enum[com].axis = Axis[axis[0]]
            if axis[1] is 0:
                Axis[axis[0]].a = enum[com]
            else:
                Axis[axis[0]].b = enum[com]
        return enum


@ComDecorator(
    {'N': 'S', 'E': 'W', 'C': 'F'},
    {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N', 'C': 'F', 'F': 'C'},
    {'N': ['NS', 0], 'E': ['EW', 0], 'S': ['NS', 1], 'W': ['EW', 1], 'C': ['CF', 0], 'F': ['CF', 1]}
)
class Com(IntFlag):
    W = 0x0001
    E = 0x0002
    N = 0x0004
    S = 0x0008
    C = 0x0010
    F = 0x0020

    def __str__(self):
        text = {Com.N: "North", Com.E: "East", Com.S: "South", Com.W: "West", Com.C: "Ceiling", Com.F: 'Floor'}
        return text[self._value_]
