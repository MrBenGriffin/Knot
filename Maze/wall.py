# encoding: utf-8
import random
from tkinter import HIDDEN
from Maze.cell import Cell
from Maze.util import Dim, Com, Orientation


class Concrete:
    kinds = (
        (' ', '╴', '╶', '─', '╵', '┘', '└', '┴', '╷', '┐', '┌', '┬', '│', '┤', '├', '┼'),
        (' ', '╸', '╺', '━', '╹', '┛', '┗', '┻', '╻', '┓', '┏', '┳', '┃', '┫', '┣', '╋'),
        (' ', '╸', '╺', '═', '╹', '╝', '╚', '╩', '╻', '╗', '╔', '╦', '║', '╣', '╠', '╬')
    )

    def __init__(self, value=0, kind=1):
        self.corner = Concrete.kinds[kind][value & 0x0F]

    def __repr__(self):
        return self.corner


class Corner:
    def __init__(self, wall_dict):
        self.concrete = None
        self.walls = wall_dict   # N,E,S,W

    def __str__(self):
        value = Com.X
        for com, wall in self.walls.items():
            if wall and wall.is_wall():
                value |= com
        return str(Concrete(value))


class Wall:
    # following statics are used for text-drawing.
    prev_ew = False
    straights_balance = 333
    zoomorph_balance = 200

    solids = {
        Orientation.NS: (0, 0, 1, 0),
        Orientation.EW: (0, 1, 0, 0)
    }

    def __init__(self, orientation, x, y, level):
        self.level = level
        self.blocked = False
        self.id = None
        self.x = x
        self.y = y
        self.door = "▦"
        self.doors = {}
        self.cells = {}
        # We need the orientation in order to draw the right wall..
        self.orientation = orientation
        self.solid = tuple(10 + Cell.size * i + Cell.size * j for i, j in zip(
            Wall.solids[self.orientation],
            (self.x, self.y, self.x, self.y)
        ))

    def make_door(self, cell_dir, kind=None):
        if cell_dir not in self.cells:
            return None
        other = self.cells[cell_dir]
        if not self.blocked and other:
            opp = {"I": "I", "X": "X", "H": "B", "B": "H"}
            self.door = " "
            other.mined = True
            if self.level.tk_level:
                self.level.tk_level.itemconfig(self.id, state=HIDDEN)
            if kind is None:
                # straights_balance; 0 = All twists, 1000=all straights
                kind = "I"
                straights = random.randint(0, 1000)
                if straights < Wall.straights_balance:
                    # zoomorph_balance; 0 = All twists, 1000=all Zoomorphs.
                    kind = "X"
                    zoos = random.randint(0, 1000)
                    if zoos < Wall.zoomorph_balance:
                        kind = random.choice(("H", "B"))
                self.doors[cell_dir] = kind
                self.doors[cell_dir.opposite] = opp[kind]
            else:
                self.doors[cell_dir] = kind
                self.doors[cell_dir.opposite] = opp[kind]
            return other
        else:
            return None

    def make_solid(self):
        self.door = "▦"

    def is_wall(self) -> bool:
        return self.door == "▦"

    def set_cell(self, cell, com):
        opp = com.opposite
        self.cells[com] = cell
        self.doors[com] = 'O'
        self.doors[opp] = 'O'
        if opp not in self.cells:
            self.cells[opp] = None

    def is_edge(self):  # If on the edge, then one of my wall cells will be None.
        if self.orientation == Orientation.NS:
            return (self.cells[Com.N] is None) or (self.cells[Com.S] is None)
        else:
            return (self.cells[Com.W] is None) or (self.cells[Com.E] is None)

    def can_be_dug(self, com_from):
        cell = self.cells[com_from]
        return not self.blocked and cell and not cell.mined

    def __str__(self):
        if not self.is_wall():
            return ' '
        if self.orientation == Orientation.NS:
            return str(Concrete(Com.E | Com.W))
        return str(Concrete(Com.N | Com.S))

    def code(self, com):
        return "O" if com not in self.doors else self.doors[com]

    def tk_paint(self):
        if self.level.tk_level:
            if self.is_wall():
                self.id = self.level.tk_level.create_line(self.solid, width=2)
            else:
                self.id = self.level.tk_level.create_line(self.solid, width=2, state=HIDDEN)


class Floor:
    """
    Represents a 'floor' between two cells.
    The cell floor is the lower cell's ceiling.
    the Com.C is the cell that sees this as a ceiling.
    the Com.F is the cell that sees this as a floor.
    """

    def __init__(self, floor, ceiling):
        self.cells = {Com.C: ceiling, Com.F: floor}
        self.solid = True
        self.tk_c = self.tk_f = None
        if ceiling:
            ceiling.floors[Com.C] = self
        floor.floors[Com.F] = self
        t = floor.walls[Com.N].solid
        b = floor.walls[Com.S].solid
        self.p = Dim(b[0] + 4, t[1] - 4, 0)
        self.q = Dim(b[2] - 4, b[1] + 4, 0)

    def make_hole(self, com):
        self.solid = False
        this = self.cells[com]
        other = self.cells[com.opposite]
        if this:
            self.tk_paint(this)
        if other:
            self.tk_paint(other)
        return other

    def tk_paint(self, cell):
        if self.solid:
            return
        if cell == self.cells[Com.C]:
            if cell.level.tk_level:
                self.tk_c = cell.level.tk_level.create_line(
                    (
                        self.p.x, self.p.y, self.q.x, self.p.y, self.q.x, self.q.y, self.p.x,
                        self.p.y),
                    width=2, fill='red')
        elif cell == self.cells[Com.F]:
            if cell.level.tk_level:
                self.tk_f = cell.level.tk_level.create_line(
                    (
                        self.p.x, self.p.y, self.p.x, self.q.y, self.q.x, self.p.y, self.p.x,
                        self.p.y),
                    width=2, fill='blue')

