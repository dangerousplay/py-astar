import itertools
from typing import Tuple, Any, List, Optional

import numpy as np

from heap import Heap

Point = Tuple[int, int]


def distance(pos_a, pos_b):
    x = pos_b[0] - pos_a[0]
    y = pos_b[1] - pos_a[1]

    return abs(x) + abs(y)


class Cell:
    position: Tuple[int, int]
    came_from: Any
    weight: int
    g_cost: int
    h_cost: int
    f_cost: int

    def __init__(self, position: Point, end: Point, g_cost: int, weight: int = 0):
        self.position = position
        self.g_cost = g_cost
        self.h_cost = distance(position, end)
        self.came_from = None
        self.weight = weight

    @property
    def f_cost(self):
        return self.h_cost + self.g_cost + self.weight

    def __lt__(self, other):
        if other is None or not isinstance(other, Cell):
            return False

        return other.f_cost > self.f_cost

    def __le__(self, other):
        if other is None or not isinstance(other, Cell):
            return False

        return other.f_cost >= self.f_cost

    def __ge__(self, other):
        if other is None or not isinstance(other, Cell):
            return False

        return other.f_cost <= self.f_cost

    def __gt__(self, other):
        if other is None or not isinstance(other, Cell):
            return False

        return other.f_cost < self.f_cost

    def __eq__(self, other):
        if other is None or not isinstance(other, Cell):
            return False

        return other.position == self.position

    def __hash__(self):
        return hash(self.position)


def get_neighbours(matrix: np.ndarray, x: int, y: int, allow_diagonal_movement=False):
    rows, cols = len(matrix), len(matrix[0])

    potential_neighbours = [(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]

    if allow_diagonal_movement:
        potential_neighbours += [(x + 1, y + 1), (x + 1, y - 1), (x - 1, y - 1), (x - 1, y + 1)]

    neighbours = []

    for nx, ny in potential_neighbours:
        if 0 <= nx < rows and 0 <= ny < cols:
            neighbours.append((nx, ny))

    return neighbours


def is_inaccessible(grid, pos):
    return grid[pos[0], pos[1]] < 0


def a_star_find(grid: np.ndarray, start: Point, goal: Point) -> Tuple[List[Point], int]:
    evaluated_cells = set()
    start_cell = Cell(start, goal, g_cost=1)

    open_cells = Heap()
    open_cells.insert(start_cell)

    current: Optional[Cell] = None
    cost = 0

    while len(open_cells) > 0:
        # remove the node with lowest f score
        current = open_cells.extract()

        node_position = current.position

        if node_position == goal:
            break

        neighbours = get_neighbours(grid, node_position[0], node_position[1])

        for nb in neighbours:
            if nb in evaluated_cells or is_inaccessible(grid, nb):
                continue

            nb_cell = Cell(nb, goal, g_cost=current.g_cost + 1, weight=grid[nb[0]][nb[1]])
            nb_cell.came_from = current
            open_cells.insert(nb_cell)

        evaluated_cells.add(current.position)

    path = []

    while current is not None:
        path.append(current.position)
        current = current.came_from

        if current is not None and current.came_from is not None:
            cost += 1 + current.weight

    # Reverse the path points to return it from start to end
    return path[::-1], cost
