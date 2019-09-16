import unittest
from knot.space import Shape
from knot.tool import Cut, Cutter


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
        self.shape = Shape.squared
        self.com = self.shape.com
        self.lattice = self.shape.lattice((3, 3), (False, False))
        self.lattice.border(1)
        self.cutter = Cutter(self.shape.wallpaper.identity())

    def makeDoor(self, dim: tuple, com: tuple, cut: Cut):
        wall = self.lattice.wall(dim, com)
        if wall:
            wall.make_door(com, self.cutter, cut)

    def cutAll(self, size: tuple):
        for i in range(size[0]):
            for j in range(size[1]):
                for c in self.com:
                    self.makeDoor((i, j), c, Cut.I)

    def cutOut(self, size: tuple):
        for i in range(size[0]):
            for j in range(size[1]):
                self.makeDoor((i, j), self.com.W, Cut.I)
                self.makeDoor((i, j), self.com.E, Cut.I)
                self.makeDoor((i, j), self.com.N, Cut.X)
                self.makeDoor((i, j), self.com.S, Cut.X)

    def test_neighbour(self):
        pass
        # ewe_answers = (
        #       (self.cells[0][0], self.cells[1][0], self.cells[2][0], None),
        #       (self.cells[0][1],             None, self.cells[2][1], None),
        #       (self.cells[0][2], self.cells[1][2], self.cells[2][2], None)
        # )
        # eww_answers = (
        #       (None, self.cells[0][0], self.cells[1][0], self.cells[2][0]),
        #       (None, self.cells[0][1],             None, self.cells[2][1]),
        #       (None, self.cells[0][2], self.cells[1][2], self.cells[2][2])
        # )
        # nsn_answers = (
        #       (self.cells[0][0], self.cells[1][0], self.cells[2][0]),
        #       (self.cells[0][1],             None, self.cells[2][1]),
        #       (self.cells[0][2], self.cells[1][2], self.cells[2][2]),
        #       (None,                         None,             None)
        # )
        # nss_answers = (
        #       (None,                         None,             None),
        #       (self.cells[0][0], self.cells[1][0], self.cells[2][0]),
        #       (self.cells[0][1],             None, self.cells[2][1]),
        #       (self.cells[0][2], self.cells[1][2], self.cells[2][2])
        # )

        # for i in range(self.cells_across + 1):
        #     for j in range(self.cells_up):
        #         ew_wall = self.ew_walls[i][j]
        #         self.assertEqual(ew_wall.cell(Com.N), None, "EW Wall doesn't know North")
        #         self.assertEqual(ew_wall.cell(Com.S), None, "EW Wall doesn't know South")
        #         ewe_test = ew_wall.cell(Com.E)
        #         ewe_answer = ewe_answers[j][i]
        #         self.assertEqual(ewe_test, ewe_answer, str(Dim(i, j)) + " E: Bad Neighbour")
        #         eww_test = ew_wall.cell(Com.W)
        #         eww_answer = eww_answers[j][i]
        #         self.assertEqual(eww_test, eww_answer, str(Dim(i, j)) + " W: Bad Neighbour")
        # for i in range(self.cells_across):
        #     for j in range(self.cells_up + 1):
        #         ns_wall = self.ns_walls[i][j]
        #         self.assertEqual(ns_wall.cell(Com.E), None, "NS Wall doesn't know East")
        #         self.assertEqual(ns_wall.cell(Com.W), None, "NS Wall doesn't know West")
        #         nsn_test = ns_wall.cell(Com.N)
        #         nsn_answer = nsn_answers[j][i]
        #         self.assertEqual(nsn_test, nsn_answer, str(Dim(i, j)) + " N: Bad Neighbour")
        #         nss_test = ns_wall.cell(Com.S)
        #         nss_answer = nss_answers[j][i]
        #         self.assertEqual(nss_test, nss_answer, str(Dim(i, j)) + " S: Bad Neighbour")

    def test_can_be_dug(self):
        pass
        # answers = {
        #     Com.W: (
        #         (False, True,  True,  True),
        #         (False, False, False, True),
        #         (False, True,  True,  True)
        #     ),
        #     Com.E: (
        #         (True, True,  True,  False),
        #         (True, False, False, False),
        #         (True, True,  True,  False)
        #     ),
        #     Com.N: (
        #         (True,  True,  True),
        #         (True,  False, True),
        #         (True,  False, True),
        #         (False, False, False)
        #     ),
        #     Com.S: (
        #         (False, False, False),
        #         (True,  False, True),
        #         (True,  False, True),
        #         (True,  True,  True)
        #     )
        # }
        # for i in range(self.cells_across + 1):
        #     for j in range(self.cells_up):
        #         wall = self.ew_walls[i][j]
        #         w_ok = answers[Com.W][j][i]
        #         e_ok = answers[Com.E][j][i]
        #         w_ts = wall.can_be_dug(Com.W)
        #         e_ts = wall.can_be_dug(Com.E)
        #         n_ts = wall.can_be_dug(Com.N)
        #         s_ts = wall.can_be_dug(Com.S)
        #
        #         self.assertEqual(w_ts, w_ok, "W" + str(i) + str(j) + " Should be " + str(w_ok))
        #         self.assertEqual(e_ts, e_ok, "E" + str(i) + str(j) + " Should be " + str(e_ok))
        #         self.assertEqual(n_ts, False, "N" + str(i) + str(j) + " Should not work on WE")
        #         self.assertEqual(s_ts, False, "S" + str(i) + str(j) + " Should not work on WE")
        # for i in range(self.cells_across):
        #     for j in range(self.cells_up + 1):
        #         wall = self.ns_walls[i][j]
        #         n_ok = answers[Com.N][j][i]
        #         s_ok = answers[Com.S][j][i]
        #         self.assertEqual(wall.can_be_dug(Com.N), n_ok, "N" + str(i) + str(j) + " Should be " + str(n_ok))
        #         self.assertEqual(wall.can_be_dug(Com.S), s_ok, "S" + str(i) + str(j) + " Should be " + str(s_ok))
        #         self.assertEqual(wall.can_be_dug(Com.W), False, "W" + str(i) + str(j) + " Should not work on NS")
        #         self.assertEqual(wall.can_be_dug(Com.E), False, "E" + str(i) + str(j) + " Should not work on NS")

    def test_is_edge(self):
        pass
        # answers = {
        #     Axis.EW: (
        #         (True, False, False, True),
        #         (True,  True, True,  True),
        #         (True, False, False, True)
        #     ),
        #     Axis.NS: (
        #         (True,  True, True),
        #         (False, True, False),
        #         (False, True, False),
        #         (True,  True, True)
        #     )
        # }
        # for i in range(self.cells_across + 1):
        #     for j in range(self.cells_up):
        #         wall = self.ew_walls[i][j]
        #         good = answers[Axis.EW][j][i]
        #         self.assertEqual(wall.is_edge(), good, "EW" + str(i) + str(j) + " Should be " + str(good))
        # for i in range(self.cells_across):
        #     for j in range(self.cells_up + 1):
        #         wall = self.ns_walls[i][j]
        #         good = answers[Axis.NS][j][i]
        #         self.assertEqual(wall.is_edge(), good, "ES" + str(i) + str(j) + " Should be " + str(good))

    def test_code(self):
        pass
        # answers = {
        #     Axis.EW: (
        #         ("O", "I", "I", "O"),
        #         ("O", "O", "O", "O"),
        #         ("O", "I", "I", "O")
        #     ),
        #     Axis.NS: (
        #         ("O", "O", "O"),
        #         ("X", "O", "X"),
        #         ("X", "O", "X"),
        #         ("O", "O", "O")
        #     )
        # }
        # for i in range(self.cells_across + 1):
        #     for j in range(self.cells_up):
        #         ew_wall = self.ew_walls[i][j]
        #         self.assertEqual(ew_wall.code(Com.N), "O", "N Should be O for EW")
        #         self.assertEqual(ew_wall.code(Com.S), "O", "S Should be O for EW")
        #         self.assertEqual(ew_wall.code(Com.E), "O", "E Should be O while no doors are set")
        #         self.assertEqual(ew_wall.code(Com.W), "O", "W Should be O while no doors are set")
        # for i in range(self.cells_across):
        #     for j in range(self.cells_up + 1):
        #         ns_wall = self.ns_walls[i][j]
        #         self.assertEqual(ns_wall.code(Com.E), "O", "E Should be O for NS")
        #         self.assertEqual(ns_wall.code(Com.W), "O", "W Should be O for NS")
        #         self.assertEqual(ns_wall.code(Com.N), "O", "N Should be O while no doors are set")
        #         self.assertEqual(ns_wall.code(Com.S), "O", "S Should be O while no doors are set")
        # self.cutOut()
        # for i in range(self.cells_across + 1):
        #     for j in range(self.cells_up):
        #         wall = self.ew_walls[i][j]
        #         good = answers[Axis.EW][j][i]
        #         self.assertEqual(wall.code(Com.W), good, "W" + str(i) + str(j) + " Should be " + good)
        #         self.assertEqual(wall.code(Com.E), good, "E" + str(i) + str(j) + " Should be " + good)
        # for i in range(self.cells_across):
        #     for j in range(self.cells_up + 1):
        #         wall = self.ns_walls[i][j]
        #         good = answers[Axis.NS][j][i]
        #         self.assertEqual(wall.code(Com.N), good, "N" + str(i) + str(j) + " Should be " + good)
        #         self.assertEqual(wall.code(Com.S), good, "S" + str(i) + str(j) + " Should be " + good)

    # def test_is_wall(self):
    #     pass
        # answers = {
        #     Axis.EW: (
        #         (True, False, False, True),
        #         (True, True,  True,  True),
        #         (True, False, False, True)
        #     ),
        #     Axis.NS: (
        #         (True,  True,  True),
        #         (False, True, False),
        #         (False, True, False),
        #         (True,  True,  True)
        #     )
        # }
        # for i in range(self.cells_across + 1):
        #     for j in range(self.cells_up):
        #         wall = self.ew_walls[i][j]
        #         good = True
        #         self.assertEqual(wall.is_wall(), good, str(i) + str(j) + " EW Should be " + str(good))
        # for i in range(self.cells_across):
        #     for j in range(self.cells_up + 1):
        #         wall = self.ns_walls[i][j]
        #         good = True
        #         self.assertEqual(wall.is_wall(), good, str(i) + str(j) + " NS Should be " + str(good))
        # self.cutOut()
        # for i in range(self.cells_across + 1):
        #     for j in range(self.cells_up):
        #         wall = self.ew_walls[i][j]
        #         good = answers[Axis.EW][j][i]
        #         self.assertEqual(wall.is_wall(), good, str(i) + str(j) + " EW Should be " + str(good))
        # for i in range(self.cells_across):
        #     for j in range(self.cells_up + 1):
        #         wall = self.ns_walls[i][j]
        #         good = answers[Axis.NS][j][i]
        #         self.assertEqual(wall.is_wall(), good, str(i) + str(j) + " NS Should be " + str(good))

    def make_solid(self, dim: tuple, com: tuple):
        wall = self.lattice.wall(dim, com)
        if wall:
            wall.make_solid()

    def is_solid(self, dim: tuple, com: tuple) -> bool:
        wall = self.lattice.wall(dim, com)
        if wall:
            return wall.is_wall()
        return True

    def test_is_wall(self):
        size = (3, 3)
        self.cutAll(size)
        foo = self.lattice.unicode()
        answers = {
            self.com.N: ((False, True, False), (False, True, False), (True, True, True)),
            self.com.E: ((False, False, True), (True, True, True), (False, False, True)),
            self.com.S: ((True, True, True), (False, True, False), (False, True, False)),
            self.com.W: ((True, False, False), (True, True, True), (True, False, False)),
        }
        for com in self.com:
            c_answer = answers[com]
            for j in range(size[1]):
                j_answer = c_answer[j]
                for i in range(size[0]):
                    wanted = j_answer[i]
                    result = self.is_solid((i, j), com)
                    self.assertEqual(result, wanted, str(com) + ":" + str(i) + str(j))
        done = True

    def test_make_solid(self):
        size = (3, 3)
        self.cutOut(size)
        for i in range(size[0]):
            for j in range(size[1]):
                for com in self.com:
                    self.make_solid((i, j), com)
                    solid = self.is_solid((i, j), com)
                    self.assertEqual(solid, True, str(com) + ":" + str(i) + str(j))
        done = True

    def test_door(self):
        pass
        # symm = Wall(Axis.EW, 1, 1, False)
        # asym = Wall(Axis.EW, 1, 1, False)
        # none = Wall(Axis.EW, 1, 1, False)
        # blok = Wall(Axis.EW, 1, 1, True)
        # cutter = Cutter()
        # symm.doors = cutter.make(Com.E, Cut.X)
        # asym.doors = cutter.make(Com.E, Cut.H)
        # self.assertEqual(symm.door(Com.E), Cut.X, "Symm. E Should be an X")
        # self.assertEqual(symm.door(Com.W), Cut.X, "Symm. W Should be an X")
        # self.assertEqual(asym.door(Com.E), Cut.H, "Asym. E Should be an H")
        # self.assertEqual(asym.door(Com.W), Cut.B, "Asym. W Should be an B")
        # self.assertEqual(none.door(Com.E),  None, "None should be None")
        # self.assertEqual(blok.door(Com.E),  None, "Blocked should be None")

    def test_make_door(self):
        pass
        # from unittest.mock import MagicMock
        # cell_a = MagicMock(spec=Cell)
        # cell_b = MagicMock(spec=Cell)
        # tool = MagicMock(spec=Cutter)
        # doors = {Com.N: Cut.X, Com.E: Cut.I}
        # tool.make.return_value = doors
        # ew = Wall(Axis.EW, 1, 1, False)
        # border = Wall(Axis.EW, 1, 1, False)
        # ns = Wall(Axis.NS, 1, 1, False)
        # blocked = Wall(Axis.EW, 1, 1, True)
        # ew.cells[Com.E] = cell_a
        # ew.cells[Com.W] = cell_b
        # ns.cells[Com.N] = cell_a
        # ns.cells[Com.S] = cell_b
        # blocked.cells[Com.E] = cell_a
        # blocked.cells[Com.W] = cell_b
        # border.cells[Com.E] = None
        # border.cells[Com.W] = cell_b
        # self.assertEqual(ew.make_door(Com.N, tool), None, "EW cannot cut a wall North.")
        # self.assertEqual(ew.make_door(Com.S, tool), None, "EW cannot cut a wall South.")
        # self.assertEqual(ew.make_door(Com.W, tool), cell_b, "EW can cut a wall West.")
        # self.assertEqual(ns.make_door(Com.E, tool), None, "NS cannot cut a wall East.")
        # self.assertEqual(ns.make_door(Com.W, tool), None, "NS cannot cut a wall West.")
        # self.assertEqual(ns.make_door(Com.S, tool), cell_b, "NS can cut a wall South.")
        # self.assertEqual(blocked.make_door(Com.E, tool), None, "blocked cannot cut a wall East.")
        # self.assertEqual(blocked.make_door(Com.W, tool), None, "blocked cannot cut a wall West.")
        # self.assertEqual(blocked.make_door(Com.S, tool), None, "blocked cannot cut a wall South.")
        # self.assertEqual(blocked.make_door(Com.E, tool), None, "blocked cannot cut a wall East.")
        # self.assertEqual(blocked.make_door(Com.W, tool), None, "blocked cannot cut a wall West.")
        # self.assertEqual(blocked.make_door(Com.S, tool), None, "blocked cannot cut a wall South.")
        # self.assertEqual(border.make_door(Com.E, tool), None, "border cannot cut a wall East.")
        # self.assertEqual(border.make_door(Com.S, tool), None, "border cannot cut a wall South.")
        # self.assertEqual(border.make_door(Com.W, tool), cell_b, "border can cut a wall West.")
        # self.assertEqual(border.doors, doors, "Doors should be set by make_door")


if __name__ == '__main__':
    unittest.main()
