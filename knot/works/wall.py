# encoding: utf-8
import random
from .orientation import Orientation
from .com import Com
from .tw import Tw


class Wall:
    straights_balance = 333
    zoomorph_balance = 200

    solids = {
        Orientation.NS: (0, 0, 1, 0),
        Orientation.EW: (0, 1, 0, 0)
    }

    def __init__(self, orientation, x, y, blocked=False):
        self.blocked = blocked
        self.door = False
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

   # TODO: Make a Tool class for digging types of door The work below isn't really about walls...
    def make_door(self, cell_dir, kind=None, tweak=None):
        if cell_dir not in self.cells:
            return None
        other = self.cells[cell_dir]
        if not self.blocked and other:
            opp = {"O": "O", "I": "I", "X": "X", "H": "B", "B": "H"}
            self.door = True
            other.mined = True
            if kind is None:
                # straights_balance; 0 = All twists, 1000=all straights
                kind = "I"
                straights = random.randint(0, 1000)
                if straights < Wall.straights_balance:
                    # zoomorph_balance; 0 = All twists, 1000=all Zoomorphs.
                    kind = "X"
                    zoos = random.randint(0, 1000)
                    if zoos < Wall.zoomorph_balance:
                        kind = random.choice(("H", "B"))
                self.doors[cell_dir] = kind
                self.doors[cell_dir.opposite] = opp[kind]
            else:
                # This seems backward, but it's not.  The cell is already digging the opposite wall,
                # and so doesn't need to worry about that part.  But the EW will look odd if unaffected by the mirror.
                # It's still not a true mirror image, as types are always CCW oriented.
                if (tweak is Tw.horizon and self.orientation is Orientation.EW) or \
                   (tweak is Tw.vanity and self.orientation is Orientation.NS):
                    self.doors[cell_dir.opposite] = kind
                    self.doors[cell_dir] = opp[kind]
                else:
                    self.doors[cell_dir] = kind
                    self.doors[cell_dir.opposite] = opp[kind]
            return other
        else:
            return None

    def make_solid(self):
        self.door = False

    def is_wall(self) -> bool:
        return not self.door

    def block(self):
        self.blocked = True

    def set_cell(self, cell, com):
        opp = com.opposite
        self.cells[com] = cell
        self.doors[com] = 'O'
        self.doors[opp] = 'O'
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
        return "O" if com not in self.doors else self.doors[com]
