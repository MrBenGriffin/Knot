# encoding: utf-8
from enum import IntFlag
from Maze.util import Orientation, Com


class Tw(IntFlag):
    master = 0x0000
    horizon = 0x0001  # HMirror
    vanity = 0x0002  # VMirror
    mirror = 0x0003
    rot000 = 0x0004  # rotate 0
    rot090 = 0x0005  #
    rot270 = 0x0006  #
    rot180 = 0x0007  #


class Tweak:

    def __init__(self, tweak):
        self.tweak = tweak

    def choose(self, com):
        result = com
        if (self.tweak & 4) == 4:
            if self.tweak == Tw.rot000:
                result = com
            if self.tweak == Tw.rot090:
                result = com.cw
            if self.tweak == Tw.rot180:
                result = com.opposite
            if self.tweak == Tw.rot270:
                result = com.ccw
        else:
            if (self.tweak & Tw.horizon) == Tw.horizon and com in (Com.N, Com.S):
                result = com.opposite
            if (self.tweak & Tw.vanity) == Tw.vanity and com in (Com.E, Com.W):
                result = com.opposite
        return result

    def cell(self, maze, basis):
        # maze.cells_across
        # maze.cells_up
        # master
        if self.tweak == Tw.master:
            return basis
        x = basis.dim.x
        y = basis.dim.y
        if self.tweak == Tw.rot090 or self.tweak == Tw.rot270:
            x, y = y, x
        if self.tweak & Tw.vanity != 0:  # not 270, not horizon
            x = (maze.cells_across - x) + self.increment(maze.cells_across, Orientation.EW)
        if self.tweak & Tw.horizon != 0:  # not 90
            y = (maze.cells_up - y) + self.increment(maze.cells_up, Orientation.NS)
        return maze.at((x, y, basis.dim.z))

    def increment(self, length, orient):
        if length % 2 == 1:
            return -1
        if self.tweak == Tw.horizon != 0 and orient == Orientation.NS:
            return - 1
        if self.tweak == Tw.vanity != 0 and orient == Orientation.EW:
            return - 1
        return 0

    def entry(self, length, border, orient):
        if border is 0:
            centre = int((length - 1) / 2)
            if length % 2 != 1:
                centre = (length >> 1) + self.increment(length, orient)
            return centre
        else:
            offset = int((border - 1) / 2)
            if border % 2 != 1:
                offset = (border >> 1) + self.increment(border, orient)
            if self.tweak is Tw.mirror or self.tweak is Tw.rot180:
                return length - offset - 1
            if self.tweak is Tw.master or \
                    (self.tweak == Tw.horizon and orient == Orientation.NS) or \
                    (self.tweak == Tw.vanity and orient == Orientation.EW) or \
                    (self.tweak is Tw.rot090 and orient == Orientation.NS) or \
                    (self.tweak is Tw.rot270 and orient == Orientation.EW):
                return offset
            else:
                return length - offset - 1
