# encoding: utf-8
# from tkinter import Canvas
from Maze.util import Orientation, Dim
from Maze.tweak import Tweak
from Maze.wall import Wall
from Maze.cell import Cell


class Maze:
    """
        Maze is created as a rectangle of x * y cells.
    """

    def __init__(self, cells_across, cells_up, border=0):
        self.cells_across = cells_across
        self.cells_up = cells_up
        if border > cells_up/2 or border > cells_across/2:
            print("Border is too large for width and height. Setting to Border to 1")
            border = 1
        self.border = border
        self.mined = False
        self.tk_maze = None
        self.bods = []
        self.things = []
        self.level = Level(cells_across, cells_up, self.border)

        # False if (border > i >= (self.cells_across - border) and j == 0) else True
        # False if border is 0 or (border > i >= (self.cells_across - border) and border > j >= (self.cells_up - border))
        # else True

    def entrance(self, tweak):
        """
        Returns the cell for miner(s) to begin mining in.
        If the maze has an odd number of cells, we don't worry about it - they can begin in the same cell.
        But if we are even, we will get to the 'left' / 'lower' edge. (6/3 - 3, but a LR tweak needs to begin at 4)
        This is fine, except when we are a clone (have a tweak value).
        :type tweak: Tweak
        """
        return self.cell(
            tweak.entry(self.cells_across, self.border, Orientation.EW),
            tweak.entry(self.cells_up, self.border, Orientation.NS)
        )

    def mine(self):
        while not self.mined:
            for bod in self.bods:
                bod.run()
        if self.border is not 0:
            for bod in self.bods:
                bod.final()  # Allow them to tidy up..

    def do_mined(self):
        self.mined = True

    def at(self, index):
        return self.cell(index[0], index[1])

    def cell(self, cell_across, cell_up):
        return self.level.cell(cell_across, cell_up)

    def add_bod(self, bod):
        self.bods.append(bod)

    def code(self):
        return self.level.code()


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

    def _ns_wall(self, across, up):
        if across in range(self.cells_across) and up in range(self.cells_up + 1):
            return self.ns_walls[across][up]
        return None

    def _ew_wall(self, across, up):
        if across in range(0, self.cells_across + 1) and up in range(0, self.cells_up):
            return self.ew_walls[across][up]
        return None

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
