from pynamodb.models import Model as PynamodbModel
from pynamodbplus.models import Model


class TestModel:
    def test_parent_class(self):
        assert issubclass(Model, PynamodbModel)

    def test_default_page_size(self):
        assert Model.PAGE_SIZE == 20

    def test_default_index_priority(self):
        assert Model.INDEX_PRIORITY == ()

    def test_to_json_list(self):
        assert isinstance(Model.to_json_list, property)

    def test_to_json_detail(self):
        assert isinstance(Model.to_json_detail, property)
