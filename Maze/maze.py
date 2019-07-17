# encoding: utf-8
# from tkinter import Canvas
from Maze.util import Orientation, Com, Dim, Tweak
from Maze.wall import Wall, Floor, Corner
from Maze.cell import Cell


class Maze:
    """
        Maze is created as a rectangle (cuboid) of x * y (*z) cells.

        Each Maze is made of 1...X levels.
        Each Maze level has it's own Canvas..
        For the time being, each level uses the same dimensions..
        (Not hard to change this).

    """
    start = (0, 0, 0)

    def __init__(self, cells_across, cells_up, depth, cell_size):
        self.cells_across = cells_across
        self.cells_up = cells_up
        # self.base = (int(cells_across/2), int(cells_up/2), 0)
        self.depth = depth
        self.mined = False
        self.tk_maze = None
        self.bods = []
        self.things = []
        self.levels = []
        # print("Making maze:", cells_across, cells_up, depth)
        for level in range(self.depth):
            floor = Level(cells_across, cells_up, cell_size, level)
            self.levels.append(floor)
        for level in self.levels:
            level.set_floor(self)

    def entrance(self, tweak):
        """
        Returns the cell for miner(s) to begin mining in.
        If the maze has an odd number of cells, we don't worry about it - they can begin in the same cell.
        But if we are even, we will get to the 'left' / 'lower' edge. (6/3 - 3, but a LR tweak needs to begin at 4)
        This is fine, except when we are a clone (have a tweak value).
        :type tweak: Tweak
        """
        return self.cell(
            tweak.entry(self.cells_across, Orientation.EW),
            tweak.entry(self.cells_up, Orientation.NS),
            0)

    def mine(self):
        while not self.mined:
            for bod in self.bods:
                bod.run()

    def do_mined(self):
        # This happens just once after the miners are done.
        # So we can post-process the mine here.
        self.mined = True
        for level in self.levels:
            level.erode()

    def at(self, index):
        return self.cell(index[0], index[1], index[2])

    def cell(self, cells_across, cells_up, level=None):
        if level is None or level not in range(0, self.depth):
            return None
        return self.levels[level].cell(cells_across, cells_up)

    def add_thing(self, cell, thing):
        if self.tk_maze:
            self.things.append(thing)
            thing.tk_init(self, cell)

    def add_bod(self, bod, show):
        if show or self.tk_maze:
            self.bods.append(bod)
            if self.tk_maze:
                bod.tk_init(self)
        else:
            while not bod.finished():
                bod.run()
                self.do_mined()

    # def tk_init(self, root):
    #     self.tk_maze = root
    #     self.tk_maze.title("Maze")
    #     for level in self.levels:
    #         level.tk_level = Canvas(self.tk_maze,
    #                                 width=20 + Cell.size * (self.cells_across + 0),
    #                                 height=20 + Cell.size * (self.cells_up + 0),
    #                                 bg='gray')
    #         level.tk_level.grid(columns=1, rows=1)
    #     self.tk_maze.after(0, self.animation)

    # def animation(self):
    #     for bod in self.bods:
    #         if bod.is_miner:
    #             if not self.mined:
    #                 bod.tk_paint()
    #         else:
    #             if self.mined:
    #                 bod.tk_paint()
    #     for thing in self.things:
    #         thing.tk_paint()
    #     self.tk_maze.after(50, self.animation)
    #
    # def tk_paint(self):
    #     for level in self.levels:
    #         level.tk_paint()

    def string(self):
        result = ""
        for level in self.levels:
            result += level.string()
        return result

    def code(self):
        result = ""
        for level in self.levels:
            result += level.code()
        return result


class Level:
    def __init__(self, cells_across, cells_up, cell_size, level):
        Cell.size = cell_size
        self.level = level
        self.tk_level = None
        self.cells_across = cells_across
        self.cells_up = cells_up
        self.floors = []

        self.ns_walls = [[
            Wall(Orientation.NS, i, j, self)
            for j in range(self.cells_up + 1)] for i in range(self.cells_across)]

        self.ew_walls = [[
            Wall(Orientation.EW, i, j, self)
            for j in range(self.cells_up)] for i in range(self.cells_across + 1)]

        self.cells = [[
            Cell(Dim(i, j, level), self.ns_walls, self.ew_walls, self)
            for j in range(self.cells_up)]
            for i in range(self.cells_across)]

        # Corner is top left of each cell.
        # So at cell 0,0 the corner sees the ns wall 0,0 as being East... +
        self.corners = [[
            Corner({Com.N: self._ew_wall(i, j - 1), Com.W: self._ns_wall(i - 1, j),
                    Com.S: self._ew_wall(i, j), Com.E: self._ns_wall(i, j)})
            for j in range(self.cells_up+1)]
            for i in range(self.cells_across+1)]

    def set_floor(self, maze):
        self.floors = [[Floor(self.cells[i][j], maze.cell(i, j, self.level + 1))
                       for j in range(self.cells_up)]
                       for i in range(self.cells_across)]

    def _ns_wall(self, across, up):
        if across in range(self.cells_across) and up in range(self.cells_up+1):
            return self.ns_walls[across][up]
        return None

    def _ew_wall(self, across, up):
        if across in range(0, self.cells_across+1) and up in range(0, self.cells_up):
            return self.ew_walls[across][up]
        return None

    def cell(self, across, up):
        if across in range(0, self.cells_across) and up in range(0, self.cells_up):
            return self.cells[across][up]
        return None

    # def tk_paint(self):
    #     for i in range(len(self.ns_walls)):
    #         for j in range(len(self.ns_walls[i])):
    #             self.ns_walls[i][j].tk_paint()
    #     for i in range(len(self.ew_walls)):
    #         for j in range(len(self.ew_walls[i])):
    #             self.ew_walls[i][j].tk_paint()
    #     for i in range(len(self.cells)):
    #         for j in range(len(self.cells[i])):
    #             self.floors[i][j].tk_paint(self.cells[i][j])

    def string(self):  # __str__ method here is just for easy visualisation purposes.
        line = "Level %s\n" % (1 + self.level)
        for j in range(self.cells_up+1):  # reversed: print goes from top to bottom..
            line_ns = ""
            line_ew = ""
            for i in range(self.cells_across+1):
                line_ns += str(self.corners[i][j])
                if self._ns_wall(i, j):
                    line_ns += str(self._ns_wall(i, j))
                if self._ew_wall(i, j):
                    line_ew += str(self._ew_wall(i, j))
                if self.cell(i, j):
                    line_ew += str(self.cell(i, j))
            line += line_ns + "\n" + line_ew + "\n"
        return line

    def code(self):
        result = ""
        for j in reversed(range(self.cells_up)):  # reversed: print goes from top to bottom..
            for i in range(self.cells_across):
                result += self.cell(i, j).code()
            result = result + "\n"
        return result
