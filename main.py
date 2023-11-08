import math
from typing import List

import click
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

from astar import is_inaccessible, a_star_find


def to_int(x) -> List[int]:
    numbers = filter(lambda n: len(n) > 0, x)
    numbers = map(int, numbers)

    return list(numbers)


def plot_map(grid):
    if not isinstance(grid, np.ndarray):
        grid = np.array(grid)

    # Create a colormap where -1's are black (blocked), 0's are green (free), and positive values (weights) are
    # varying intensities of red
    cmap = LinearSegmentedColormap.from_list('astar', ['black', 'green', 'red'])
    fig, ax = plt.subplots(figsize=grid.shape)

    # Plot the grid using the custom colormap
    img = ax.imshow(grid, cmap=cmap)

    # Set color limits to define the range of values that each color in the colormap represents
    img.set_clim(-1, grid.max() +3)

    # Show the weight of each cell
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            ax.text(j, i, grid[i, j],
                    ha="center",
                    va="center",
                    color="w")


def annotate_solution(grid, solution):
    actual_solution_map = np.copy(grid)
    for pos in solution:
        if is_inaccessible(actual_solution_map, pos):
            actual_solution_map[pos[0], pos[1]] = math.inf
        else:
            actual_solution_map[pos[0], pos[1]] = 5
    return actual_solution_map


@click.command()
@click.option('--input', type=click.File('r'), help='The file containing the coordinates.', default="input-example")
@click.option('--output', help='The path for the solution image.', default="solution.png")
def main(input, output):
    start = to_int(input.readline().split(" "))
    end = to_int(input.readline().split(" "))

    lines: List[str] = input.readlines()

    grid = []

    for line in lines:
        weights = to_int(line.strip("\n").split(" "))
        grid.append(weights)

    grid = np.array(grid)

    solution = a_star_find(grid, tuple(start), tuple(end))

    plot_map(annotate_solution(grid, solution))

    print(f"Generating solution file {output}")

    plt.savefig(output, dpi=100, bbox_inches='tight')


if __name__ == '__main__':
    main()
