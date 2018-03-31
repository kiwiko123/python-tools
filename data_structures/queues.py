# Author: Geoffrey Ko (2018)
# Developed with Python 3.5.0b3
import abc
import math
import operator


class _BaseQueue(metaclass=abc.ABCMeta):
    """
    Base class defining methods common to queue-like data types.
    The underlying data structure is by default a list, but can be changed (see @property container_type).
    Derived classes MUST implement methods top(), push(), and pop().
    """
    def __init__(self, container_type=list):
       self.container_type = container_type

    @property
    def container_type(self) -> type:
        """
        Returns the type of the underlying data structure used to implement this queue.
        """
        return self.__container_type

    @container_type.setter
    def container_type(self, new_type: type) -> None:
        """
        Sets the type of the underlying data structure used to implement this queue.
        In setting the new type, it will also convert the existing container to the new type.
        """
        self.__container_type = new_type
        self.__container = new_type(self.__container)

    @property
    def _container(self) -> list:
        return self.__container

    def __repr__(self) -> str:
        return '{0}({1})'.format(type(self).__name__, self._container)

    def __str__(self) -> str:
        return repr(self)

    def __len__(self) -> int:
        """
        Returns the number of items in this queue.
        """
        return len(self._container)

    def __bool__(self) -> bool:
        """
        Returns False if this queue is empty, or True if non-empty.
        """
        return len(self) > 0

    def __contains__(self, item) -> bool:
        """
        Returns True if 'item' is contained within the queue, or False if not.
        """
        return item in self._container

    def __iter__(self):
        yield from self._container

    def __eq__(self, other) -> bool:
        return isinstance(other, type(self)) and self._container == other._container

    @abc.abstractmethod
    def top(self):
        pass

    @abc.abstractmethod
    def push(self, item) -> None:
        pass

    @abc.abstractmethod
    def pop(self):
        pass



class PriorityQueue(_BaseQueue):
    """
    A Pythonic implementation of a heap priority queue.
    The initializer provides control over order through 'key' and 'reverse' parameters, similar to sorted(...).
    By default (with reverse=False), a max-heap is used.

    heapq, a module in the Python Standard Library, makes for an efficient priority queue implementation.
    However, it is not as high level and is unnecessarily confusing to use with custom comparators.
    This implementation provides a simple, Pythonic way to use a priority queue with any ordering through
    parameters similar to sorted(...) (see __init__).
    """

    @property
    def container_type(self) -> type:
        return super().container_type

    @container_type.setter
    def container_type(self, new_type: type) -> None:
        raise ValueError('cannot change the underlying data structure for PriorityQueue (list)')


    def __init__(self, iterable=None, key=lambda x: x, reverse=False, gt=operator.gt, lt=operator.lt):
        """
        Initialize a PriorityQueue object.

        * iterable: if non-empty, adds in all items and appropriately orders them.
            - O(N) optimized - appends all items (linearly) to the underlying list, then heapifies itself.
        * key: unary callable function that returns the object to be sorted. See parameters of sorted(...) for details.
        * reverse: set True if items should be arranged in reverse order (read below).
        * gt: binary predicate that returns True if its first argument is deemed greater than its second (e.g., a > b).
            - used only when reverse=False.
        * lt: binary predicate that returns True if its first argument is deemed less than its second (e.g., a < b)
            - used only when reverse=True.

        Recall that this PriorityQueue implements a max-heap;
        an important distinction between this and sorted(...) is that by default,
        here items will be ordered from GREATEST to LEAST;
        sorted(...) by default orders items from LEAST to GREATEST.
        These orders can be flipped by setting 'reverse=True'.
        By default, items are deemed greater/less than others as per their __gt__ and __lt__ methods -
        i.e.,  the object returned by 'key(x)' must have implemented __gt__ and/or __lt__ methods.
        Alternatively, you can provide custom predicate functions as arguments to the 'gt' and 'lt' parameters
        instead of overloading __gt__ and __lt__ methods.
        """
        if not callable(key):
            raise ValueError('key must be a unary callable predicate')
        super().__init__()
        self._key = key
        self._reverse = reverse
        self._gt = lt if reverse else gt

        if iterable:
            for item in iterable:
                self._container.append(item)
            self._heapify()


    def __repr__(self) -> str:
        return '{0}({1}, key={2}, reverse={3})'.format(type(self).__name__, self._container, self._key, self._reverse)


    def __str__(self) -> str:
        heap = self.copy()
        s = ', '.join([str(heap.pop()) for _ in range(len(heap))])
        return '{0}({1})'.format(type(self).__name__, s)


    def copy(self, deep=True) -> 'PriorityQueue':
        """
        Returns a copy of the object.
        If deep=True, returns a deep copy (different object, same contents).
        Otherwise, returns a reference to itself (same object).

        Θ(n) time when deep=True,
        Θ(1) time otherwise.
        """
        return PriorityQueue(self._container, key=self._key, reverse=self._reverse) if deep else self


    def top(self):
        """
        Returns the highest-priority object in the queue.
        Raises ValueError if the queue is empty.

        Θ(1) time.
        """
        if not self:
            raise ValueError('queue is already empty')
        return self._container[0]


    def push(self, item) -> None:
        """
        Adds 'item' into the queue, in its appropriate order.

        O(log n) time.
        """
        self._container.append(item)
        self._sift_up(len(self) - 1)


    def pop(self):
        """
        Removes and returns the highest-priority object in the queue.
        Re-orders the queue if necessary.
        Raises ValueError if the queue is already empty.

        O(log n) time.
        """
        if not self:
            raise ValueError('pop from empty queue')
        result = self._container[0]
        self.remove(0)
        return result


    def remove(self, index: int) -> None:
        """
        Caution - do not use this unless fine-grained control is needed.
        Use sparingly in conjunction with the methods 'find(...)' and 'view()'.

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


    def view(self) -> tuple:
        """
        Returns a tuple representing the underlying list.
        A separate tuple is returned as to prevent modification of the underlying list.

        Use in conjunction with the methods 'find(...)' and 'remove(...)'.

        Θ(n) time.
        """
        return tuple(self._container)


    def find(self, item) -> int:
        """
        Returns the index of item in the underlying list, or -1 if not found.
        Similar to list.index, but returns -1 upon failure instead of raising ValueError.

        Use in conjunction with the methods 'view()' and 'remove(...)'.

        O(n) time.
        """
        try:
            return self._container.index(item)
        except ValueError:
            return -1


    def _compare(self, a: int, b: int) -> bool:
        """
        Returns True if key(a) is greater than key(b) (or 'less than' if reverse=True).
        """
        return self._gt(self._key(self._container[a]), self._key(self._container[b]))


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
        else:
            return

        if self._compare(larger, i):
            self._container[i], self._container[larger] = self._container[larger], self._container[i]
            self._sift_down(larger)


    def _heapify(self) -> None:
        """
        Converts the arbitrary list into a heap.

        O(n) time.
        """
        for i in range(self._parent_of(len(self)), -1, -1):
            self._sift_down(i)


    def _in_heap(self, i: int) -> bool:
        """
        Returns True if index 'i' is within the bounds of the list's size.

        Θ(1) time.
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