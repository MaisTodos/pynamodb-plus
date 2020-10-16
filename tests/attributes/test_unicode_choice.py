import pytest
from pynamodb.attributes import UnicodeAttribute
from pynamodb.models import Model
from pynamodbplus.attributes import UnicodeChoiceAttribute


class TestUnicodeChoiceAttribute:
    def test_parent_class(self):
        assert issubclass(UnicodeChoiceAttribute, UnicodeAttribute)

    def test_default_choices(self):
        attr = UnicodeChoiceAttribute
        assert attr.choices == []

    def test_init(self):
        attr = UnicodeChoiceAttribute(choices=["foo", "bar"])
        assert attr.choices == ["foo", "bar"]

    def test_set(self):
        class UnicodeChoiceModel(Model):
            unicode_choice = UnicodeChoiceAttribute(choices=["foo", "bar"])

        instance = UnicodeChoiceModel()
        with pytest.raises(ValueError) as err:
            instance.unicode_choice = "dummy"

        assert err.value.args[0] == "Invalid choice: 'dummy'"
