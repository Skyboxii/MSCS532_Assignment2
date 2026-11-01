import random
import unittest

from sorts import merge_sort, quick_sort

SORTERS = {
    "merge": merge_sort,
    "quick": quick_sort,
    "quick_random": lambda A: quick_sort(A, randomized=True),
}


class TestSorts(unittest.TestCase):
    def check(self, data):
        for name, sort in SORTERS.items():
            with self.subTest(algorithm=name, data=data[:10]):
                self.assertEqual(sort(data), sorted(data))

    def test_edge_cases(self):
        self.check([])
        self.check([1])
        self.check([2, 1])
        self.check([5, 5, 5, 5])

    def test_sorted_and_reversed(self):
        self.check(list(range(500)))
        self.check(list(range(500, 0, -1)))

    def test_random(self):
        for _ in range(50):
            self.check([random.randint(-100, 100) for _ in range(random.randint(0, 200))])

    def test_input_not_modified(self):
        data = [3, 1, 2]
        for sort in SORTERS.values():
            sort(data)
        self.assertEqual(data, [3, 1, 2])


if __name__ == "__main__":
    unittest.main()
