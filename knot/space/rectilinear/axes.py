# encoding: utf-8
from enum import Enum
from ..crs import AxesDecorator, ComDecorator, Symmetry


@AxesDecorator(
    {'NS': [], 'EW': []},
    {'NS': (Symmetry.V, Symmetry.H), 'EW': (Symmetry.H, Symmetry.V)})
class Axis(Enum):
    NS = 0x0100
    EW = 0x0200

    def __str__(self):
        text = {Axis.NS: "NS", Axis.EW: "EW"}
        return text[self]


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
        return text[self]
