from pynamodb.models import Model as PynamodbModel


class Model(PynamodbModel):
    PAGE_SIZE = 20
    INDEX_PRIORITY = ()

    @property
    def to_json_list(self):
        raise NotImplementedError

    @property
    def to_json_detail(self):
        raise NotImplementedError

    @classmethod
    def _paginate(cls, query, page_size):
        items = []
        next_page = None
        for page in range(page_size):
            try:
                obj = query.next()
            except StopIteration:
                break
            items.append(obj.to_json_list)
            next_page = query.last_evaluated_key

        response = {
            "items": items,
            "next_page": next_page,
        }
        return response

    @classmethod
    def _filter_priority_setup(cls, conditions):
        main_index = None
        hash_key = None
        range_key_condition = None

        # Identifies the hash and range key based on the highest priority index.
        for index in cls.INDEX_PRIORITY:
            hash_attr = index._hash_key_attribute()

            if hash_attr.attr_name in conditions.keys():
                main_index = index

                hash_condition = conditions[hash_attr.attr_name]
                hash_type = hash_condition.values[1].short_attr_type
                hash_key = hash_condition.values[1].value[hash_type]

                # Since this condition has already been defined as hash_key,
                # we can remove it from the conditions list.
                del conditions[hash_attr.attr_name]

                main_index_attrs = main_index._get_attributes().values()

                try:
                    range_attr = next(
                        filter(lambda obj: obj.is_range_key, main_index_attrs)
                    )
                except StopIteration:
                    # It menas the main index does not have a sort key.
                    # So, we can go foward.
                    return main_index, hash_key, range_key_condition, conditions

                range_key_condition = conditions.get(range_attr.attr_name, None)
                # Since this condition has already been defined as range_key,
                # we can remove it from the conditions list.
                if range_key_condition is not None:
                    del conditions[range_attr.attr_name]

                return main_index, hash_key, range_key_condition, conditions

        return main_index, hash_key, range_key_condition, conditions

    @classmethod
    def filter(cls, conditions, last_evaluated_key=None, page_size=None):
        (
            main_index,
            hash_key,
            range_key_condition,
            conditions,
        ) = cls._filter_priority_setup(conditions)
        page_size = page_size or cls.PAGE_SIZE
        filter_condition = None

        for condition in conditions.values():
            if filter_condition is None:
                filter_condition = condition
            else:
                filter_condition &= condition

        if main_index:
            query = main_index.query(
                hash_key,
                range_key_condition=range_key_condition,
                filter_condition=filter_condition,
                last_evaluated_key=last_evaluated_key,
            )
        else:
            query = cls.scan(
                filter_condition=filter_condition,
                last_evaluated_key=last_evaluated_key,
            )
        return cls._paginate(query, page_size=page_size)

    @classmethod
    def all(cls, last_evaluated_key=None, page_size=None):
        page_size = page_size or cls.PAGE_SIZE

        query = cls.scan(last_evaluated_key=last_evaluated_key)
        return cls._paginate(query, page_size=page_size)

    @classmethod
    def detail(cls, hash_value, range_value=None):
        instance = cls.get(hash_value, range_key=range_value)
        return instance.to_json_detail
