import abc


class BaseContainer(metaclass=abc.ABCMeta):
    """
    An abstract class providing some default convenience methods (__len__, __bool__, __eq__, etc.).
    Override the @property _container to return the actual underlying container object.
    Example:
    ```
    class MyList(BaseContainer):
        def __init__(self, iterable=None):
            self.__list = list(iterable)

        @property
        def _container(self) -> list:
            return self.__list
    ```
    No other method besides __init__ should reference the self.__list property;
    all other methods should operate on self._container.
    """

    @abc.abstractmethod
    def __init__(self, iterable=None):
        pass

    @property
    @abc.abstractmethod
    def _container(self):
        """
        This property represents the data structure on which derived classes can operate.
        All methods (outside of __init__) should operate on this property.
        """
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