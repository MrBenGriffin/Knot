from abc import ABCMeta, abstractmethod


class Mover(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def _run(self):
        pass

    def __init__(self, maze, tweak):
        self.track = []
        self.levels = 1
        self.is_miner = False
        self.maze = maze
        self.entrance = None
        self.tweak = tweak

    def run(self):
        if self.is_miner and not self.track and not self.maze.mined:
            self.maze.mined = True
        else:
            self._run()

    '''
    This isn't brilliant.
    It could start at entrance and then trace through 
    it's own maze until it finds a neighbour it's not joined to.
    Currently, if the entrance is bounded by the miner, there will be nowhere to join.
    '''
    def final(self):
        self.entrance.join()

    def enter(self, cell):
        self.entrance = cell
        self.dig(self.entrance)

    def dig(self, cell):
        if not cell.mined:
            cell.miner = self
            cell.mined = True
        self.go(cell)

    def go(self, cell):
        self.track.append(cell)

    def finished(self):
        return not self.track

    def cell(self):
        if not self.track:
            return None
        return self.track[-1]
