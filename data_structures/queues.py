# Author: Geoffrey Ko (2018)
# Developed with Python 3.5.0b3
import abc
import math
import operator
from .containers import BaseContainer


class BaseQueue(BaseContainer, metaclass=abc.ABCMeta):
    """
    Base class defining methods common to queue-like data types.
    The underlying data structure is by default a list, but can be changed (see @property _container_type).
    Derived classes MUST implement methods top(), push(), and pop().
    """
    def __init__(self, iterable=None, container_type=list):
        self._can_override_container_type = True
        self.__container_type = container_type
        self.__container = container_type()
        self._can_override_container_type = False

    @property
    def _container_type(self) -> type:
        """
        Returns the type of the underlying data structure used to implement this queue.
        """
        return self.__container_type

    @_container_type.setter
    def _container_type(self, new_type: type) -> None:
        """
        Sets the type of the underlying data structure used to implement this queue.
        In setting the new type, it will also convert the existing container to the new type.
        """
        if not self._can_override_container_type:
            raise ValueError('The underlying data structure of this queue is unmodifiable')

        self.__container_type = new_type
        self.__container = new_type(self.__container)

    @property
    def _container(self) -> list:
        return self.__container

    @abc.abstractmethod
    def top(self):
        """
        Returns the first item in the queue.
        Raises ValueError if empty.
        """
        pass

    @abc.abstractmethod
    def push(self, item) -> None:
        """
        Pushes item into the queue.
        """
        pass

    @abc.abstractmethod
    def pop(self):
        """
        Removes and returns the first item in the queue.
        The first item in the queue must be the same value returned by top().
        Raises ValueError if empty.
        """
        pass



class PriorityQueue(BaseQueue):
    """
    A Pythonic implementation of a heap priority queue.
    The initializer provides control over order through 'key' and 'reverse' parameters, similar to sorted(...).
    By default (with reverse=False), a max-heap is used.

    heapq, a module in the Python Standard Library, makes for an efficient priority queue implementation.
    However, it is not as high level and offers little control over custom comparators.
    This implementation provides a simple, Pythonic way to use a priority queue with any ordering through a key function.
    """

    @property
    def _container_type(self) -> type:
        return super()._container_type


    def __init__(self, iterable=None, key=lambda x: x, reverse=False, greater_than=operator.gt, less_than=operator.lt):
        """
        Initialize a PriorityQueue object.

        * iterable: if non-empty, adds in all items and appropriately orders them.
            - O(N) optimized - appends all items (linearly) to the underlying list, then heapifies itself.
        * key: unary callable function that returns the object to be sorted. See parameters of sorted(...) for details.
            - TIP: to sort by multiple criteria, use a tuple, where each item is the sorting predicate;
              e.g., to sort first by even numbers, then numbers less than 10, use:
                key=lambda x: (x % 2 == 0, x < 10)
              Items will be sorted in the order that the criteria appears in the returned tuple.
        * reverse: set True if items should be arranged in reverse order (read below).
        * gt: binary predicate that returns True if its first argument is deemed greater than its second (e.g., a > b).
            - used only when reverse=False.
        * lt: binary predicate that returns True if its first argument is deemed less than its second (e.g., a < b)
            - used only when reverse=True.

        This PriorityQueue implements a max-heap.
        An important distinction between this and sorted(...) is that by default,
        items will be ordered from GREATEST to LEAST,
        while sorted(...) by default orders items from LEAST to GREATEST.
        These orders can be flipped by setting 'reverse=True'.
        By default, items are deemed greater/less than others as per their __gt__ and __lt__ methods -
        i.e.,  the object returned by 'key(x)' must have implemented __gt__ and/or __lt__ methods.
        Alternatively, you can provide custom predicate functions as the 'gt' and 'lt' parameters.
        """
        super().__init__()

        if not callable(key):
            raise ValueError('key must be a unary callable predicate')

        self._key = key
        self._reverse = reverse
        self._gt = less_than if reverse else greater_than

        if iterable:
            for item in iterable:
                self._container.append(item)
            self._heapify()


    def __repr__(self) -> str:
        return '{0}({1}, key={2}, reverse={3})'.format(type(self).__name__, self._container, self._key, self._reverse)


    def __str__(self) -> str:
        contents = ', '.join([str(item) for item in self.view()])
        return '{0}({1})'.format(type(self).__name__, contents)


    def copy(self) -> 'PriorityQueue':
        """
        Returns a new PriorityQueue object containing the same properties and values as this one.
        """
        return PriorityQueue(self._container, key=self._key, reverse=self._reverse)


    def top(self):
        """
        Returns the highest-priority object in the queue.
        Raises ValueError if the queue is empty.

        O(1) time.
        """
        if not self:
            raise ValueError('Cannot retrieve the top of an empty queue')
        return self._container[0]


    def push(self, item) -> None:
        """
        Adds 'item' into the queue, in its appropriate order.

        O(log n) time.
        """
        self._container.append(item)
        size = len(self) - 1
        self._sift_up(size)


    def pop(self):
        """
        Removes and returns the highest-priority object in the queue.
        Re-orders the queue if necessary.
        Raises ValueError if the queue is already empty.

        O(log n) time.
        """
        if not self:
            raise ValueError('Cannot pop from an empty queue')

        result = self._container[0]
        self._remove(0)
        return result


    def view(self) -> list:
        """
        Returns an ordered list containing all the items in the queue.
        The list's order respects the queue's `reverse` and `gt` properties.

        O(nlogn) time.
        """
        result = []
        copy = self.copy()
        while copy:
            next_value = copy.pop()
            result.append(next_value)

        return result


    def _remove(self, index: int) -> None:
        """
        Helper method that removes the item at position 'index' in the underlying list.
        Raises ValueError if the queue is already empty.
        Raises IndexError if 'index' is out of bounds.

        O(log n) time.
        """
        if not self:
            raise ValueError('removal from empty queue')
        if not self._in_heap(index):
            raise IndexError('index {0} out of bounds'.format(index))

        self._container[index] = self._container[-1]
        self._container.pop()
        self._sift_up(index)
        self._sift_down(index)


    def _compare(self, a: int, b: int) -> bool:
        """
        Returns True if key(a) is greater than key(b) (or 'less than' if reverse=True).
        """
        key_a = self._key(self._container[a])
        key_b = self._container[b]
        return self._gt(key_a, key_b)


    def _sift_up(self, i: int) -> None:
        """
        Recursively swaps the value at list index 'i' with its parent until the invariant is restored.

        O(log n) time.
        """
        parent = self._parent_of(i)
        if self._in_heap(i) and self._in_heap(parent) and self._compare(i, parent):
            self._container[i], self._container[parent] = self._container[parent], self._container[i]
            self._sift_up(parent)


    def _sift_down(self, i: int) -> None:
        """
        Recursively swaps the value at list index 'i' with the larger of its 2 children until the invariant is restored.

        O(log n) time.
        """
        left = self._left_child(i)
        right = self._right_child(i)
        larger = None

        if self._in_heap(right) and self._compare(right, left):
            larger = right
        elif self._in_heap(left):
            larger = left

        if larger is not None and self._compare(larger, i):
            self._container[i], self._container[larger] = self._container[larger], self._container[i]
            self._sift_down(larger)


    def _heapify(self) -> None:
        """
        Converts the underlying list into a heap.

        O(n) time.
        """
        size = len(self)
        first_parent = self._parent_of(size)
        for i in range(first_parent, -1, -1):
            self._sift_down(i)


    def _in_heap(self, i: int) -> bool:
        """
        Returns True if index 'i' is within the bounds of the list's size.
        """
        return 0 <= i < len(self)


    @staticmethod
    def _parent_of(i: int) -> int:
        """
        Returns the index of i's parent ((i - 1) // 2) in the heap.
        """
        return math.floor((i - 1) / 2)


    @staticmethod
    def _left_child(i: int) -> int:
        """
        Returns the index of i's left child (2i + 1) in the heap.
        """
        return 2 * i + 1


    @staticmethod
    def _right_child(i: int) -> int:
        """
        Returns the index of i's right child (2i + 2) in the heap.
        """
        return 2 * i + 2


if __name__ == '__main__':
    pass
