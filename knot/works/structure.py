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
        if border:
            for axis in self.size:
                if border > axis / 2:
                    border = min(0, int(axis/2 - 1))
                    print("Border was too large for width and height. Resized to " + str(border))
        self.border = None if not border or border == 0 else border
        self.mined = False
        self.joined = False
        self.bods = []
        self.things = []
        self.level = shape.lattice(size, wrap)
        self.size = self.level.size
    #     TODO:: Border is not managed.

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

    def at(self, index: Coords) -> Cell:
        return self.level.cell(index)

    def add_bod(self, bod):
        self.bods.append(bod)

    def code(self):
        return self.level.code()

    def unicode(self):
        return self.level.unicode()
