from ..crs import Coords


class Dim(Coords):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y


