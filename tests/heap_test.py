import unittest
from random import shuffle

from ddt import data, unpack, ddt

from heap import Heap, HeapType


@ddt
class TestHeap(unittest.TestCase):

    @data(*[
        {'typ': HeapType.MAX, 'order': lambda x: x},
        {'typ': HeapType.MIN, 'order': reversed},
    ])
    @unpack
    def test_insert(self, typ, order):
        h = Heap(heap_type=typ)

        for i, v in enumerate(order(range(100))):
            h.insert(v)
            self.assertEqual(h._array[0], v)
            self.assertEqual(len(h), i+1)

    @data(*[
        {'typ': HeapType.MIN, 'order': lambda x: x},
        {'typ': HeapType.MAX, 'order': reversed},
    ])
    @unpack
    def test_extract(self, typ, order):
        h = Heap(heap_type=typ)

        items = []

        for i in range(100):
            items.append(i)

        items_input = items.copy()
        shuffle(items_input)

        for i in items_input:
            h.insert(i)

        self.assertEqual(len(h), len(items_input))

        for i in order(items):
            actual = h.extract()
            self.assertEqual(actual, i)

        self.assertEqual(len(h), 0)

    def test_len(self):
        h = Heap()

        for i in range(5):
            h.insert(i)

        self.assertEqual(len(h), 5)

        h.extract()
        self.assertEqual(len(h), 4)


if __name__ == '__main__':
    unittest.main()
