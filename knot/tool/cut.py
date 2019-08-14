# encoding: utf-8
from enum import Enum
# import random


# Decorator class.
class Reverse:
    def __init__(self, reverse_map):
        self.reverse_map = reverse_map

    def __call__(self, enum):
        for fwd, rev in self.reverse_map.items():
            enum[fwd].opposite = enum[rev]
            enum[rev].opposite = enum[fwd]
        return enum


@Reverse(
    {'O': 'O', 'I': 'I', 'X': 'X', 'H': 'B'}
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
