import os
import random
import sys
from knot.space import Tw
from knot.works import Structure, Wall
from knot.actor import Mazer, Clone, Joiner
from knot.tool import Setting


def maze(parms):
    random.seed(os.urandom(6))
    knot_work = Structure(parms[0], parms[1], parms[6])
    setting = Setting(parms[2], parms[3])
    Mazer.cutoff = max(2, parms[5])
    styles = (Tw.master, Tw.vanity, Tw.horizon, Tw.rot180, Tw.rot090)
    style = styles[parms[4]]
    miner1 = Mazer(knot_work, setting)
    knot_work.add_bod(miner1)

    if style == Tw.rot090 and parms[0] != parms[1]:
        style = Tw.rot180
    if style != Tw.master:
        miner2 = Clone(knot_work, style, miner1)
        knot_work.add_bod(miner2)
    if style == Tw.rot090:
        miner3 = Clone(knot_work, Tw.rot180, miner1)
        miner4 = Clone(knot_work, Tw.rot270, miner1)
        knot_work.add_bod(miner3)
        knot_work.add_bod(miner4)
    knot_work.mine()
    # The clones won't touch anyone else if,
    # if there is more than one miner AND
    # if (1) there's a border OR
    #    (2) if the edges are even
    # Then we will need a joiner (and clones).
    if len(knot_work.bods) > 1 and (knot_work.border > 0 or knot_work.cells_up % 2 is 0 or knot_work.cells_across % 2 is 0):
        joiner = Joiner(knot_work, setting)
        knot_work.bods[0] = joiner
        for bod in range(1, len(knot_work.bods)):
            knot_work.bods[bod].set_other(joiner)
        knot_work.join()

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

