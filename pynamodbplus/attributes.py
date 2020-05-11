from datetime import datetime
from typing import Any

from pynamodb.attributes import Attribute
from pynamodb.constants import STRING


class TimestampAttribute(Attribute):
    """
    PynamoDB attribute for timestamp in microseconds.

    >>> class MyModel(Model):
    >>>   timestamp = TimestampAttribute(default_for_new=datetime.utcnow)
    """

    attr_type = STRING
    _multiplier = 1000000.0

    def deserialize(self, value: str) -> datetime:
        """
        Deserialize timestamp in microseconds into datetime.
        """
        return datetime.fromtimestamp(int(value) / self._multiplier)

    def __set__(self, instance: Any, value: datetime) -> None:
        if type(value) is not datetime:
            raise TypeError(f"Invalid type, datetime expected: '{type(value)}'")
        serialized_value = str(int(datetime.timestamp(value) * self._multiplier))
        return super().__set__(instance, serialized_value)
