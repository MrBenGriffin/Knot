# encoding: utf-8
from knot.space import Orientation, Com
from knot.tool import Cutter, Cut


class Wall:

    def __init__(self, orientation, x, y, blocked=False):
        self.blocked = blocked
        self.id = None
        self.x = x
        self.y = y
        self.doors = {}
        self.cells = {}
        self.orientation = orientation

    def neighbour(self, cell_dir):
        if cell_dir not in self.cells:
            return None
        return self.cells[cell_dir]

    def make_door(self, cell_dir: Com, tool: Cutter, cut: Cut = None):
        if cell_dir not in self.cells:
            return None
        other = self.cells[cell_dir]
        if not self.blocked and other:
            self.doors = tool.make(self, cell_dir, cut)
            return other
        else:
            return None

    def make_solid(self):
        self.doors = {}

    def is_wall(self) -> bool:
        return not self.doors

    def block(self):
        self.blocked = True

    def set_cell(self, cell, com):
        opp = com.opposite
        self.cells[com] = cell
        if opp not in self.cells:
            self.cells[opp] = None

    def is_edge(self):  # If on the edge, then one of my wall cells will be None.
        if self.orientation == Orientation.NS:
            return (self.cells[Com.N] is None) or (self.cells[Com.S] is None)
        else:
            return (self.cells[Com.W] is None) or (self.cells[Com.E] is None)

    def can_be_dug(self, com_from) -> bool:
        if com_from not in self.cells:
            return False
        else:
            cell = self.cells[com_from]
            return False if not cell else not (self.blocked or cell.mined)

    def code(self, com):
        return "O" if com not in self.doors else str(self.doors[com])
