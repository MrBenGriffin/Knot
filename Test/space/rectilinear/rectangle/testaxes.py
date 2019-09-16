import unittest
from knot.space.crs import Symmetry
from knot.space.rectilinear.rectangle import Paper


class TestAxes(unittest.TestCase):

    def test_paper_str(self):
        answer = {Paper.master: "Master", Paper.sunset: "Sunset",
                  Paper.vanity: "Vanity", Paper.mirror: "Mirror"}
        for item in Paper:
            self.assertEqual(str(item), answer[item], "Should be " + answer[item])

    def test_paper_identity(self):
        self.assertEqual(Paper.identity(), Paper.master, "Should be master")

    def test_paper_select(self):
        answer = {"N": "Master", "H": "Sunset",
                  "V": "Vanity", "F": "Mirror", "R": "Mirror"}
        for item in Symmetry.choices():
            self.assertEqual(str(Paper.select(item)), answer[item], "Should be " + answer[item])


if __name__ == '__main__':
    unittest.main()
