import abc
import copy
import functools
import inspect


class const:
    """ Instance method decorator.
        Raises AttributeError upon calling the decorated method
        if it modifies the object's state.
    """
    def __init__(self, method: callable):
        if not callable(method):
            raise TypeError('expected callable method object; received {0}'.format(method))
        self._method = method

    def __repr__(self) -> str:
        return '{0}({1})'.format(self.__class__.__name__, self._method)

    def __str__(self) -> str:
        return 'const_method({0})'.format(self._method.__name__)

    def __get__(self, instance, owner):
        """ Binds instance as the first argument to __call__ """
        return functools.partial(self.__call__, instance)

    def __call__(self, *args, **kwargs):
        if not (args and hasattr(args[0], self._method.__name__)):
            raise ValueError('expected bound instance method; received {0}'.format(self._method))
        instance = args[0]
        state = copy.deepcopy(instance.__dict__)
        result = self._method(*args, **kwargs)

        if instance.__dict__ != state:
            raise AttributeError('{0} attempted to modify object {1}'.format(self._method, instance))

        return result



class _ContractCondition:
    def __init__(self, condition: callable, exception=AssertionError, msg=''):
        self._condition = condition
        self._exc = exception
        self._msg = msg

    def __repr__(self) -> str:
        return '{0}({1}, exception={2}, msg={3})'.format(type(self).__name__, self._condition, self._exc, self._msg)

    def __str__(self) -> str:
        return repr(self)

    @abc.abstractmethod
    def __call__(self, function: callable):
        pass

    @property
    def condition(self) -> callable:
        """ Access the condition function """
        return self._condition

    @condition.setter
    def condition(self, new_condition: callable) -> None:
        """ Update to new condition """
        self._condition = new_condition

    def check_condition(self, *args, **kwargs):
        if not self._condition(*args, **kwargs):
            if not self._msg:
                self._msg = '@{0}: arguments {1}, {2} failed to meet expected condition'.format(type(self).__name__, args, kwargs)
            raise self._exc(self._msg)



class expects(_ContractCondition):
    """ Function decorator.
        Examines and places a contract expects on the decorated function's arguments.
        Raises an exception if such condition is not met.

        e.g.,
        @expects(lambda a, b: type(a) is int and type(b) is int)
        def add(a, b):
          return a + b

        When decorating a bound instance method, the condition function must omit the 'self' argument.
        e.g.,
        @expects(lambda a: a > 0)      # not @expects(lambda self, a: a > 0)
        def update(self, value):
            self._value = value
    """
    def __init__(self, condition: callable, exception=AssertionError, msg=''):
        super().__init__(condition, exception, msg)

    def __call__(self, function):
        def _interceptor(*args, **kwargs):
            if self._is_method(function, *args):
                self.check_condition(*(args[1:]), **kwargs)
            else:
                self.check_condition(*args, **kwargs)

            return function(*args, **kwargs)

        _interceptor.__name__ = function.__name__
        return _interceptor

    @staticmethod
    def _is_method(function: callable, *args) -> bool:
        """ Returns True if the decorated function is a method;
            examines args to see if the first argument is an object,
            and checks if function is a member of that object.
        """
        if args:
            instance = args[0]
            member = getattr(instance, function.__name__, None)
            return member is not None and inspect.ismethod(member)
        return False


class ensures(_ContractCondition):
    """ Function decorator.
        Examines and places a contract ensures on the return value of the decorated function.
        Raises an exception if such condition is not met.
        Condition function must take 1 parameter only (representing the return value of the decorated function).

        e.g.,
        @ensures(lambda r: r > 10)
        def add(a, b):
          return a + b
    """
    def __init__(self, condition: callable, exception=AssertionError, msg=''):
        signature = inspect.signature(condition)
        if len(signature.parameters) != 1:
            raise ValueError('condition function takes exactly 1 parameter (representing the returned result of the decorated function); received {0}'.format(len(signature.parameters)))
        super().__init__(condition, exception, msg)

    def __call__(self, function):
        def _interceptor(*args, **kwargs):
            result = function(*args, **kwargs)
            self.check_condition(result)
            return result

        _interceptor.__name__ = function.__name__
        return _interceptor



if __name__ == '__main__':
    pass