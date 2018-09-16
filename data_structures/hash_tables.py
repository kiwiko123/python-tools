import collections
from .containers import BaseContainer


class MultiSet(BaseContainer):

    @property
    def _container(self) -> collections.defaultdict:
        return self.__table

    def __init__(self, iterable=[]):
        self.__table = collections.defaultdict(int)
        self._size = 0

    def __str__(self) -> str:
        return '{0}({1})'.format(
            type(self).__name__,
            ', '.join([str(i) for i in self])
        )

    def __repr__(self) -> str:
        return str(self)

    def __len__(self) -> int:
        return self._size

    def __iter__(self):
        for item, count in self._container.items():
            for _ in range(count):
                yield(item)

    def add(self, item) -> None:
        self._container[item] += 1
        self._size += 1

    def discard(self, item) -> None:
        if item in self:
            if self._container[item] > 1:
                self._container[item] -= 1
            else:
                del self._container[item]
            self._size -= 1

    def remove(self, item) -> None:
        if item in self:
            self.discard(item)
        else:
            raise KeyError('"{0}" not in set'.format(item))

    def union(self, other: set) -> 'MultiSet':
        if isinstance(other, set) or isinstance(other, MultiSet):
            for item in other:
                self.add(other)
        else:
            raise TypeError('union only takes a set or MultiSet; received {0}'.format(type(other)))


if __name__ == '__main__':
    pass