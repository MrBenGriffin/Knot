import os
import random
import sys
from knot.space import Tw
from knot.works import Structure
from knot.actor import Mazer, Clone, Joiner, Holer
from knot.tool import Setting


def maze(parms):
    if parms[9] is 0:
        random.seed(os.urandom(7))
    else:
        random.seed(parms[9])

#    0:9, 1:9, 2:200, 3:200, 4:4, 5:0, 6:0, 7:0, 8:12, 9:0

#   0 cells_across, 1 cells_up,5 border,6 h_wrap,7 v_wrap
    knot_work = Structure(parms[0], parms[1], parms[5], parms[6], parms[7])
    setting = Setting(parms[2], parms[3])
    Mazer.cutoff = max(2, parms[8])
    styles = (Tw.master, Tw.vanity, Tw.sunset, Tw.rot180, Tw.rot090)
    style = styles[parms[4]]
    # miner1 = Holer(knot_work, setting)
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
    # if len(knot_work.bods) > 1 and (knot_work.border > 0 or knot_work.cells_up % 2 is 0 or knot_work.cells_across % 2 is 0):
    #     joiner = Joiner(knot_work, setting)
    #     knot_work.bods[0] = joiner
    #     for bod in range(1, len(knot_work.bods)):
    #         knot_work.bods[bod].set_other(joiner)
    #     knot_work.join()

    print(knot_work.code())


if __name__ == "__main__":
    parameters = [9, 9, 200, 200, 4, 0, 0, 0, 12, 0]
    if len(sys.argv) < 3 or sys.argv[1] == "-?":
        print("You will need the font 'KNOTS Zoo' installed with ligatures set for this to show what it is doing.")
        print("This takes from two or more numeric parameters. Each one affects the knot work generated.")
        print("Parm 1: Width.  The number of characters wide. It must be more than 1. Default 9")
        print("Parm 2: Height. The number of characters high. It must be more than 1. Default 9")
        print("Parm 3: Straights Balance. This is a value between 0 and 1000. 0 = All twists, 1000=all straights. Default is 200.")
        print("Parm 4: Zoomorph Balance (Only affects twists). This is a value between 0 and 1000. 0 = All twists, 1000=all Zoomorphs. Default is 200.")
        print("Parm 5: Transform, 0: None; 1: Horizontal Mirror; 2: Vertical Mirror; 3: Rotate 180; 4: Rotate 90 (needs width and height to be the same. Default is 4.")
        print("Parm 6: Border. If this is more than 0, then the knotwork will be a border this thick. Default is 0")
        print("Parm 7: H Wrap. If this is set to 1 then the knotwork will tile horizontally. Default 0")
        print("Parm 8: V Wrap. If this is set to 1 then the knotwork will tile vertically. Default 0")
        print("Parm 9: Connectivity. Slightly adjusts connections, smaller makes more. Minimum is 2. Default is 12")
        print("Parm 10: Seed. If this is set you should always get the same knot for the parameters. Default 0")
        print("")
        # print("Parm 8: Tiling. 0: None, 1: Horizontal, 2: Vertical, 3: Both. Default is none.")
    for i in range(1, min(len(parameters), len(sys.argv))):
        parameters[i - 1] = int(sys.argv[i])
    maze(parameters)

