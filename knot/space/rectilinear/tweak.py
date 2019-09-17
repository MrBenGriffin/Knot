# encoding: utf-8
from abc import ABC, abstractmethod
from math import floor, ceil
from knot.space.crs import Tweak as CRSTweak, Wallpaper
from .dim import Com, Dim


class Tweak(CRSTweak, ABC):
    """
    Tweak provides the information for clones. It answers the following questions from a clone.
    What is my orientation to the other (self.paper).
    If the other faces West, which direction I should face? face()
    If the other is at dimension 0,0 what cell I be in?  dim()
    Given that the maze might be hollow in the middle, where should I start?
    """

    def __init__(self, paper: Wallpaper, idx: tuple, worker_no: int = 0):
        """
        :param paper: The wallpaper being used in the lattice. e.g. Paper.sunset
        :param idx: The index within the lattice of the master cell that this is a transform of.
        :param worker_no: The worker number that this paper is identifying with (0..3)
        """
        coords = Dim.adopt((max(0, idx[0] - 1), max(0, idx[1] - 1)))
        super().__init__(paper, coords, worker_no)

    @abstractmethod
    def face(self, com: Com) -> [Com, None]:
        pass

    @abstractmethod
    def dim(self, index: tuple) -> Dim:
        pass

    def entry(self, border: [int, None]) -> Dim:
        """
        Given that the structure might be hollow, where should an actor start?
        my x_off and y_off are the maximum indices of a grid.
        Normally I start at the centre of the grid at ceil((grid.x-1)/2),ceil((grid.x-1)/2)
        """
        xy = ceil(self.coords.x / 2) if not border else floor(border / 2), ceil(self.coords.y / 2) if not border else floor(border / 2)
        return self.dim(xy)
