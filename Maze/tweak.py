# encoding: utf-8
from math import floor, ceil
from enum import IntFlag
from Maze.util import Dim
from Maze.com import Com


class Tw(IntFlag):
    master = 0x0000
    horizon = 0x0001  # HMirror
    vanity = 0x0002   # VMirror
    mirror = 0x0003
    rot000 = 0x0004  # rotate 0
    rot090 = 0x0005  #
    rot270 = 0x0006  #
    rot180 = 0x0007  #


class Tweak:
    """
    Tweak provides the information for clones. It answers the following questions from a clone.

    What is my orientation to the other (self.tweak).

    If the other faces West, which direction I should face? face()

    If the other is at dimension 0,0 what cell I be in?  dim()

    Given that the maze might be hollow in the middle, where should I start?

    """
    def __str__(self):
        text = {Tw.master: "As is", Tw.horizon: "Horizon", Tw.vanity: "Vanity",
                Tw.mirror: "Mirror", Tw.rot000: "Rotate 000", Tw.rot090: 'Rotate 090',
                Tw.rot180: "Rotate 180", Tw.rot270: "Rotate 270"}
        return text[self.tweak]

    def __init__(self, tweak, width, height):
        self.tweak = tweak
        self.x_off = width - 1
        self.y_off = height - 1

    def face(self, com: Com) -> Com:
        if self.tweak == Tw.master or self.tweak == Tw.rot000:
            return com
        if self.tweak == Tw.rot090:
            return com.cw
        if self.tweak == Tw.rot270:
            return com.ccw
        if (self.tweak == Tw.rot180) or \
                (self.tweak == Tw.mirror) or \
                (self.tweak == Tw.horizon and com in (Com.N, Com.S)) or \
                (self.tweak == Tw.vanity and com in (Com.E, Com.W)):
            return com.opposite
        return com

    def dim(self, basis: Dim) -> Dim:
        if self.tweak == Tw.master:
            return basis
        x = basis.x
        y = basis.y
        # result = Dim(basis.x, basis.y)
        if self.tweak == Tw.rot090 or self.tweak == Tw.rot270:
            x, y = y, x
        if self.tweak & Tw.vanity != 0:  # not 270, not horizon
            x = self.x_off - x
        if self.tweak & Tw.horizon != 0:  # not 90
            y = self.y_off - y
        return Dim(x, y)

    def entry(self, border: int = 0) -> Dim:
        return self.dim(Dim(ceil(self.x_off/2), ceil(self.y_off/2) if border is 0 else floor(border/2)))
