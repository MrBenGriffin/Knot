# encoding: utf-8
import os
import random
import argparse
from knot.space.crs import Symmetry
from knot.space.shape import Shape
from knot.works import Structure
from knot.actor import Mazer, Clone, Joiner, Holer, Spiral
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
        return self.start <= key <= self.stop

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
    shape = None

    if not args['hex']:
        if args['width'] == args['height']:
            shape = Shape.squared
        else:
            shape = Shape.rectangle

    style = shape.wallpaper.select(args['symmetry'])
    if not style or not shape:
        print("Style / symmetry is currently not available")
        exit(0)
    knot_work = Structure(args['width'], args['height'], args['border'], shape,  args['htile'], args['vtile'])
    setting = Setting(args['straights'], args['zoo'])
    Mazer.cutoff = int(20.0 * args['connectivity'])
    Holer.balance = args['connectivity']
    master = args['worker'](knot_work, setting)
    knot_work.add_bod(master)
    for w in range(1, style.workers):
        miner = Clone(knot_work, master, style, w)
        knot_work.add_bod(miner)
    knot_work.mine()

    # TODO:: Uncomment this when ready..
    # if len(knot_work.bods) > 1 and args['worker'] is Mazer and (knot_work.border or knot_work.cells_up % 2 is 0 or knot_work.cells_across % 2 is 0):
    #     joiner = Joiner(knot_work, setting)
    #     knot_work.bods[0] = joiner
    #     for bod in range(1, len(knot_work.bods)):
    #         knot_work.bods[bod].set_other(joiner)
    #     knot_work.join()
    result = knot_work.code() if args['encoding'] == 'HIBOX' else knot_work.unicode()
    print(result)


def do_args():
    # There is no need for an upper limit - but the choices here are breaking using range(1, 10**100000)
    bounds = ArgRange(2)
    balance = ArgRange(0.0, 1.0)
    workers = {'M': Mazer, 'S': Spiral, 'F': Holer}
    parser = argparse.ArgumentParser(description="Calculate and print out knot-work. You will need the font 'KNOTS Zoo' installed with ligatures set for this to show what it is doing.")
    parser.add_argument("-x", "--width",  type=int, choices=bounds,  default=9, help="Width.  The number of cells wide. (default: %(default)s)")
    parser.add_argument("-y", "--height", type=int, choices=bounds, default=0, help="Height. The number of cells high. (default: same as -x")
    parser.add_argument("-sb", "--straights", type=float, default=0.2, choices=balance, help="Balance between Twists and Straights. 0.0 = twists, 1.00 = straights. (default: %(default)s)")
    parser.add_argument("-zb", "--zoo", type=float, default=0.2, choices=balance, help="Balance between Twists and Zoomorphs. 0.0 = twists, 1.00 = zoomorphs. (default: %(default)s)")
    parser.add_argument("-s", "--symmetry", type=str, default='R', choices=Symmetry.choices(), help="N: None; H: Horizontal Mirror; V: Vertical Mirror; F: Flip (rotate 180); R: Rotate 90 (when width and height are the same). (default: %(default)s)")
    parser.add_argument("-b", "--border", type=int, help="If this is set, then the knot-work will be a border this thick. (default: %(default)s)")
    parser.add_argument("-w", "--worker", type=str, default='M', choices=['M', 'S', 'F'], help="Miner builds corridors, Spiral makes spirals, Filler is a full network (default: %(default)s)")
    parser.add_argument("-6", "--hex", action="store_true", help="The knot-work will use hexagonal hex-map. (default: square tiling)")
    parser.add_argument("-ht", "--htile", action="store_true", help="The knot-work will tile horizontally. (default: %(default)s)")
    parser.add_argument("-vt", "--vtile", action="store_true", help="The knot-work will tile vertically. (default: %(default)s)")
    parser.add_argument("-cb", "--connectivity", type=float, default=0.2, choices=balance, help="Balance of connections. Larger numbers make longer threads. (default: %(default)s)")
    parser.add_argument("-r", "--random", type=int, default=os.urandom(7), help="Random seed. If this is non-zero you should always get the same knot for the parameters. (default: os.urandom)")
    parser.add_argument("-e", "--encoding", type=str, choices=['HIBOX', 'E000'], default='HIBOX', help="Output encoding - either HIBOX ligatures or Unicode PUA 0xE000")
    args = parser.parse_args()
    arg_dict = vars(args)

    arg_dict['height'] = arg_dict['width'] if arg_dict['height'] == 0 else arg_dict['height']
    arg_dict['worker'] = workers[arg_dict['worker']]
    make_knot(arg_dict)


if __name__ == "__main__":
    do_args()

