# This module contains two known algorithms for selecting the k-th smallest value from a collection.
# Both methods consist of selecting some "median" value m*, then partitioning the collection into 3 sequences:
#
#   L: values strictly less than m*
#   E: values equal to m*
#   G: values strictly greater than m*
#
# If k is less than |L|, recursively select from L.
# Otherwise, if k equals |E|, then the k-th smallest value is m*.
# Otherwise, recursively select the (k - |L| - |E|)th value from G.
#
# In this example, and in the functions below, note that k is 1-indexed.
#
# For more information about selection, read https://en.wikipedia.org/wiki/Selection_algorithm.
#
# Author: Geoffrey Ko (2018)
import math
import random


def brute_force_select(iterable, k: int):
    """ Returns the k-th smallest value in iterable by sorting and taking the k-th index.
        k is 1-indexed.
    """
    iterable = sorted(iterable)
    return iterable[k]


def quick_select(iterable, k: int):
    """ Returns the k-th smallest value of iterable in average-case linear time.
        Chooses a random "median", then partitions iterable and recursively selects the k-th smallest value.

        Because m* is chosen at random, there is a worst-case run time of Θ(n^2).
        However, the idea is that at least half the time, 1/4 of the elements will be eliminated.
        With this assumption, we can represent the running time as a geometric series:

        run_time = b[n + n(3/4) + n(3/4)^2 + n(3/4)^3 + ...]
                 ∈ O(n)

        where b is the overhead of each recursive call.
    """
    random_median_index = random.randrange(len(iterable))
    median = iterable[random_median_index]

    return _base_select(quick_select, median, iterable, k)


def deterministic_select(iterable, k: int):
    """ Returns the k-th smallest value of iterable in linear time.

        1) Divides iterable into ⌈n/5⌉ groups, where n is the number of elements in iterable.
        2) Computes the median of each group through brute-force (i.e., sorting and choosing the middle element).
           Note that this step is considered to be done in constant time, since each group is of fixed length 5 (except possibly the last, which could be smaller).
        3) Computes the median-of-medians by deterministically selecting the middle value from the medians of each group.
        4) Partitions iterable, and recursively selects the k-th smallest value.

        Although this is done in linear time, there is a high constant associated with brute-forcing the medians.
        Quick-select could very well perform faster in some cases.
    """
    constant = 5
    size = len(iterable)
    if size <= constant:
        return brute_force_select(iterable, k)

    n_groups = _ceil(size / constant)
    groups = [[None for _ in range(constant)] for _ in range(n_groups)]
    overflow = size % constant
    groups[-1] = groups[-1][:(overflow if overflow else size)]    # truncate the last group to its actual size if it's less than 5

    # divide into ⌈n/5⌉ groups
    for i in range(len(iterable)):
        groups[i // constant][i % constant] = iterable[i]

    # find the median of each group through brute force
    medians = []
    for group in groups:
        local_median = brute_force_select(group, _ceil(len(group) / 2))
        medians.append(local_median)

    median_of_medians = deterministic_select(medians, _ceil(len(medians) / 2))
    return _base_select(deterministic_select, median_of_medians, iterable, k)


def _base_select(selector: callable, median, iterable, k: int):
    """ Recursive selection.
        Partitions iterable into L, E, G:
          L: values strictly less than median
          E: values equal to median
          G: values strictly greater than median
        Recursively selects the k-th smallest value from iterable.

        Values in iterable must implement comparison operators.
        iterable must implement __getitem__.
    """
    less = []
    greater = []
    equal_count = 0

    for item in iterable:
        if item < median:
            less.append(item)
        elif item > median:
            greater.append(item)
        else:
            equal_count += 1

    if k <= len(less):
        return selector(less, k)
    elif k <= len(less) + equal_count:
        return median
    else:
        return selector(greater, k - len(less) - equal_count)


def _ceil(n: float) -> int:
    """ Like math.ceil(), but returns the value as an integer. """
    return int(math.ceil(n))


if __name__ == '__main__':
    pass