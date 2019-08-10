# encoding: utf-8
from enum import Enum
from collections import namedtuple


class Orientation(Enum):
    NS = True
    EW = False


Dim = namedtuple('Dim', 'x y')
