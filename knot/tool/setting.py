# encoding: utf-8
import random
from .cut import Cut


class Setting:
    def __init__(self, straights_balance=333, zoo_balance=200):
        self.straights_balance = straights_balance
        self.zoomorph_balance = zoo_balance

    def choose(self) -> Cut:
        # straights_balance; 0 = All twists, 1000=all straights
        kind = Cut.I
        straights = random.randint(0, 1000)
        if straights < self.straights_balance:
            # zoomorph_balance; 0 = All twists, 1000=all Zoomorphs.
            kind = Cut.X
            zoos = random.randint(0, 1000)
            if zoos < self.zoomorph_balance:
                kind = random.choice((Cut.H, Cut.B))
        return kind
