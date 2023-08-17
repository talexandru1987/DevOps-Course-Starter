import pytest

from ..data.trello_items import Item

from ..data.view_model import ViewModel


testData = [
    {
        "card": {
            "id": "1",
            "name": "Test1",
            "dateLastActivity": "2023-08-26T00:00:00.000Z",
            "due": "2023-08-26T00:00:00.000Z",
            "desc": "card1",
        },
        "list": {"name": "To Do"},
    },
    {
        "card": {
            "id": "2",
            "name": "Test1",
            "dateLastActivity": "2023-08-26T00:00:00.000Z",
            "due": "2023-08-26T00:00:00.000Z",
            "desc": "card2",
        },
        "list": {"name": "Done"},
    },
    {
        "card": {
            "id": "3",
            "name": "Test1",
            "dateLastActivity": "2023-08-26T00:00:00.000Z",
            "due": "2023-08-26T00:00:00.000Z",
            "desc": "card3",
        },
        "list": {"name": "Doing"},
    },
    {
        "card": {
            "id": "4",
            "name": "Test1",
            "dateLastActivity": "2023-08-26T00:00:00.000Z",
            "due": "2023-08-26T00:00:00.000Z",
            "desc": "card4",
        },
        "list": {"name": "To Do"},
    },
]


@pytest.fixture
def create_items():
    items = []
    for obj in testData:
        item = Item.from_trello_card(obj["card"], obj["list"])
        items.append(item)
    return ViewModel(items)
