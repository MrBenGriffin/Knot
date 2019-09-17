from enum import Enum
from abc import ABC, abstractmethod


class Tool(ABC):

    @abstractmethod
    def make(self, com: Enum, cut: Enum = None) -> dict:
        pass


# Cut Decorator class.
class CutDecorator:
    def __init__(self, reverse_map, unicode_map, axis_map):
        self.reverse_map = reverse_map
        self.unicode_map = unicode_map
        self.axis_map = axis_map

    def __call__(self, enum):
        for fwd, rev in self.reverse_map.items():
            enum[fwd].opposite = enum[rev]
            enum[rev].opposite = enum[fwd]
        for x, uni in self.unicode_map.items():
            enum[x].uni = uni
        for crs, values in self.axis_map.items():
            for com, exp in values.items():
                crs[com].mux = pow(len(enum), exp)
        return enum
