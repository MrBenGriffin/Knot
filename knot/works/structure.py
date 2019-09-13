# encoding: utf-8
from knot.space import Coords, Shape
from .lattice import Lattice
from .cell import Cell


class Structure:
    """
        works is created as a lattice of cells.
    """
    # {'width': 11, 'height': 11, 'straights': 0.2, 'zoo': 0.2, 'symmetry'
    #  : < Wallpaper.rot090: 5 >, 'border': None, 'htile': True, 'vtile': True, 'connectivity': 12, 'random': 1337}

    def __init__(self, cells_across: int, cells_up: int, border: [None, int], shape: Shape = None,  h_wrap: bool = False, v_wrap: bool = False):
        self.cells_across = cells_across
        self.cells_up = cells_up
        self.shape = shape
        self.dim = shape.dim
        if border and (border > cells_up/2 or border > cells_across/2):
            print("Border is too large for width and height.")
            border = None
        self.border = border
        self.mined = False
        self.joined = False
        self.bods = []
        self.things = []
        self.level = Lattice(cells_across, cells_up, self.border, h_wrap, v_wrap)

    def size(self):
        return self.dim(self.cells_across, self.cells_up)

    def mine(self):
        while not self.mined:
            for bod in self.bods:
                bod.run()
        # self.bods[0].run()
        # self.bods[3].run()
        # self.bods[0].run()
        # self.bods[3].run()

    def join(self):
        while not self.joined:
            for bod in self.bods:
                bod.run()

    def do_mined(self):
        self.mined = True

    def at(self, index: Coords) -> Cell:
        return self.level.cell(index)

    def add_bod(self, bod):
        self.bods.append(bod)

    def code(self):
        return self.level.code()

    def unicode(self):
        return self.level.unicode()
