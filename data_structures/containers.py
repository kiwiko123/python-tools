import abc


class BaseContainer(metaclass=abc.ABCMeta):

    @property
    @abc.abstractmethod
    def _container(self):
        pass

    @abc.abstractmethod
    def __len__(self) -> int:
        pass

    @abc.abstractmethod
    def __iter__(self):
        pass

    def __bool__(self) -> bool:
        return len(self) > 0

    def __contains__(self, item) -> bool:
        return item in self._container

    def __eq__(self, other) -> bool:
        return isinstance(other, type(self)) and self._container == other._container

    def copy(self, deep=False):
        if deep:
            initializer = type(self)
            return initializer((i for i in self))
        else:
            return self


if __name__ == '__main__':
    pass