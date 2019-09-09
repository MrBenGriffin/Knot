# encoding: utf-8
from enum import Enum
from .square.square import Square

"""
cf. https://www.redblobgames.com/grids/hexagons/
    https://www.redblobgames.com/grids/hexagons/implementation.html
"""


class ShapeDecorator:
    def __init__(self, shape_map):
        self.shape_map = shape_map

    def __call__(self, enum):
        for name, system in self.shape_map.items():
            crs = system()
            enum[name].tweak = crs.tweak()
            enum[name].dim = crs.dim()
            enum[name].axis = crs.axis()
            enum[name].com = crs.com()
            enum[name].wallpaper = crs.paper()
        return enum


@ShapeDecorator({'squared': Square, 'rectang': Square})
class Shape(Enum):
    squared = 1  # square map.
    rectang = 2  # rectangular map.
    # hex_map = 3  # a even-odd rectangle (hexagons - allows mirror - using 'even-q' coordinates.)
    # rhombus = 4  # a twisted rectangle (hexagons - allows mirror)
    # hexagon = 5  # a hexagon of hexagons (allows 6-rotation)
    # pyramid = 6  # a triangle of hexagons (allows 3-rotation)
