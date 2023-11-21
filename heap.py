from enum import Enum
import math
from typing import Any, List, TypeVar, Optional

T = TypeVar("T")

def left_child(i: int) -> int:
    return 2 * i


def right_child(i: int) -> int:
    return left_child(i) + 1


def parent(i: int) -> int:
    return math.floor(i/2)


def swap(a, i, j):
    a[i], a[j] = a[j], a[i]


def max_heapify(heap, i: int, m: int):
    l = left_child(i)
    r = right_child(i)
    max_value = i

    if l < m and heap[l] > heap[max_value]:
        max_value = l

    if r < m and heap[r] > heap[max_value]:
        max_value = r

    if max_value != i:
        swap(heap, i, max_value)
        max_heapify(heap, max_value, m)


def min_heapify(heap, i: int, m: int):
    l = left_child(i)
    r = right_child(i)
    min_value = i

    if l < m and heap[l] < heap[min_value]:
        min_value = l

    if r < m and heap[r] < heap[min_value]:
        min_value = r

    if min_value != i:
        swap(heap, i, min_value)
        min_heapify(heap, min_value, m)


def build_heap(heap, heapify_func=min_heapify):
    heap_size = len(heap)
    n = math.floor(heap_size/2)

    for i in range(n+1):
        heapify_func(heap, n - i, heap_size)


class HeapType(Enum):
    MIN = 1
    MAX = 2


def _gt(a, b):
    return a > b


def _lt(a, b):
    return a < b


class Heap:
    _array: List[T]
    _size: int

    def __init__(self, heap_type: HeapType = HeapType.MIN):
        self._heapify_func = min_heapify if heap_type == HeapType.MIN else max_heapify
        self._element_cmp = _lt if heap_type == HeapType.MIN else _gt
        self._array = []
        self._size = 0

    def extract(self) -> Optional[T]:
        if self._size < 1:
            return None

        max_or_min = self._array[0]

        # Swap first and last element
        self._array[0] = self._array[self._size - 1]

        # Remove last element
        self._array = self._array[:-1]

        self._size -= 1

        # Heapify down
        self._heapify_func(self._array, 0, self._size)

        return max_or_min

    def insert(self, value: T):
        # Increase the size of the heap
        self._size += 1

        # Insert value at the end
        self._array.append(value)

        i = self._size - 1

        while i > 0 and self._element_cmp(value, self._array[parent(i)]):
            swap(self._array, i, parent(i))
            i = parent(i)

    def __len__(self):
        return self._size
