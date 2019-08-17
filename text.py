# encoding: utf-8
import os
import random
import argparse
from knot.space import Tw
from knot.works import Structure
from knot.actor import Mazer, Clone, Joiner, Holer
from knot.tool import Setting


# This is used for argument passing
class ArgRange(object):
    from decimal import Decimal
    huge = Decimal('+infinity')
    huge_str = '{:.4E}'.format(huge)

    def __init__(self, start, stop=huge, n=3):
        self.start = start
        self.stop = stop
        self.n = n

    def __contains__(self, key):
        return self.start <= key < self.stop

    def __iter__(self):
        if self.stop < self.start + (self.n * 3):
            if isinstance(self.stop, int):
                for i in range(self.start, self.stop):
                    yield i
            else:
                yield self.start
        else:
            if isinstance(self.stop, int):
                for i in range(self.start, self.start + self.n):
                    yield i
            if self.stop is self.huge:
                yield '...' + self.huge_str
            else:
                yield '...'
                if isinstance(self.stop, int):
                    for i in range(self.stop - self.n, self.stop):
                        yield i
                else:
                    yield self.stop


def make_knot(args: dict):
    # print(args)
    random.seed(args['random'])

    knot_work = Structure(args['width'], args['height'], args['border'], args['htile'], args['vtile'])
    setting = Setting(args['straights'], args['zoo'])
    Mazer.cutoff = args['connectivity']
    style = args['symmetry']
    miner1 = Mazer(knot_work, setting)
    knot_work.add_bod(miner1)

    if style == Tw.rot090 and args['width'] != args['height']:
        print("Rotational symmetry requires width and height to be the same. Downgrading to flip symmetry")
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


def do_args():
    # There is no need for an upper limit - but the choices here are breaking using range(1, 10**100000)
    bounds = ArgRange(2)
    balance = ArgRange(0.0, 1.0, 3.0)
    styles = {'N': Tw.master, 'V': Tw.vanity, 'H': Tw.sunset, 'F': Tw.rot180, 'R': Tw.rot090}
    parser = argparse.ArgumentParser(description="Calculate and print out knot-work. You will need the font 'KNOTS Zoo' installed with ligatures set for this to show what it is doing.")
    parser.add_argument("-x", "--width",  type=int, choices=bounds,  default=9, help="Width.  The number of cells wide. (default: %(default)s)")
    parser.add_argument("-y", "--height", type=int, choices=bounds, default=9, help="Height. The number of cells high. (default: %(default)s)")
    parser.add_argument("-sb", "--straights", type=float, default=0.2, choices=balance, help="Balance between Twists and Straights. 0.0 = twists, 1.00 = straights. (default: %(default)s)")
    parser.add_argument("-zb", "--zoo", type=float, default=0.2, choices=balance, help="Balance between Twists and Zoomorphs. 0.0 = twists, 1.00 = zoomorphs. (default: %(default)s)")
    parser.add_argument("-s", "--symmetry", type=str, default='R', choices=['N', 'H', 'V', 'F', 'R'], help="N: None; H: Horizontal Mirror; V: Vertical Mirror; F: Flip (rotate 180); R: Rotate 90 (when width and height are the same). (default: %(default)s)")
    parser.add_argument("-b", "--border", type=int, help="If this is set, then the knot-work will be a border this thick. (default: %(default)s)")
    parser.add_argument("-ht", "--htile", action="store_true", help="The knot-work will tile horizontally. (default: %(default)s)")
    parser.add_argument("-vt", "--vtile", action="store_true", help="The knot-work will tile vertically. (default: %(default)s)")
    parser.add_argument("-c", "--connectivity", type=int, default=12, choices=bounds, help="Slightly adjusts connections. Larger numbers make longer threads. (default: %(default)s)")
    parser.add_argument("-r", "--random", type=int, default=os.urandom(7), help="Random seed. If this is non-zero you should always get the same knot for the parameters. (default: %(default)s)")
    args = parser.parse_args()
    arg_dict = vars(args)
    arg_dict['symmetry'] = styles[arg_dict['symmetry']]
    make_knot(arg_dict)


if __name__ == "__main__":
    do_args()

