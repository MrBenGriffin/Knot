# encoding: utf-8
from knot.space import Com
from knot.tool import Cut


class Cell:
    last = None
    last_mined = None

    def __init__(self, dim, wns, wew, blocked=False):
        self.miner = None
        self.dim = dim
        self.mined = False
        self.walls = {Com.N: wns[dim.x][dim.y + 1],
                      Com.E: wew[dim.x + 1][dim.y],
                      Com.S: wns[dim.x][dim.y],
                      Com.W: wew[dim.x][dim.y]
                      }
        if blocked:
            self.walls[Com.N].block()
            self.walls[Com.E].block()
            self.walls[Com.S].block()
            self.walls[Com.W].block()
        else:
            self.walls[Com.N].set_cell(self, Com.S)
            self.walls[Com.E].set_cell(self, Com.W)
            self.walls[Com.S].set_cell(self, Com.N)
            self.walls[Com.W].set_cell(self, Com.E)

    def log(self, orig):
        print(str(" " + self.name() + ":" + orig + "->" + self.code()))

    def name(self):
        return str(self.dim)

    def move(self, com):
        if com in self.walls and self.walls[com]:
            wall = self.walls[com]
            if not wall.is_wall():
                return wall.cells[com]
        return self

    def exits(self):
        list_of_exits = self.level_exits()
        return list_of_exits

    def level_exits(self):
        list_of_exits = []
        for compass, wall in self.walls.items():
            if not wall.is_wall():
                list_of_exits.append(compass)
        return list_of_exits

    def count_level_exits(self):
        count = 0
        for wall in list(self.walls.values()):
            if not wall.is_wall():
                count += 1
        return count

    def level_walls_to_be_dug(self, walls):
        for compass, wall in self.walls.items():
            if wall.can_be_dug(compass):
                walls.append(compass)
        return walls

    def neighbours(self):
        """
        :return: dict [Com: Neighbour] of neighbours
        """
        neighbours = {}
        for compass, wall in self.walls.items():
            neighbour = wall.neighbour(compass)
            if neighbour:
                neighbours[compass] = neighbour
        return neighbours

    def walls_that_can_be_dug(self):
        """
        :return: list [Com] that may be dug..
        """
        return self.level_walls_to_be_dug([])

    def is_a_passage(self):
        exits = self.walls_that_can_be_dug()
        if not exits:
            exits = self.level_exits()
            return len(exits) == 2 and exits[0] == exits[1].opposite
        return False

    # make_door_in is done on self's side.
    # def make_door(self, cell_dir: Com, tool: Cutter, ):
    def make_door_in(self, com, miner, cut: Cut = None):
        cell = self.walls[com].make_door(com, miner.tool, cut)
        if cell:
            if not cell.miner:
                cell.mined = True
                cell.miner = miner
            Cell.last_mined = cell
        return cell

    def __str__(self):
        return self.code()

    def __repr__(self):
        return "Cell (" + str(self.dim) + " " + self.code() + ")"

    def code(self):
        if not self.mined:
            return "oooo"
        return self.walls[Com.N].code(Com.N) + \
               self.walls[Com.E].code(Com.E) + \
               self.walls[Com.S].code(Com.S) + \
               self.walls[Com.W].code(Com.W)

    def __cmp__(self, other):
        return self.dim == other.dim
