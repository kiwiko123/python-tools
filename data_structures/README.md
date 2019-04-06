# Data Structures
## Overview
This folder contains data structures implemented in pure Python.

## Highlights
### Base Container
`containers.py` houses `BaseContainer`, an abstract class that provides some convenience methods for implementing other data structures,
including `__len__`, `__bool__`, and `__eq__`.

Override the `@property` `_container` to return the actual container object.
All methods (besides `__init__`) should reference and operate on `self._container`.

Example:
```python
from containers import BaseContainer

class MyList(BaseContainer):
    def __init__(self, iterable=None):
        self.__list = list(iterable)
        
    @property
    def _container(self) -> list:
        return self.__list
        
    def add_to_list(self, item) -> None:
        self._container.append(item)
``` 
In `__init__`, we initialize the _actual_ container object as `self.__list`.
We override the `_container` property to return `self.__list`.
From there on out, any time we want to operate on that underlying list, we'll do so through `self._container`.

### Queues
Inside `queues.py` lives `BaseQueue` and `PriorityQueue`.
`BaseQueue` provides an abstract class that requires the implementation of some standard queue operations, like `top`, `push`, and `pop`.

But the really cool part is `PriorityQueue` - a high-level class that implements a max-heap.

#### Why re-invent the wheel?
It's easy to mimic a priority queue in Python just by using a list, and repeatedly calling `sorted` whenever it needs order.
`sorted` is great because it takes in a unary `key` function that returns an object on which comparison is determined.
But, this isn't very efficient.

There's also the `heapq` module in the standard library, but that provides little control over custom comparators, and is a little unintuitive to use.

Wouldn't it be great if there was a high-level priority queue object that behaved the same way as `sorted`?

#### PriorityQueue
This class takes in some pretty familiar arguments:

* `iterable`: a collection of objects with which the queue should be initialized. Pretty standard across any builtin container type.
    * default: `None`
* `key`: a unary function that returns the object on which sorting criteria is determined. This behaves exactly the same way as `sorted`'s `key` parameter.
    * default: `lambda x: x` (i.e., the identity function -- compare on each object itself)
* `reverse`: if `False`, order items from greatest to least (it's a max-heap after all). If `True`, well, reverse the order!
    * default: `False`
* `greater_than`: a binary predicate that returns True if its first argument is deemed greater than its second.
    * `greater_than(a, b)` indicates `a > b`. 
    * this should probably be left alone, but it's there if you need it.
    * _this is only used when `reverse=False`_.
    * default: `operator.gt`
* `less_than`: same idea as `greater_than`, but the opposite!
    * `less_than(a, b)` indicates `a < b`.
    * this should also probably be left alone, but it's there if you need it.
    * _this is only used when `reverse=True`_.
    * default: `operator.lt`

##### Example
```python
import random
from queues import PriorityQueue

# Make a priority queue that orders numbers from least to greatest
unordered_numbers = [8, 3, 4, 1, 6, 0, 2, 7, 5]
least_to_greatest = PriorityQueue(unordered_numbers, reverse=True)
least_to_greatest.view() # this method returns a list of the items in the queue, in order
>> [0, 1, 2, 3, 4, 5, 6, 7, 8]

# Order a list of lists, by decreasing length of each nested list.
nested = [[1, 2, 3], [4], [7, 8, 9, 0], [5, 6]]
decreasing_nested_length = PriorityQueue(nested, key=lambda nested_list: len(nested_list))
decreasing_nested_length.view()
>> [[7, 8, 9, 0], [1, 2, 3], [5, 6], [4]]
```