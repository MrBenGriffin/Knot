from ..crs import Coords


class Dim(Coords):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    def __repr__(self):
        return "<Dim>(" + str(self.x) + "," + str(self.y) + ")"

    def __eq__(self, other):
        if isinstance(other, Dim):
            return self.x == other.x and self.y == other.y
        if isinstance(other, tuple):
            return self.x == other[0] and self.y == other[1]
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, Dim):
            return self.x != other.x or self.y != other.y
        if isinstance(other, tuple):
            return self.x != other[0] or self.y != other[1]
        return NotImplemented
