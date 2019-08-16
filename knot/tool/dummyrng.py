
class DummyRng:

    def __init__(self, seed: int = 0):
        self.i_counter = seed
        self.c_counter = seed

    def seed(self, seed: int = 0):
        self.i_counter = seed
        self.c_counter = seed

    def randint(self, x: int = 0, y: int = 1000) -> int:
        values = (0.0, 0.25, 0.5, 0.75, 1.0)
        value = int(x + values[self.i_counter % 5] * (y-x))
        self.i_counter += 1
        return value

    def choice(self, args):
        index = self.c_counter % len(args)
        self.c_counter += 1
        return args[index]
