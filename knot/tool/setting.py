# encoding: utf-8
import random
from .cut import Cut


# zoomorph_balance;  0 = All twists, 1000=all Zoomorphs.
# straights_balance; 0 = All twists, 1000=all Straights
# So a setting of(0,1000) is all zoo.
class Setting:
    def __init__(self, straights_balance=0.2, zoo_balance=0.2, rng=random):
        self.straights_balance = straights_balance
        self.zoomorph_balance = zoo_balance
        self.rng = rng
        self.hb_choice = (Cut.H, Cut.B)

    def choose(self) -> Cut:
        # straights_balance; 0 = All twists, 1.000=all straights
        kind = Cut.I
        straights = self.rng.random()
        if self.straights_balance < straights:
            # need to do something if not straights..
            # zoomorph_balance; 0 = All twists, 1.000=all Zoomorphs.
            kind = Cut.X
            zoos = self.rng.random()
            if self.zoomorph_balance > zoos:
                # logic vs straights is switched because here we need to do something if zoo.
                kind = self.rng.choice(self.hb_choice)
        return kind
