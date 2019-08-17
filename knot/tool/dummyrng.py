
class DummyRng:

    def __init__(self, seed: int = 0):
        self.i_counter = seed
        self.c_counter = seed

    def seed(self, seed: int = 0):
        self.i_counter = seed
        self.c_counter = seed

    def random(self) -> float:
        values = (0.0, 0.25, 0.5, 0.75, 0.999)
        value = values[self.i_counter % 5]
        self.i_counter += 1
        return value

    def choice(self, args):
        index = self.c_counter % len(args)
        self.c_counter += 1
        return args[index]
