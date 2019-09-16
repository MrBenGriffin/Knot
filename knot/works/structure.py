# encoding: utf-8
from knot.space import Coords, Shape, Cell


class Structure:
    """
        works is created as a lattice of cells.
    """
    # {'width': 11, 'height': 11, 'straights': 0.2, 'zoo': 0.2, 'symmetry'
    #  : < Wallpaper.rot090: 5 >, 'border': None, 'htile': True, 'vtile': True, 'connectivity': 12, 'random': 1337}
    # shape, args['dimensions']
    def __init__(self, shape: Shape, size: tuple, border: [None, int], wrap: tuple):
        self.shape = shape
        self.mined = False
        self.joined = False
        self.bods = []
        self.things = []
        self.lattice = shape.lattice(size, wrap)
        self.size = self.lattice.size
        self.border = self.lattice.set_border(border)

    def mine(self):
        while not self.mined:
            self.mined = True
            for bod in self.bods:
                if not bod.finished:
                    self.mined = False
                    bod.run()

    def join(self):
        while not self.joined:
            self.joined = True
            for bod in self.bods:
                if not bod.finished:
                    self.joined = False
                    bod.run()

    def do_mined(self):
        self.mined = True

    def at(self, index: Coords) -> Cell:
        return self.lattice.cell(index)

    def add_bod(self, bod):
        self.bods.append(bod)

    def code(self):
        return self.lattice.code()

    def unicode(self):
        return self.lattice.unicode()
