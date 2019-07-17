from abc import ABCMeta, abstractmethod
# from tkinter import HIDDEN, NORMAL
from Maze.cell import Cell


class Mover(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def _run(self):
        pass

    def __init__(self, maze):
        self.track = []
        self.levels = 1
        self.is_miner = False
        self.maze = maze
        self.goal = None
        # self.ids = []
        # self.canvases = []
        # self.halo = None
        # self.body = None
        # self.size = Cell.size - Cell.size // 4
        # self.offset = Cell.size // 4

    def run(self):
        if self.is_miner and not self.track and not self.maze.mined:
            self.maze.mined = True
        else:
            self._run()

    def dig(self, cell):
        cell.mined = True
        self.go(cell)

    def go(self, cell):
        self.track.append(cell)

    def finished(self):
        return not self.track or (self.goal and self.track[-1] == self.goal.track[-1])

    def cell(self):
        if not self.track:
            return None
        return self.track[-1]

    # def tk_init(self, maze):
    #     self.maze = maze
    #     self.levels = len(maze.levels)
    #     for level in maze.levels:
    #         self.canvases.append(level.tk_level)
    #         canvas = level.tk_level
    #         canvas_id = canvas.create_oval(self.offset, self.offset, self.size, self.size, outline=self.halo,
    #                                        fill=self.body, state=HIDDEN)
    #         self.ids.append(canvas_id)

   # def tk_move(self, dim):
    #     if not self.finished():
    #         x = dim.x * Cell.size + self.offset
    #         y = dim.y * Cell.size + self.offset
    #         canvas = self.canvases[dim.z]
    #         canvas_id = self.ids[dim.z]
    #         canvas.coords(canvas_id, x, y, x + self.size, y + self.size)

    # def tk_paint(self):
    #     dim = None
    #     if self.finished() and not self.is_miner:
    #         dim = self.track[-1].dim
    #         self.canvases[dim.z].itemconfig(self.ids[dim.z], state=NORMAL, width=4)
    #         self.tk_move(dim)
    #
    #     if not self.finished():
    #         dim = None
    #         if self.track:
    #             dim = self.track[-1].dim
    #         self._run()
    #         if self.track:
    #             if dim:
    #                 self.tk_move(dim)
    #             else:
    #                 self.tk_move(self.track[-1])
    #
    #     for z in range(self.levels):
    #         if dim and z == dim.z:
    #             self.canvases[z].itemconfig(self.ids[z], state=NORMAL)
    #         else:
    #             self.canvases[z].itemconfig(self.ids[z], state=HIDDEN)
