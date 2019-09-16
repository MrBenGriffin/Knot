# encoding: utf-8
from .cell import Cell


class Wall:

    def __init__(self):
        self.blocked = False
        self.doors = {}
        self.cells = {}

    def neighbour(self, cell_dir) -> [Cell, None]:
        if cell_dir not in self.cells:
            return None
        return self.cells[cell_dir]

    def make_door(self, com, tool, cut=None) -> [Cell, None]:
        # Make door towards com (from com.opposite)
        if self.doors or self.blocked or not self.cells[com] or not self.cells[com.opposite]:
            return None
        other = self.cells[com]
        start = self.cells[com.opposite]
        self.doors = tool.make(com, cut)
        other.open(tool, com.opposite)
        start.open(tool, com)
        return other

    def make_solid(self):
        self.doors = {}

    def door(self, com):
        """
        Return the door Cut (or None), according to direction.
        (Some cuts may appear different depending on what side of the wall
        you are looking through).
        :param com:
        :return:
        """
        if com not in self.doors:
            return None
        return self.doors[com]

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
        return len(self.cells) != 2

    def can_be_dug(self, com_from) -> bool:
        return not self.cells[com_from].mined() if self.can_be_door(com_from) else False

    def can_be_door(self, com_from) -> bool:
        return not self.doors and com_from in self.cells and self.cells[com_from] and not self.blocked

    def code(self, com):
        """ Return cut for the door on a particular side """
        return "O" if com not in self.doors else str(self.doors[com])

    def unicode(self, com):
        """ Return the unicode value for the cut on a particular side"""
        return 0x00 if com not in self.doors else com.mux * self.doors[com].uni
