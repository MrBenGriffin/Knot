# encoding: utf-8
from knot.space import Dim
from .level import Level
from .cell import Cell


class Structure:
    """
        works is created as a rectangle of x * y cells.
    """

    def __init__(self, cells_across, cells_up, border=0):
        self.cells_across = cells_across
        self.cells_up = cells_up
        if border > cells_up/2 or border > cells_across/2:
            print("Border is too large for width and height. Setting to Border to 0")
            border = 0
        self.border = border
        self.mined = False
        self.joined = False
        self.bods = []
        self.things = []
        self.level = Level(cells_across, cells_up, self.border, True, True)

    def mine(self):
        while not self.mined:
            for bod in self.bods:
                bod.run()

    def join(self):
        while not self.joined:
            for bod in self.bods:
                bod.run()

    def do_mined(self):
        self.mined = True

    def at(self, index: Dim) -> Cell:
        return self.cell(index.x, index.y)

    def cell(self, cell_across, cell_up):
        return self.level.cell(cell_across, cell_up)

    def add_bod(self, bod):
        self.bods.append(bod)

    def code(self):
        return self.level.code()
