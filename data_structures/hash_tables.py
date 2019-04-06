import collections
from containers import BaseContainer


class MultiSet(BaseContainer):

    @property
    def _container(self) -> collections.defaultdict:
        return self.__table

    def __init__(self, iterable=None):
        self.__table = collections.defaultdict(int)
        self._size = 0
        if iterable:
            for item in iterable:
                self.add(item)

    def __len__(self) -> int:
        return self._size

    def __iter__(self):
        for item, count in self._container.items():
            for _ in range(count):
                yield item

    def add(self, item) -> None:
        """
        Inserts item into the set.
        """
        self._container[item] += 1
        self._size += 1

    def discard(self, item) -> None:
        """
        Removes item from the set.
        If item isn't in the set, does nothing.
        """
        if item not in self:
            return

        if self._container[item] > 1:
            self._container[item] -= 1
        else:
            del self._container[item]

        self._size -= 1

    def remove(self, item) -> None:
        """
        Removes item from the set.
        If item isn't in the set, raises a ValueError.
        """
        if item in self:
            self.discard(item)
        else:
            raise ValueError('"{0}" not in set'.format(item))

    def union(self, iterable) -> 'MultiSet':
        """
        Returns a new MultiSet containing all items in both containers.
        """
        result = MultiSet(iterable)
        for item in self:
            result.add(item)

        return result

    def intersection(self, iterable) -> 'MultiSet':
        """
        Returns a new MultiSet containing only items present in both containers.
        """
        return MultiSet((i for i in iterable if i in self))

    def count(self, item) -> int:
        """
        Returns the number of items that are in this set.
        """
        return self._container[item] if item in self else 0


if __name__ == '__main__':
    pass