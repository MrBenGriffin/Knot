import os
import sys
import random
from Maze.maze import Maze
from Bod.mazer import Mazer
from Bod.clone import Clone
from Maze.tweak import Tweak
from Maze.wall import Wall


def maze(parms):
    random.seed(os.urandom(6))
    knot_work = Maze(parms[0], parms[1], parms[6])
    Wall.straights_balance = parms[2]
    Wall.zoomorph_balance = parms[3]
    Mazer.cutoff = max(2, parms[5])
    styles = (Tweak.master, Tweak.vanity, Tweak.horizon, Tweak.rot180, Tweak.rot090)
    style = styles[parms[4]]
    miner1 = Mazer(knot_work, Tweak.master)
    miner1.enter(knot_work.entrance(Tweak(Tweak.master)))
    knot_work.add_bod(miner1)

    if style == Tweak.rot090 and parms[0] != parms[1]:
        style = Tweak.rot180
    if style != Tweak.master:
        miner2 = Clone(knot_work, Tweak(style), miner1)
        miner2.enter(knot_work.entrance(miner2.tweak))
        knot_work.add_bod(miner2)
    if style == Tweak.rot090:
        miner3 = Clone(knot_work, Tweak(Tweak.rot180), miner1)
        miner4 = Clone(knot_work, Tweak(Tweak.rot270), miner1)
        miner3.enter(knot_work.entrance(miner3.tweak))
        miner4.enter(knot_work.entrance(miner4.tweak))
        knot_work.add_bod(miner3)
        knot_work.add_bod(miner4)
    knot_work.mine()
    print(knot_work.code())


if __name__ == "__main__":
    parameters = [9, 9, 850, 300, 4, 10, 0, 0, 0]
    if len(sys.argv) < 3 or sys.argv[1] == "-?":
        print("You will need the font 'KNOTS Zoo' installed with ligatures set for this to show what it is doing.")
        print("This takes from two or more numeric parameters. Each one affects the knot work generated.")
        print("Parm 1: Width.  The number of characters wide. It must be more than 1. Default 9")
        print("Parm 2: Height. The number of characters high. It must be more than 1. Default 9")
        print("Parm 3: Straights Balance. This is a value between 0 and 1000. 0 = All twists, 1000=all straights. Default is 850.")
        print("Parm 4: Zoomorph Balance (Only affects twists). This is a value between 0 and 1000. 0 = All twists, 1000=all Zoomorphs. Default is 300.")
        print("Parm 5: Transform, 0: None; 1: Horizontal Mirror; 2: Vertical Mirror; 3: Rotate 180; 4: Rotate 90 (needs width and height to be the same. Default is Rotate.")
        print("Parm 6: Connectivity. Slightly adjusts connections, smaller makes more. Minimum is 2. Default is 10")
        print("Parm 7: Border. If this is more than 0, then the knotwork will be a border this thick. Default is none")
        print("")
        # print("Parm 8: Tiling. 0: None, 1: Horizontal, 2: Vertical, 3: Both. Default is none.")
    for i in range(1, len(sys.argv)):
        parameters[i - 1] = int(sys.argv[i])
    maze(parameters)

