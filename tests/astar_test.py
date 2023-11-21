import unittest
from ddt import ddt, data, file_data, idata, unpack

from mazelib import Maze
from mazelib.generate.BinaryTree import BinaryTree
from mazelib.generate.GrowingTree import GrowingTree
from mazelib.generate.Prims import Prims
from mazelib.generate.Sidewinder import Sidewinder
from mazelib.solve.BacktrackingSolver import BacktrackingSolver

from astar import a_star_find


def generate_cases(algorithms, positions):
    for algo in algorithms:
        for pos in positions:
            yield algo, pos


@ddt
class AStarTestCase(unittest.TestCase):

    @data(
        *generate_cases(
            [Prims, BinaryTree, GrowingTree, Sidewinder],
            [(10, 10), (10, 13), (13, 10), (5, 10), (10, 5), (5, 17), (17, 5)]
        )
    )
    @unpack
    def test_astar(self, algorithm, pos):
        x_size, y_size = pos

        for _ in range(10):
            m = Maze()
            m.generator = algorithm(x_size, y_size)
            m.generate()

            m.solver = BacktrackingSolver()
            m.generate_monte_carlo(10)
            m.solve()

            solution = m.solutions[0]
            grid = m.grid * -1

            start = solution[0]
            end = solution[-1]

            actual, _ = a_star_find(grid, start, end)

            self.assertEqual(actual, solution)


if __name__ == '__main__':
    unittest.main()
