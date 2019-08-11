import unittest
from knot.works import Wall, Orientation, Cell, Dim, Com


class TestWall(unittest.TestCase):
    """
          0 1 2
    ns0   + + +
    ew0  +O+O+O+
    ns1   + + +
    ew1  +O+X+O+
    ns2   + + +
    ew2  +O+O+O+
    ns3   + + +
         0 1 2 3
    """

    def setUp(self):
        """
        It's really hard to use walls without cells.
        So here, we are initialising a group of 3x3 cells - the centre of which is Blocked.
        """
        self.cells_across = 3
        self.cells_up = 3
        self.ns_walls = [[
            Wall(Orientation.NS, i, j)
            for j in range(self.cells_up + 1)] for i in range(self.cells_across)]
        self.ew_walls = [[
            Wall(Orientation.EW, i, j)
            for j in range(self.cells_up)] for i in range(self.cells_across + 1)]
        self.cells = [[
            Cell(Dim(i, j), self.ns_walls, self.ew_walls, True if i == 1 and j == 1 else False)
            for j in range(self.cells_up)]
            for i in range(self.cells_across)]

    def test_neighbour(self):
        ewe_answers = (
              (self.cells[0][0], self.cells[1][0], self.cells[2][0], None),
              (self.cells[0][1],             None, self.cells[2][1], None),
              (self.cells[0][2], self.cells[1][2], self.cells[2][2], None)
        )
        eww_answers = (
              (None, self.cells[0][0], self.cells[1][0], self.cells[2][0]),
              (None, self.cells[0][1],             None, self.cells[2][1]),
              (None, self.cells[0][2], self.cells[1][2], self.cells[2][2])
        )
        nsn_answers = (
              (self.cells[0][0], self.cells[1][0], self.cells[2][0]),
              (self.cells[0][1],             None, self.cells[2][1]),
              (self.cells[0][2], self.cells[1][2], self.cells[2][2]),
              (None,                         None,             None)
        )
        nss_answers = (
              (None,                         None,             None),
              (self.cells[0][0], self.cells[1][0], self.cells[2][0]),
              (self.cells[0][1],             None, self.cells[2][1]),
              (self.cells[0][2], self.cells[1][2], self.cells[2][2])
        )

        for i in range(self.cells_across + 1):
            for j in range(self.cells_up):
                ew_wall = self.ew_walls[i][j]
                self.assertEqual(ew_wall.neighbour(Com.N), None, "EW Wall doesn't know North")
                self.assertEqual(ew_wall.neighbour(Com.S), None, "EW Wall doesn't know South")
                ewe_test = ew_wall.neighbour(Com.E)
                ewe_answer = ewe_answers[j][i]
                self.assertEqual(ewe_test, ewe_answer, str(Dim(i, j)) + " E: Bad Neighbour")
                eww_test = ew_wall.neighbour(Com.W)
                eww_answer = eww_answers[j][i]
                self.assertEqual(eww_test, eww_answer, str(Dim(i, j)) + " W: Bad Neighbour")
        for i in range(self.cells_across):
            for j in range(self.cells_up + 1):
                ns_wall = self.ns_walls[i][j]
                self.assertEqual(ns_wall.neighbour(Com.E), None, "NS Wall doesn't know East")
                self.assertEqual(ns_wall.neighbour(Com.W), None, "NS Wall doesn't know West")
                nsn_test = ns_wall.neighbour(Com.N)
                nsn_answer = nsn_answers[j][i]
                self.assertEqual(nsn_test, nsn_answer, str(Dim(i, j)) + " N: Bad Neighbour")
                nss_test = ns_wall.neighbour(Com.S)
                nss_answer = nss_answers[j][i]
                self.assertEqual(nss_test, nss_answer, str(Dim(i, j)) + " S: Bad Neighbour")

    def test_code(self):
        answers = {
            Orientation.EW: (
                ("O", "I", "I", "O"),
                ("O", "O", "O", "O"),
                ("O", "I", "I", "O")
            ),
            Orientation.NS: (
                ("O", "O", "O"),
                ("X", "O", "X"),
                ("X", "O", "X"),
                ("O", "O", "O")
            )
        }

        for i in range(self.cells_across + 1):
            for j in range(self.cells_up):
                ew_wall = self.ew_walls[i][j]
                self.assertEqual(ew_wall.code(Com.N), "O", "N Should be O for EW")
                self.assertEqual(ew_wall.code(Com.S), "O", "S Should be O for EW")
                self.assertEqual(ew_wall.code(Com.E), "O", "E Should be O while no doors are set")
                self.assertEqual(ew_wall.code(Com.W), "O", "W Should be O while no doors are set")
        for i in range(self.cells_across):
            for j in range(self.cells_up + 1):
                ns_wall = self.ns_walls[i][j]
                self.assertEqual(ns_wall.code(Com.E), "O", "E Should be O for NS")
                self.assertEqual(ns_wall.code(Com.W), "O", "W Should be O for NS")
                self.assertEqual(ns_wall.code(Com.N), "O", "N Should be O while no doors are set")
                self.assertEqual(ns_wall.code(Com.S), "O", "S Should be O while no doors are set")

        for i in range(self.cells_across + 1):
            for j in range(self.cells_up):
                ew_wall = self.ew_walls[i][j]
                if not ew_wall.is_edge():
                    ew_wall.make_door(Com.E, "I")
                    ew_wall.make_door(Com.W, "I")
        for i in range(self.cells_across):
            for j in range(self.cells_up + 1):
                ns_wall = self.ns_walls[i][j]
                if not ns_wall.is_edge():
                    ns_wall.make_door(Com.N, "X")
                    ns_wall.make_door(Com.S, "X")

        for i in range(self.cells_across + 1):
            for j in range(self.cells_up):
                wall = self.ew_walls[i][j]
                good = answers[Orientation.EW][j][i]
                self.assertEqual(wall.code(Com.W), good, "W" + str(i) + str(j) + " Should be " + good)
                self.assertEqual(wall.code(Com.E), good, "E" + str(i) + str(j) + " Should be " + good)
        for i in range(self.cells_across):
            for j in range(self.cells_up + 1):
                wall = self.ns_walls[i][j]
                good = answers[Orientation.NS][j][i]
                self.assertEqual(wall.code(Com.N), good, "N" + str(i) + str(j) + " Should be " + good)
                self.assertEqual(wall.code(Com.S), good, "S" + str(i) + str(j) + " Should be " + good)

        # result = ""
        # for j in reversed(range(self.cells_up)):  # reversed: print goes from top to bottom..
        #     for i in range(self.cells_across):
        #         result += self.cells[i][j].code()
        #     result = result + "\n"
        # print(result)

#      OIXOOIOIOOXI
#      XOXOooooXOXO
#      XIOOOIOIXOOI

    # def test_make_solid(self):
    #     for i in range(self.cells_across):
    #         for x in range(self.cells_up):
    #             for wall in self.ns_walls[i][j]:
    #                 wall.make_solid()
    #                 self.assertEqual(wall.door, False, "Wall is not a door")
    #
    # def test_is_wall(self):
    #     for i in range(4):
    #         for wall in self.sample[i]:
    #             wall.make_solid()
    #             self.assertEqual(wall.is_wall, True, "Wall is not a door")
    #         for wall in self.sample[i]:
    #             self.assertEqual(wall.is_wall, True, "Wall is not a door")
    #
    # def test_block(self):
    #     self.blocked = True
    #
    # def test_set_cell(self, cell, com):
    #     opp = com.opposite
    #     self.cells[com] = cell
    #     self.doors[com] = 'O'
    #     self.doors[opp] = 'O'
    #     if opp not in self.cells:
    #         self.cells[opp] = None
    #
    # def test_is_edge(self):  # If on the edge, then one of my wall cells will be None.
    #     if self.orientation == Orientation.NS:
    #         return (self.cells[Com.N] is None) or (self.cells[Com.S] is None)
    #     else:
    #         return (self.cells[Com.W] is None) or (self.cells[Com.E] is None)
    #
    # def test_can_be_dug(self, com_from):
    #     cell = self.cells[com_from]
    #     return not self.blocked and cell and not cell.mined

    # sample = (Com.N, Com.E, Com.S, Com.W, Com.C, Com.F, Com.X)
    #
    # def test_str(self):
    #     self.assertEqual(str(Com.N), "North", "Should be North")


if __name__ == '__main__':
    unittest.main()
