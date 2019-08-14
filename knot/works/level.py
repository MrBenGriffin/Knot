# encoding: utf-8
from knot.space import Orientation, Dim
from .wall import Wall
from .cell import Cell


class Level:
    def __init__(self, cells_across, cells_up, border):
        self.cells_across = cells_across
        self.cells_up = cells_up

        self.ns_walls = [[
            Wall(Orientation.NS, i, j)
            for j in range(self.cells_up + 1)] for i in range(self.cells_across)]

        self.ew_walls = [[
            Wall(Orientation.EW, i, j)
            for j in range(self.cells_up)] for i in range(self.cells_across + 1)]

        self.cells = [[
            Cell(Dim(i, j), self.ns_walls, self.ew_walls,
                 True if border > 0 and
                    (border <= i < self.cells_across - border) and
                    (border <= j < self.cells_up - border) else False
                 )
            for j in range(self.cells_up)]
            for i in range(self.cells_across)]

    def cell(self, across, up):
        if across in range(0, self.cells_across) and up in range(0, self.cells_up):
            return self.cells[across][up]
        return None

    def code(self):
        result = ""
        for j in reversed(range(self.cells_up)):  # reversed: print goes from top to bottom..
            for i in range(self.cells_across):
                result += self.cell(i, j).code()
            result = result + "\n"
        return result
