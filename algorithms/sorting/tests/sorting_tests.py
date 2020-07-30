import cProfile
import random
import unittest
from algorithms import sorting

class SortingTest(unittest.TestCase):

    def setUp(self) -> None:
        self.values = []
        self.expected = None
        self.sort = list.sort # Override this
        self.profile_test_runs = False

    def set_up_values(self, values: list) -> None:
        self.values = values
        self.expected = sorted(values)

    def assert_values_sorted(self) -> None:
        message = 'Expected: {0}\nActual: {1}'.format(self.expected, self.values)
        self.assertListEqual(self.expected, self.values, message)

    def run_test(self, values: list) -> None:
        self.set_up_values(values)

        if self.profile_test_runs:
            self._profile_sort_operation()
        else:
            self.sort(self.values)

        self.assert_values_sorted()

    def _profile_sort_operation(self) -> None:
        pr = cProfile.Profile()
        pr.enable()
        self.sort(self.values)
        pr.disable()
        pr.print_stats()


class NumberSortTest(SortingTest):
    def test_unordered_numbers_short(self) -> None:
        self.run_test([1, 6, 2, 5, 4, 3])

    def test_random_numbers(self) -> None:
        random_values = [random.randrange(999999) for _ in range(5000)]
        self.run_test(random_values)


class SelectionSortTest(NumberSortTest):
    def setUp(self) -> None:
        super().setUp()
        self.sort = sorting.selection_sort


class InsertionSortTest(NumberSortTest):
    def setUp(self) -> None:
        super().setUp()
        self.sort = sorting.insertion_sort


class CountingSortTest(NumberSortTest):
    def setUp(self) -> None:
        super().setUp()
        self.sort = sorting.counting_sort


class BucketSortTest(NumberSortTest):
    def setUp(self) -> None:
        super().setUp()
        self.sort = lambda arr: sorting.bucket_sort(arr, 10)


if __name__ == '__main__':
    unittest.main()
