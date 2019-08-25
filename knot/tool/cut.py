# encoding: utf-8
from enum import Enum
# import random


# Decorator class.
class CutDecorator:
    def __init__(self, reverse_map, unicode_map):
        self.reverse_map = reverse_map
        self.unicode_map = unicode_map

    def __call__(self, enum):
        for fwd, rev in self.reverse_map.items():
            enum[fwd].opposite = enum[rev]
            enum[rev].opposite = enum[fwd]
        for x, uni in self.unicode_map.items():
            enum[x].uni = uni
        return enum


@CutDecorator(
    {'O': 'O', 'I': 'I', 'X': 'X', 'H': 'B'},
    {'O': 0, 'I': 2, 'X': 1, 'H': 3, 'B': 4}
)
class Cut(Enum):
    O = 1
    I = 2
    X = 3
    H = 4
    B = 5

    def __str__(self):
        text = {1: "O", 2: "I", 3: "X", 4: "H", 5: "B"}
        return text[self._value_]
