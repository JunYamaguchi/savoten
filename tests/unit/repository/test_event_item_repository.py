import pytest

from savoten.domain import Candidate, EventItem, User
from savoten.repository.memory import EventItemRepository
from tests.util import get_public_vars

user_args = {
    'name': 'test_user',
    'email': 'test_user@test.com',
    'permission': 100
}
user = User(**user_args)
candidate_args = {'user': user}
candidate = Candidate(**candidate_args)


class TestSave:

    @pytest.fixture(scope='function')
    def setup_repository(self):
        event_item_repository = EventItemRepository()
        yield (event_item_repository)
        del (event_item_repository)

    @pytest.mark.parametrize('event_item',
                             [EventItem('test_name', [candidate])])
    def test_succeeds_if_event_item_has_no_id(self, event_item,
                                              setup_repository):
        event_item_repository = setup_repository
        event_item_repository.save(event_item)
        assert get_public_vars(
            event_item_repository.event_items[1]) == get_public_vars(event_item)

    @pytest.mark.parametrize('event_item',
                             [EventItem('test_name', [candidate], id=3)])
    def test_update_succeeds_if_event_item_has_id(self, event_item,
                                                  setup_repository):
        event_item_repository = setup_repository
        event_item_repository.save(event_item)
        event_item.name = 'updated_name'
        event_item_repository.save(event_item)
        assert get_public_vars(
            event_item_repository.event_items[3]) == get_public_vars(event_item)


class TestDelete:

    @pytest.fixture(scope='function')
    def setup_repository(self):
        event_item_repository = EventItemRepository()
        yield (event_item_repository)
        del (event_item_repository)

    @pytest.mark.parametrize('event_item',
                             [EventItem('test_name', [candidate], id=1)])
    def test_succeeds_if_event_item_exists(self, event_item, setup_repository):
        event_item_repository = setup_repository
        event_item_repository.event_items[1] = event_item
        event_item_repository.delete(event_item)

    @pytest.mark.parametrize('event_item',
                             [EventItem('test_name', [candidate], id=1)])
    def test_return_value_error_if_event_item_id_is_none(
            self, event_item, setup_repository):
        event_item_repository = setup_repository
        event_item_repository.event_items[1] = event_item
        event_item.id = None
        with pytest.raises(ValueError):
            assert event_item_repository.delete(event_item)

    @pytest.mark.parametrize('event_item',
                             [EventItem('test_name', [candidate], id=1)])
    def test_return_value_error_if_event_item_does_not_exist(
            self, event_item, setup_repository):
        event_item_repository = setup_repository
        with pytest.raises(ValueError):
            assert event_item_repository.delete(event_item)


class TestFindById:

    @pytest.fixture(scope='function')
    def setup_repository(self):
        event_item_repository = EventItemRepository()
        yield (event_item_repository)
        del (event_item_repository)

    @pytest.mark.parametrize('event_item',
                             [EventItem('test_name', [candidate], id=1)])
    def test_return_event_item_if_id_exists(self, event_item, setup_repository):
        event_item_repository = setup_repository
        event_item_repository.event_items[1] = event_item
        found_event_item = event_item_repository.find_by_id(1)
        assert get_public_vars(found_event_item) == get_public_vars(
            event_item_repository.event_items[1])

    def test_return_none_if_id_does_not_exist(self, setup_repository):
        event_item_repository = setup_repository
        found_event_item = event_item_repository.find_by_id(100)
        assert found_event_item is None


class TestFindByEventId:

    @pytest.fixture(scope='function')
    def setup_and_add_event_items_to_repository(self):
        event_item_repository = EventItemRepository()
        event_item = EventItem('test_name', [candidate])
        added_event_items = []
        for i in range(1, 5):
            event_item.id = i
            event_item.event_id = 1
            event_item_repository.event_items[i] = event_item
            added_event_items.append(event_item)
        return (event_item_repository, added_event_items)

    def test_return_found_event_items_if_event_id_exists(
            self, setup_and_add_event_items_to_repository):
        event_item_repository, added_event_items = \
            setup_and_add_event_items_to_repository
        found_event_items = event_item_repository.find_by_event_id(1)
        assert set(found_event_items) == set(added_event_items)

    def test_return_empty_list_if_event_item_does_not_exist(
            self, setup_and_add_event_items_to_repository):
        event_item_repository, _ = setup_and_add_event_items_to_repository
        found_event_items = event_item_repository.find_by_event_id(2)
        assert len(found_event_items) == 0
