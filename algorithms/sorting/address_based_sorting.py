# Address-based calculation sorts.

import math

def counting_sort(arr: [int], max_value=None) -> None:
    if max_value is None:
        max_value = max(arr)

    locator = [0 for _ in range(max_value + 1)]
    for value in arr:
        locator[value] += 1
    for i in range(1, max_value + 1):
        locator[i] += locator[i - 1]

    copy = list(arr)
    for value in copy:
        locator[value] -= 1
        arr[locator[value]] = value


def bucket_sort(arr: [int], number_of_buckets: int, max_value=None, sort_bucket=list.sort) -> None:
    if max_value is None:
        max_value = max(arr)

    # Distribute the values into buckets.
    bucket_range = math.ceil(max_value / number_of_buckets)
    buckets = [[] for _ in range(number_of_buckets)]
    for value in arr:
        bucket_index = value // bucket_range
        buckets[bucket_index].append(value)

    # Sort each individual bucket.
    for bucket in buckets:
        sort_bucket(bucket)

    # Combine the sorted buckets.
    i = 0
    for bucket in buckets:
        for value in bucket:
            arr[i] = value
            i += 1


if __name__ == '__main__':
    import cProfile, random

    l = [random.randrange(999999) for _ in range(10000)]
    pr = cProfile.Profile()
    pr.enable()
    bucket_sort(l, 100)
    pr.disable()
    pr.print_stats()