# encoding: utf-8
import os
import random
import argparse
from knot.space.crs import Symmetry
from knot.space.rectilinear import Square, Rectangle
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
    random.seed(args['random'])
    shape = None

    if not args['hex']:
        if len(args['dimensions']) == 1 or args['dimensions'][0] == args['dimensions'][1]:
            shape = Square()
        else:
            shape = Rectangle()

    style = shape.paper().select(args['symmetry'])
    if not style or not shape:
        print("Style / symmetry is currently not available")
        exit(0)
    knot_work = Structure(shape, args['dimensions'], args['border'], args['tiling'])
    setting = Setting(args['straights'], args['zoo'])
    Mazer.cutoff = int(20.0 * args['connectivity'])
    Holer.balance = args['connectivity']
    master = args['worker'](knot_work.lattice, setting)
    knot_work.add_bod(master)
    for w in range(1, style.workers):
        clone = Clone(knot_work.lattice, master, style, w)
        knot_work.add_bod(clone)
    knot_work.mine()
    if len(knot_work.bods) > 1:
        knot_work.bods.clear()
        joiner = Joiner(knot_work.lattice, master)
        knot_work.add_bod(joiner)
        for w in range(1, style.workers):
            clone = Clone(knot_work.lattice, joiner, style, w)
            knot_work.add_bod(clone)
        knot_work.join()
    result = knot_work.code() if args['encoding'] == 'HIBOX' else knot_work.unicode()
    print(result)


def do_args():
    # There is no need for an upper limit - but the choices here are breaking using range(1, 10**100000)
    bounds = ArgRange(2)
    balance = ArgRange(0.0, 1.0)
    workers = {'M': Mazer, 'S': Spiral, 'F': Holer}
    parser = argparse.ArgumentParser(description="Calculate and print out knot-work. You will need the font 'KNOTS Zoo' installed with ligatures set for this to show what it is doing.")
    parser.add_argument("-d", "--dimensions", nargs='+', type=int, default=[9, 9], help="Dimensions. Size of each axis (eg, x, y). (default: %(default)s)")
    parser.add_argument("-t", "--tiling", nargs='+', type=bool, default=[False, False], help="Tiling (wrapping) options along each axis (eg, x, y)")
    parser.add_argument("-s", "--symmetry", type=str, default='R', choices=Symmetry.choices(), help="N: None; H: Horizontal Mirror; V: Vertical Mirror; F: Flip (rotate 180); R: Rotate 90 (when width and height are the same). (default: %(default)s)")
    parser.add_argument("-b", "--border", type=int, help="If this is set, then the knot-work will be a border this thick. (default: %(default)s)")
    parser.add_argument("-w", "--worker", type=str, default='M', choices=['M', 'S', 'F'], help="Miner builds corridors, Spiral makes spirals, Filler is a full network (default: %(default)s)")
    parser.add_argument("-sb", "--straights", type=float, default=0.2, choices=balance, help="Balance between Twists and Straights. 0.0 = twists, 1.00 = straights. (default: %(default)s)")
    parser.add_argument("-zb", "--zoo", type=float, default=0.2, choices=balance, help="Balance between Twists and Zoomorphs. 0.0 = twists, 1.00 = zoomorphs. (default: %(default)s)")
    parser.add_argument("-x", "--hex", action="store_true", help="The knot-work will use hexagonal hex-map. (default: square tiling)")
    parser.add_argument("-cb", "--connectivity", type=float, default=0.2, choices=balance, help="Balance of connections. Larger numbers make longer threads. (default: %(default)s)")
    parser.add_argument("-r", "--random", type=int, default=os.urandom(7), help="Random seed. If this is non-zero you should always get the same knot for the parameters. (default: os.urandom)")
    parser.add_argument("-e", "--encoding", type=str, choices=['HIBOX', 'E000'], default='HIBOX', help="Output encoding - either HIBOX ligatures or Unicode PUA 0xE000")
    args = parser.parse_args()
    arg_dict = vars(args)

    arg_dict['worker'] = workers[arg_dict['worker']]
    arg_dict['dimensions'] = tuple(args.dimensions)
    arg_dict['tiling'] = tuple(args.tiling)
    make_knot(arg_dict)


if __name__ == "__main__":
    do_args()

