import abc


class BaseContainer(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self, iterable=None):
        pass

    @property
    @abc.abstractmethod
    def _container(self):
        pass

    def __repr__(self) -> str:
        name = type(self).__name__
        contents = ', '.join([str(item) for item in self])
        return '{0}({1})'.format(name, contents)

    def __str__(self) -> str:
        return repr(self)

    def __iter__(self):
        yield from self._container

    def __len__(self) -> int:
        return len(self._container)

    def __bool__(self) -> bool:
        return len(self) > 0

    def __contains__(self, item) -> bool:
        return item in self._container

    def __eq__(self, other) -> bool:
        return isinstance(other, type(self)) and self._container == other._container

    def copy(self):
        initializer = type(self)
        return initializer((i for i in self))


if __name__ == '__main__':
    pass