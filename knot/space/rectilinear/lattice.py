# encoding: utf-8
from knot.space.rectilinear import Com
from ..lattice import Lattice as CRSLattice


class Lattice(CRSLattice):

    def set_border(self, border: [None, int]):
        if border and border > 0:
            x0 = border
            y0 = border
            # borders = (max(0, self.size[0] - border), max(0, self.size[1] - border))
            xn = self.size[0] - border
            yn = self.size[1] - border
            for yi in range(y0, yn):
                self.cells[x0, yi].wall(Com.W).block()
                self.cells[xn, yi].wall(Com.W).block()
            for xi in range(x0, xn):
                self.cells[xi, y0].wall(Com.S).block()
                self.cells[xi, yn].wall(Com.S).block()
            self.border = border
            return border
        return None

    def code(self):
        return "\n".join(
            ["".join([self.cells[i, j].code() for i in range(self.size[0])]) for j in range(self.size[1] - 1, -1, -1)]
        )

    def unicode(self):
        return "\n".join(
            ["".join([self.cells[i, j].unicode() for i in range(self.size[0])]) for j in range(self.size[1] - 1, -1, -1)]
         )
