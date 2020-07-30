def swap(arr: list, index_a: int, index_b: int) -> None:
    arr[index_a], arr[index_b] = arr[index_b], arr[index_a]


def merge(arr: list, midpoint_index: int) -> None:
    left = 0
    right = midpoint_index
    copy = list(arr)
    counter = 0

    while left < midpoint_index and right < len(copy):
        if copy[left] <= copy[right]:
            arr[counter] = copy[left]
            left += 1
        else:
            arr[counter] = copy[right]
            right += 1
        counter += 1

    while left < midpoint_index:
        arr[counter] = copy[left]
        left += 1
        counter += 1

    while right < len(copy):
        arr[counter] = copy[right]
        right += 1
        counter += 1



def partition(arr: list, select_pivot_index=lambda l: 0) -> int:
    pivot_index = select_pivot_index(arr)
    pivot_value = arr[pivot_index]

    swap(arr, pivot_index, len(arr) - 1)

    left = 0
    right = len(arr) - 2

    while True:
        while left < pivot_index and arr[left] < pivot_value:
            left += 1
        while left < right and arr[right] >= pivot_value:
            right -= 1

        if left >= right:
            break

        swap(arr, left, right)
        left += 1
        right -= 1

    swap(arr, pivot_index, right)
    return pivot_index


def selection_sort(arr: list) -> None:
    """
    Start at the end of the list, and scan backwards.
    Find the maximum value from the beginning of the list up to the current index.
    Swap the maximum value with the value at the current index.
    Move the pointer backwards one position, then repeat.

    Note that this algorithm can also work by starting at the beginning, and finding the minimum value each time.

    * Time complexity: Θ(n^2).
    * In-place.
    * Unstable.

    :param arr: the list to be sorted
    """
    for i in range(len(arr) - 1, 0, -1):
        local_max, index_of_local_max = max((value, index) for index, value in enumerate(arr[:i]))
        if arr[i] < local_max:
            swap(arr, i, index_of_local_max)


def insertion_sort(arr: list) -> None:
    """
    Maintain a threshold that divides the list into two groups -- one to the threshold's left, and one to its right.
    Values to the left of the threshold are known to be sorted.
    Values to the right of the threshold are unknown, and assumed to be unsorted.

    The invariant condition is that each value in the list must be greater than or equal to the previous value.
    Start at the beginning of the list, and scan forwards.
    Each time the invariant is broken (i.e., the current value at the threshold is less than the previous value),
    keep swapping it backwards with its preceding neighbor until the invariant is restored.

    * Time Complexity: O(n^2).
       - Worst case: Θ(n^2)
       - Average case: Θ(n^2)
       - Best case: Θ(n)
          + In the best case, the list is already sorted. No swapping will occur, and (n - 1) comparisons will be made.
    * In-place.
    * Stable.
       - Equal values aren't swapped

    :param arr: the list to be sorted
    """
    for threshold_index in range(1, len(arr)):
        i = threshold_index
        while i > 0 and arr[i] < arr[i - 1]:
            swap(arr, i, i - 1)
            i -= 1


def merge_sort(arr: list) -> None:
    # BROKEN
    midpoint = len(arr) // 2
    if not midpoint:
        return

    merge_sort(arr[:midpoint])
    merge_sort(arr[midpoint:])
    merge(arr, midpoint)


def quick_sort(arr: list, partition_function=partition) -> None:
    # BROKEN
    if not arr:
        return

    pivot_index = partition_function(arr)
    quick_sort(arr[:pivot_index], partition_function)
    quick_sort(arr[pivot_index+1:], partition_function)



if __name__ == '__main__':
    # l = [7, 10, 3, 2, 6, 13, 15, 12, 16, 4, 5, 9, 14, 1, 11, 8]
    l = [6, 3, 7, 1, 2, 8, 5, 4]
    # partition_function = lambda arr: partition(arr, lambda x: len(x) - 1)
    merge_sort(l)
    print(l)
