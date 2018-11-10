# These 'contract condition' decorators are inspired by the proposed addition of contracts in C++17.
# 
# These decorators allow easy, readable type management
# by eliminating the following semi-common Python idioms that tend to be present at the top of many functions:
#
#   if not type(x) is ...   # or. if not isinstance(x, ...):
#       raise TypeError(...)
#
# Intuitive contract conditions promote more readable, maintanable Python code.
#
# Author: Geoffrey Ko (2017)
import abc
import inspect


class _ContractCondition(metaclass=abc.ABCMeta):
    def __init__(self, condition: callable, exception=AssertionError, msg=''):
        self._condition = condition
        self._exception = exception
        self._msg = msg

    def __repr__(self) -> str:
        return '{0}({1}, exception={2}, msg={3})'.format(type(self).__name__, self._condition, self._exception, self._msg)

    def __str__(self) -> str:
        return repr(self)

    @abc.abstractmethod
    def __call__(self, function: callable):
        pass

    def check_condition(self, *args, **kwargs) -> None:
        if not self._condition(*args, **kwargs):
            msg = self._msg
            if not self._msg:
                msg = '@{0}: arguments ({1}, {2}) failed to meet expected condition'.format(type(self).__name__, args, kwargs)
            raise self._exception(msg)

    def check_number_of_arguments(self, function: callable, expected: int) -> None:
        actual = self.get_number_of_arguments(function)
        if actual != expected:
            message = "Expected {0} arguments; received {1}. If you're decorating a method, did you include `self`?".format(expected, actual)
            raise self._exception(message)

    @staticmethod
    def get_number_of_arguments(function: callable) -> int:
        signature = inspect.signature(function)
        return len(signature.parameters)


class expects(_ContractCondition):
    """ Function/method decorator.
        Examines and places a pre-condition contract on the decorated function's arguments.
        Raises an exception if such condition is not met.
        The condition function must take the same number of arguments as the decorated function.
        ----------
        @expects(lambda a, b: type(a) is int and type(b) is int)
        def add(a, b):
          return a + b

        When decorating an instance method, you must include an argument for `self`.
        ----------
        class Foo:
            @expects(lambda a, b: b > 5)    # here, `a` corresponds to `self`, and `b` corresponds to `x`
            def bar(self, x):
                pass
    """
    def __init__(self, condition: callable, exception=AssertionError, msg=''):
        super().__init__(condition, exception=exception, msg=msg)

    def __call__(self, function: callable):
        number_of_arguments = self.get_number_of_arguments(function)
        self.check_number_of_arguments(self._condition, number_of_arguments)

        def _interceptor(*args, **kwargs):
            self.check_condition(*args, **kwargs)
            return function(*args, **kwargs)

        _interceptor.__name__ = function.__name__
        return _interceptor


class ensures(_ContractCondition):
    """ Function/method decorator.
        Examines and places a post-condition contract on the return value of the decorated function.
        Raises an exception if such condition is not met.
        The condition function must take exactly 1 argument, representing the return value of the decorated function.
        ----------
        @ensures(lambda x: x > 10)
        def add(a, b):
          return a + b
    """
    def __init__(self, condition: callable, exception=AssertionError, msg=''):
        self.check_number_of_arguments(condition, 1)
        super().__init__(condition, exception=exception, msg=msg)

    def __call__(self, function: callable):
        def _interceptor(*args, **kwargs):
            result = function(*args, **kwargs)
            self.check_condition(result)
            return result

        _interceptor.__name__ = function.__name__
        return _interceptor


if __name__ == '__main__':
    pass