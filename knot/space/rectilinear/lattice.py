# encoding: utf-8
from ..lattice import Lattice as CRSLattice


class Lattice(CRSLattice):

    def code(self):
        return "\n".join(
            ["".join([self.cells[i, j].code() for i in range(self.size[0])]) for j in range(self.size[1] - 1, -1, -1)]
        )

    def unicode(self):
        return "\n".join(
            ["".join([self.cells[i, j].unicode() for i in range(self.size[0])]) for j in range(self.size[1] - 1, -1, -1)]
         )
