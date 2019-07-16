import os
import sys
import random
from Maze.maze import Maze
from Bod.mazer import Mazer
from Bod.clone import Clone
from Maze.util import Tweak
from Maze.wall import Wall


def maze(parms):
    random.seed(os.urandom(6))
    knot_work = Maze(parms[0], parms[1], 1, 0)
    Wall.straights_balance = parms[2]
    Wall.zoomorph_balance = parms[3]

    miner1 = Mazer(knot_work)
    miner1.dig(knot_work.entrance(Tweak(Tweak.master)))
    knot_work.add_bod(miner1, True)

    styles = (Tweak.master, Tweak.vanity, Tweak.horizon, Tweak.rot180, Tweak.rot090)
    style = styles[parms[4]]
    if style == Tweak.rot090 and parms[0] != parms[1]:
        style = Tweak.rot180
    if style != Tweak.master:
        miner2 = Clone(knot_work, Tweak(style), miner1)
        miner2.dig(knot_work.entrance(miner2.tweak))
        knot_work.add_bod(miner2, True)
    if style == Tweak.rot090:
        miner3 = Clone(knot_work, Tweak(Tweak.rot180), miner1)
        miner4 = Clone(knot_work, Tweak(Tweak.rot270), miner1)
        miner3.dig(knot_work.entrance(miner3.tweak))
        miner4.dig(knot_work.entrance(miner4.tweak))
        knot_work.add_bod(miner3, True)
        knot_work.add_bod(miner4, True)
    knot_work.mine()
    print(knot_work.code())


if __name__ == "__main__":
    parameters = [21, 5, 850, 300, 3, 0, 0]
    if len(sys.argv) < 3 or sys.argv[1] == "-?":
        print("You will need the font 'KNOTS Zoo' installed with ligatures set for this to show what it is doing.")
        print("This takes from two or more numeric parameters. Each one affects the knot work generated.")
        print("Parm 1: Width.  The number of characters wide. It must be more than 1.")
        print("Parm 2: Height. The number of characters high. It must be more than 1.")
        print("Parm 3: Straights Balance. This is a value between 0 and 1000. 0 = All twists, 1000=all straights. Default is 850.")
        print("Parm 4: Zoomorph Balance (Only affects twists). This is a value between 0 and 1000. 0 = All twists, 1000=all Zoomorphs. Default is 300.")
        print("Parm 5: Transform, 0: None; 1: Horizontal Mirror; 2: Vertical Mirror; 3: Rotate 180; 4: Rotate 90 (needs width and height to be the same. Default is Rotate.")
        # The below is not yet implemented.
        # print("Parm 6: Border. If this is more than 0, then the knotwork will be a border this thick. Default is none")
        # print("Parm 7: Tiling. 0: None, 1: Horizontal, 2: Vertical, 3: Both. Default is none.")
    for i in range(1, len(sys.argv)):
        parameters[i - 1] = int(sys.argv[i])
    maze(parameters)

