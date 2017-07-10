# These 'contract condition' decorators are inspired by the proposed addition of contracts in C++17.
# 
# These decorators allow easy, readable type management - 
# they eliminate the following semi-common Python idioms that tend to be present at the top of many functions:
#
#   if not type(x) is ...   # or. if not isinstance(x, ...):
#       raise TypeError(...)
#
# Intuitive contract conditions promote more readable, maintanable Python code -
# an aspect of the language that is quite commonly criticized,
# especially since a large amount of Python programmers do not take advantage of 3.x's function argument annotations.
#
# Author: Geoffrey Ko (2017)
import abc
import inspect


class _ContractCondition(metaclass=abc.ABCMeta):
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

    def check_condition(self, *args, **kwargs):
        if not self._condition(*args, **kwargs):
            msg = self._msg
            if not self._msg:
                msg = '@{0}: arguments *{1}, **{2} failed to meet expected condition'.format(type(self).__name__, args, kwargs)
            raise self._exc(msg)


class expects(_ContractCondition):
    """ Function decorator.
        Examines and places a contract on the decorated function's arguments.
        Raises an exception if such condition is not met.
        e.g.,
        @expects(lambda a, b: type(a) is int and type(b) is int)
        def add(a, b):
          return a + b
    """
    def __init__(self, condition: callable, exception=AssertionError, msg='', args=True, instance=False):
        """
        Default arguments affecting the condition function's parameter structure:
         * set args=True to accept all of the decorated callable's recognized arguments in the condition (default).
         * set instance=True to accept the object that the decorated bound method is operating on ('self' parameter).
         * set args=True, instance=False to accept all arguments after the decorated method's 'self' parameter.
         * set args=False, instance=True to accept only the passed instance as the condition function's sole argument.
         * args and instance cannot both be False.
         * raises ValueError in the event of an illegal combination.
        """
        self._args = args
        self._instance = instance
        super().__init__(condition, exception=exception, msg=msg)

    def __call__(self, function: callable):
        def _interceptor(*args, **kwargs):
            is_method = self._is_method(function, *args)
            if self._instance and not is_method:
                raise ValueError('instance=True but decorated callable {0} is not a bound method'.format(function))

            if self._args:
                check = args
                if is_method and not self._instance:
                    check = args[1:]
            elif self._instance:
                if is_method:
                    check = args[0]
            else:
                raise ValueError('neither args nor instance are True; logic states zero arguments')

            self.check_condition(*check, **kwargs)
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
        Examines and places a contract on the return value of the decorated function.
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