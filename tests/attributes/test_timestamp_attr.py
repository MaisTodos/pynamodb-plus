from datetime import datetime

from pynamodb.constants import STRING
from pynamodb.models import Model
from pynamodbplus.attributes import TimestampAttribute


class TimestampModel(Model):
    timestamp = TimestampAttribute(default_for_new=lambda: datetime(2020, 1, 1))


class TestTimestampAttribute:
    instance = TimestampModel()

    def test_attr_type(self):
        assert TimestampAttribute().attr_type == STRING

    def test_multiplier(self):
        assert TimestampAttribute()._multiplier == 1000000.0

    def test_deserialize(self):
        assert TimestampAttribute().deserialize("1577847600000000") == datetime(
            2020, 1, 1
        )

    def test_set_method(self):
        assert self.instance.timestamp == "1577847600000000"
