# encoding: utf-8
from knot.space import Orientation, Dim
from .wall import Wall
from .cell import Cell


# TODO:: Open up horizontal and vertical wrap-around options.
class Level:
    def __init__(self, cells_across, cells_up, border, h_wrap=False, v_wrap=False):
        self.cells_across = cells_across
        self.cells_up = cells_up
        self.h_range = cells_across if h_wrap else cells_across + 1
        self.v_range = cells_up if v_wrap else cells_up + 1
        # self.h_range = cells_across + 1
        # self.v_range = cells_up + 1
        self.v_wrap = v_wrap
        self.h_wrap = h_wrap
        self.ns_walls = [[
            Wall(Orientation.NS, i, j)
            for j in range(self.v_range)] for i in range(self.cells_across)]

        self.ew_walls = [[
            Wall(Orientation.EW, i, j)
            for j in range(self.cells_up)] for i in range(self.h_range)]
        self.cells = [[
            Cell(Dim(i, j),
                 (self.ns(i, j + 1), self.ew(i + 1, j), self.ns(i, j), self.ew(i, j)),
                 True if border > 0 and
                         (border <= i < self.cells_across - border) and
                         (border <= j < self.cells_up - border) else False
                 )
            for j in range(self.cells_up)]
            for i in range(self.cells_across)]

    def ns(self, across, up):
        x = across % self.h_range if self.h_wrap else across
        y = up % self.v_range if self.v_wrap else up
        if x in range(0, self.h_range) and y in range(0, self.v_range):
            return self.ns_walls[x][y]
        return None

    def ew(self, across, up):
        x = across % self.h_range if self.h_wrap else across
        y = up % self.v_range if self.v_wrap else up
        if x in range(0, self.h_range) and y in range(0, self.v_range):
            return self.ew_walls[x][y]
        return None

    def cell(self, across, up):
        x = across % self.cells_across if self.h_wrap else across
        y = up % self.cells_up if self.v_wrap else up
        if x in range(0, self.cells_across) and y in range(0, self.cells_up):
            return self.cells[x][y]
        return None

    def code(self):
        result = ""
        for j in reversed(range(self.cells_up)):  # reversed: print goes from top to bottom..
            for i in range(self.cells_across):
                result += self.cell(i, j).code()
            result = result + "\n"
        return result
