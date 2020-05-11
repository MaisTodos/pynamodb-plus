from datetime import datetime

import pytest
from pynamodb.attributes import Attribute
from pynamodb.constants import STRING
from pynamodb.models import Model
from pynamodbplus.attributes import TimestampAttribute


class TestTimestampAttribute:
    def test_parent_class(self):
        assert issubclass(TimestampAttribute, Attribute)

    def test_attr_type(self):
        assert TimestampAttribute.attr_type == STRING

    def test_multiplier(self):
        assert TimestampAttribute._multiplier == 1000000.0


class TestTimestampAttributeInstance:
    utc_now = datetime.utcnow()
    timestamp_as_str = str(
        int(datetime.timestamp(utc_now) * TimestampAttribute._multiplier)
    )

    def test_deserializer(self):
        assert TimestampAttribute().deserialize(self.timestamp_as_str) == self.utc_now

    def test_set_method(self):
        class TimestampModel(Model):
            timestamp = TimestampAttribute(default_for_new=self.utc_now)

        timestamp_obj = TimestampModel()
        assert timestamp_obj.timestamp == self.timestamp_as_str

    def test_set_method_with_invalid_type(self):
        class TimestampModel(Model):
            timestamp = TimestampAttribute(default_for_new="1589162296560056")

        with pytest.raises(TypeError) as err:
            TimestampModel()

        assert err.value.args[0] == "Invalid type, datetime expected: '<class 'str'>'"
