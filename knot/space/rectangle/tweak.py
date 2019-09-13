# encoding: utf-8
from math import floor, ceil
from ..crs import Tweak as CRSTweak
from .dim import Dim
from .axes import Com, Paper


class Tweak(CRSTweak):
    """
    Tweak provides the information for clones. It answers the following questions from a clone.
    What is my orientation to the other (self.paper).
    If the other faces West, which direction I should face? face()
    If the other is at dimension 0,0 what cell I be in?  dim()
    Given that the maze might be hollow in the middle, where should I start?
    """

    def __init__(self, paper: Paper, idx: Dim, worker_no: int = 0):
        """
        :param paper: The wallpaper being used in the lattice. e.g. Paper.sunset
        :param idx: The index within the lattice of the master cell that this is a transform of.
        :param worker_no: The worker number that this paper is identifying with (0..3)
        """
        super().__init__(paper, idx, worker_no)
        self.paper = paper
        self.worker_no = worker_no
        self._dim = Dim(max(0, idx.x - 1), max(0, idx.y - 1))

    def __str__(self):
        return str(self.paper) + ' w' + str(self.worker_no)

    def __repr__(self):
        return str(self.paper) + ' w' + str(self.worker_no) + "; under " + str(self._dim)

    def face(self, com: Com) -> [Com, None]:
        if com is None:
            return None
        return com if self.worker_no == 0 else com.opposite

    def dim(self, basis: Dim) -> Dim:
        if self.worker_no == 0:
            return basis
        w1 = {
            Paper.sunset: Dim(basis.x, self._dim.y - basis.y),
            Paper.vanity: Dim(self._dim.x - basis.x, basis.y),
            Paper.mirror: Dim(self._dim.x - basis.x, self._dim.y - basis.y)
        }
        return w1[self.paper]

    def entry(self, border: [int, None]) -> Dim:
        """
        Given that the structure might be hollow, where should an actor start?
        my x_off and y_off are the maximum indices of a grid.
        Normally I start at the centre of the grid at ceil((grid.x-1)/2),ceil((grid.x-1)/2)
        """
        return self.dim(Dim(ceil(self._dim.x / 2), ceil(self._dim.y / 2) if not border else floor(border / 2)))
