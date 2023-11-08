import io

import numpy as np
from mazelib import Maze
from mazelib.generate.Prims import Prims
from mazelib.solve.BacktrackingSolver import BacktrackingSolver


def main():
    m = Maze()
    m.generator = Prims(10, 10)
    m.generate()

    m.solver = BacktrackingSolver()

    m.generate_monte_carlo(10)

    m.solve()

    solution = m.solutions[0]

    grid: np.ndarray = m.grid * -1

    start = solution[0]
    end = solution[-1]

    with io.open('input-example', 'w+') as f:
        f.write(f"{start[0]} {start[1]}\n")
        f.write(f"{end[0]} {end[1]}\n")

        for x in grid:
            for weight in x:
                f.write(f"{weight} ")
            f.write("\n")

if __name__ == '__main__':
    main()