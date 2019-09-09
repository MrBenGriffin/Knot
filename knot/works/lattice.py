# encoding: utf-8
from knot.space import Axis, Dim
from .wall import Wall
from .cell import Cell


class Lattice:
    def __init__(self, cells_across, cells_up, border, h_wrap=False, v_wrap=False):
        self.cells_across = cells_across
        self.cells_up = cells_up
        self.h_range = cells_across if h_wrap else cells_across + 1
        self.v_range = cells_up if v_wrap else cells_up + 1
        self.v_wrap = v_wrap
        self.h_wrap = h_wrap
        self.ns_walls = [[
            Wall(Axis.NS, i, j)
            for j in range(self.v_range)] for i in range(self.cells_across)]

        self.ew_walls = [[
            Wall(Axis.EW, i, j)
            for j in range(self.cells_up)] for i in range(self.h_range)]
        self.cells = [[
            Cell(Dim(i, j),
                 (self.ns(Dim(i, j + 1)), self.ew(Dim(i + 1, j)), self.ns(Dim(i, j)), self.ew(Dim(i, j))),
                 True if border and
                         (border <= i < self.cells_across - border) and
                         (border <= j < self.cells_up - border) else False
                 )
            for j in range(self.cells_up)]
            for i in range(self.cells_across)]

    def pole(self, index: Dim, map_to_use):
        x = index.x % self.h_range if self.h_wrap else index.x
        y = index.y % self.v_range if self.v_wrap else index.y
        if x in range(0, self.h_range) and y in range(0, self.v_range):
            return map_to_use[x][y]
        return None

    def ns(self, index: Dim):
        return self.pole(index, self.ns_walls)

    def ew(self, index: Dim):
        return self.pole(index, self.ew_walls)

    def cell(self, index: Dim):
        return self.pole(index, self.cells)

    def code(self):
        return "\n".join(
            ["".join([self.cell(Dim(i, j)).code() for i in range(self.cells_across)]) for j in range(self.cells_up - 1, -1, -1)]
        )

    def unicode(self):
        return "\n".join(
            ["".join([self.cell(Dim(i, j)).unicode() for i in range(self.cells_across)]) for j in range(self.cells_up - 1, -1, -1)]
        )
