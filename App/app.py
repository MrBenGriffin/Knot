# from tkinter import *
from Maze.maze import Maze
from Bod.clone import Clone
from Bod.mazer import Mazer
# from App.config import Config
from Maze.tweak import Tweak


class App(object):
    def __init__(self, tk_root):
        self.root = tk_root
    #   self.miner = None
    #   self.maze_windows = []
    #   self.config_window = tk_root     # for the moment, we shall use root for config.
    #   self.config = Config(self.config_window, self.create_maze)

# width, height, levels, cell_size, digger, show_dig
    def create_maze(self, cells_across, cells_up, levels, cell_size, digger, show_dig):
        the_maze = Maze(cells_across, cells_up, levels, cell_size)
        # maze_window = Toplevel(self.root)
        # the_maze.tk_init(maze_window)
        miner1 = Mazer(the_maze)
        miner2 = Clone(the_maze, Tweak(Tweak.rot090), miner1)
        miner3 = Clone(the_maze, Tweak(Tweak.rot180), miner1)
        miner4 = Clone(the_maze, Tweak(Tweak.rot270), miner1)
        miner1.dig(the_maze.entrance(Tweak(Tweak.master)))
        miner2.dig(the_maze.entrance(miner2.tweak))
        miner3.dig(the_maze.entrance(miner3.tweak))
        miner4.dig(the_maze.entrance(miner4.tweak))
        the_maze.add_bod(miner1, True)
        the_maze.add_bod(miner2, True)
        the_maze.add_bod(miner3, True)
        the_maze.add_bod(miner4, True)
        # the_maze.tk_paint()
        # self.maze_windows.append(maze_window)

    @staticmethod
    def run():
        the_root = None
        # the_root = Tk()
        App(the_root)
        the_root.mainloop()


if __name__ == "__main__":
    App.run()
