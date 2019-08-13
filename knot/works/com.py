# encoding: utf-8
from enum import IntFlag

# TODO:  Com (Reverse) and Orientation - they are environmental definitions


# Decorator class.
class Reverse:
    def __init__(self, reverse_map, rotate_map):
        self.reverse_map = reverse_map
        self.rotate_map = rotate_map

    def __call__(self, enum):
        for fwd, rev in self.reverse_map.items():
            enum[fwd].opposite = enum[rev]
            enum[rev].opposite = enum[fwd]
        for fwd, rot in self.rotate_map.items():
            enum[fwd].cw = enum[rot]
            enum[rot].ccw = enum[fwd]
        return enum


@Reverse(
    {'N': 'S', 'E': 'W', 'C': 'F', 'X': 'X'},
    {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N', 'C': 'F', 'F': 'C', 'X': 'X'}
)
class Com(IntFlag):
    X = 0x0000
    W = 0x0001
    E = 0x0002
    N = 0x0004
    S = 0x0008
    C = 0x0010
    F = 0x0020

    def __str__(self):
        text = {Com.N: "North", Com.E: "East", Com.S: "South", Com.W: "West", Com.C: "Ceiling", Com.F: 'Floor', Com.X: "Nothing"}
        return text[self._value_]
