# Simulates Banker's Algorithm.
import random


class ResourceVector(list):
    def __init__(self, *iterable):
        super().__init__(*iterable)

    def __lt__(self, other) -> bool:
        """ Returns True if all items in other are < corresponding items in self """
        return all(l < r for l, r in zip(self, other))

    def __le__(self, other) -> bool:
        return all(l <= r for l, r in zip(self, other))

    def __add__(self, other):
        """ Returns a ResourceVector with each number added up;
            e.g. [1, 2, 3] + [1, 1, 1] = [2, 3, 4]
        """
        ResourceVector._check_type(other)
        return ResourceVector([l + r for l, r in zip(self, other)])

    def __iadd__(self, other):
        self = self + other
        return self

    def __sub__(self, other):
        ResourceVector._check_type(other)
        return ResourceVector([l - r for l, r in zip(self, other)])

    def __isub__(self, other):
        self = self - other
        return self

    def find(self, value, *bounds) -> int:
        try:
            return self.index(value, *bounds)
        
        except ValueError:
            return -1

    @staticmethod
    def _check_type(other):
        if not isinstance(other, list):
            raise TypeError('{0} must be an instance of list; was type {1}'.format(other, type(other)))



#
# <Functions>
#
def to_resource_vector(matrix) -> ResourceVector:
    """ Returns iterable matrix as a ResourceVector """
    result = ResourceVector()
    for i in matrix:
        if hasattr(i, '__iter__'):
            result.append(to_resource_vector(i))
        else:
            result.append(i)

    return result


def calculate_need(allocation: [[int]], max_matrix: [[int]]) -> ResourceVector:
    """ Returns max - allocation """
    allocation, max_matrix = to_resource_vector(allocation), to_resource_vector(max_matrix)
    return max_matrix - allocation


def safe_state(allocation: [[int]], max_matrix: [[int]], available: [int]) -> ResourceVector:
    work = ResourceVector(available)
    need = calculate_need(allocation, max_matrix)
    finish = [False] * len(need)
    i = 0
    result = ResourceVector()

    while False in finish and any(v <= work for v in need):
        if not finish[i] and need[i] <= work:
            work += allocation[i]
            finish[i] = True
            result.append(i)
        i += 1
        if i >= len(need):
            i = 0

    return result if all(finish) else ResourceVector()


def rsafe_state(allocation: [[int]], max_matrix: [[int]], available: [int]) -> ResourceVector:
    work = ResourceVector(available)
    need = calculate_need(allocation, max_matrix)
    finish = [False] * len(need)
    result = ResourceVector()
    remaining = {i for i in range(len(need))}

    while False in finish and any((v <= work for v in need)):
        if not remaining:
            remaining = {i for i in range(len(need))}

        while True:
            i = random.randrange(len(need))
            if i in remaining:
                remaining.remove(i)
                break
        print(i)
        if not finish[i] and need[i] <= work:
            work += allocation[i]
            finish[i] = True
            result.append(i)

    return result if all(finish) else ResourceVector()


def is_sequence_safe(allocation: [[int]], max_matrix: [[int]], available: [int], sequence: [int]) -> bool:
    work = ResourceVector(available)
    need = calculate_need(allocation, max_matrix)
    finish = [False] * len(need)

    for i in sequence:
        if not finish[i] and need[i] <= work:
            work += allocation[i]
            finish[i] = True
        else:
            return False

    return all(finish)


#
# </Functions>
#



if __name__ == '__main__':
    allocation_list = [[3, 0, 1, 1], [0, 1, 0, 0], [1, 1, 1, 0], [1, 1, 0, 1], [0, 0, 0, 0]]
    max_list = [[4, 1, 1, 1], [0, 2, 1, 2], [4, 2, 1, 0], [1, 1, 1, 1], [2, 1, 1, 0]]
    available_list = [1, 0, 2, 0]

    allocation = to_resource_vector(allocation_list)
    max_matrix = to_resource_vector(max_list)
    available = to_resource_vector(available_list)
    need = calculate_need(allocation, max_matrix)

    print('Allocation:', allocation)
    print('Max:', max_matrix)
    print('Available:', available)
    print('Need:', need)

    print()

    safe = safe_state(allocation, max_matrix, available)
    print('SAFE STATE:', safe)

    solution_seq = [3, 0, 1, 2, 4]
    sol_safe = is_sequence_safe(allocation, max_matrix, available, solution_seq)
    print('SOLUTION SAFE?', sol_safe)
