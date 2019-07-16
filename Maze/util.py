# encoding: utf-8
from enum import Enum, IntFlag
# from Maze.maze import Maze


class Tweak:
    master = 0x0000
    horizon = 0x0001 # HMirror
    vanity = 0x0002  # VMirror
    mirror = 0x0003
    rot000 = 0x0004  # rotate 0
    rot090 = 0x0005  #
    rot270 = 0x0006  #
    rot180 = 0x0007  #

    def __init__(self, tweak):
        self.tweak = tweak

    def choose(self, com):
        result = com
        if (self.tweak & 4) == 4:
            if self.tweak == Tweak.rot000:
                result = com
            if self.tweak == Tweak.rot090:
                result = com.cw
            if self.tweak == Tweak.rot180:
                result = com.opposite
            if self.tweak == Tweak.rot270:
                result = com.ccw
        else:
            if (self.tweak & Tweak.horizon) == Tweak.horizon and com in (Com.N, Com.S):
                result = com.opposite
            if (self.tweak & Tweak.vanity) == Tweak.vanity and com in (Com.E, Com.W):
                result = com.opposite
        return result

    def cell(self, maze, basis):
        # maze.cells_across
        # maze.cells_up
        # master
        if self.tweak == Tweak.master:
            return basis
        x = basis.dim.x
        y = basis.dim.y
        if self.tweak == self.rot090 or self.tweak == self.rot270:
            x, y = y, x
        if self.tweak & Tweak.vanity != 0:  # not 270, not horizon
            x = (maze.cells_across - x) + self.increment(maze.cells_across, Orientation.EW)
        if self.tweak & Tweak.horizon != 0:  # not 90
            y = (maze.cells_up - y) + self.increment(maze.cells_up, Orientation.NS)
        return maze.at((x, y, basis.dim.z))

    def increment(self, length, orient):
        if length % 2 == 1:
            return -1
        if self.tweak & Tweak.horizon != 0 and orient == Orientation.NS:
            return - 1
        if self.tweak & Tweak.vanity != 0 and orient == Orientation.EW:
            return - 1
        return 0

    def entry(self, length, orient):
        if length % 2 == 1:
            return int((length - 1) / 2)
        return (length >> 1) + self.increment(length, orient)


# Decorator class.
class Reverse:
    def __init__(self, reverse_map, rotate_map):
        self.reverse_map = reverse_map
        self.rotate_map = rotate_map

    def __call__(self, enum):
        for fwd, rev in self.reverse_map.items():
            enum[fwd].opposite = enum[rev]
            enum[rev].opposite = enum[fwd]
        for fwd, rot in self.rotate_map.items():
            enum[fwd].cw = enum[rot]
            enum[rot].ccw = enum[fwd]
        return enum


@Reverse(
    {'N': 'S', 'E': 'W', 'C': 'F'},
    {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N', 'C': 'C', 'F': 'F'}
)
class Com(IntFlag):
    X = 0x0000
    W = 0x0001
    E = 0x0002
    N = 0x0004
    S = 0x0008
    C = 0x0010
    F = 0x0020


class Orientation(Enum):
    NS = True
    EW = False


class Dim:
    def __init__(self, x=None, y=None, z=None):
        if not x:
            self.x = 0
        else:
            self.x = x
        if not y:
            self.y = 0
        else:
            self.y = y
        if not z:
            self.z = 0
        else:
            self.z = z

    def __str__(self):
        return "%02x\n%02x" % (self.x, self.y)

    def __cmp__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z


if __name__ == "__main__":
    print(Com.N | Com.S)
    print(Com.W)
    print(Com.N.opposite)
    print((Com.W | Com.E | Com.N))
    print(Com.W | Com.E)
    print(Com.C)
    print(Com.C.opposite)
