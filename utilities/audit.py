import collections
import datetime


_PRIMITIVE_TYPES = {int, float, bool, str}


class UpdateHistory:
    def __init__(self, attribute: str, value, time_of_update: datetime.datetime):
        self.attribute = attribute
        self.value = value
        self.time_of_update = time_of_update

    def __repr__(self) -> str:
        return "{0}(attribute='{1}', value={2}, time_of_update={3})".format(
            type(self).__name__,
            self.attribute,
            self.value,
            self.time_of_update
        )

    def __str__(self) -> str:
        return repr(self)



class Recordable:
    """
    A base class used to monitor, track, and audit an object's history.
    Deriving a class from Recordable will allow all updates to its properties to be recorded and stored.
    Update times are captured in UTC.

    Recordable.__init__(self) MUST be the very first step that happens in the derived class' __init__ method.
    """
    _whitelisted_fields = {
        '_whitelisted_fields',
        '_history',
        '_recordable_types',
        '_size'
    }


    def __init__(self, recordable_types=_PRIMITIVE_TYPES):
        """
        recorded_types is a container of types that are to be recorded.
        If None, record all values.
        If empty, record no values.

        Recordable.__init__(self) MUST be the very first step that happens in the derived class' __init__ method.
        """
        self._history = collections.OrderedDict()
        self._recordable_types = recordable_types
        self._size = 0


    @property
    def recordable_types(self) -> {type}:
        return self._recordable_types


    @recordable_types.setter
    def recordable_types(self, new_recordable_types: {type}) -> None:
        self._recordable_types = new_recordable_types


    def __setattr__(self, name: str, value):
        super().__setattr__(name, value)
        if name not in self._whitelisted_fields:
            value_to_record = value if self.should_record_value(value) else None
            self._update(name, value_to_record)
            self._size += 1


    def last_modification(self) -> UpdateHistory:
        """
        Returns the last update that occurred, or None if there haven't been any.
        """
        return self._history[-1] if self._history else None


    def diff_count(self) -> int:
        """
        Returns the total number of updates that have been captured so far.
        """
        return self._size


    def timeline(self, ascending=True) -> [UpdateHistory]:
        """
        Returns a one-dimensional list of all updates that have been captured, ordered by time-of-update.
        If ascending=True, order the list from least-recent to most-recent update.
        Otherwise, order from most-recent to least-recent.
        """
        updates = []
        for records in self._history.values():
            updates.extend(records)

        return sorted(updates, key=lambda update: update.time_of_update, reverse=not ascending)


    def report(self) -> {str: [UpdateHistory]}:
        """
        Returns a dictionary whose keys are string attribute fields,
        and values are a list of updates that those fields have gone through.
        """
        return dict(self._history)


    def should_record_value(self, value) -> bool:
        """
        Override this method to determine what values should be recorded.
        By default, it will ensure that the value's type is in the recorded_types container with which the object was initialized.
        Return True if the value should be recorded, or False if not.
        If a value should not be recorded, its attribute and time will still be captured. Only the actual value will be skipped.
        """
        return self.recordable_types is None or type(value) in self.recordable_types


    def _update(self, attribute: str, value) -> None:
        """
        Given the attribute and value passed into __setattr__,
        process and record this update.
        """
        time_of_update = datetime.datetime.utcnow()
        update = UpdateHistory(attribute, value, time_of_update)

        if attribute in self._history:
            updates = self._history[attribute]
            if updates and updates[-1].value != value:
                self._history[attribute].append(update)
        else:
            self._history[attribute] = [update]


if __name__ == '__main__':
    pass
