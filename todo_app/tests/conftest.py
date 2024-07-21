import pytest
import os
from dotenv import load_dotenv, find_dotenv
from ..data.mongo_items import *
from ..data.view_model import ViewModel
from .mock_data import *
from .. import app
from datetime import datetime
from flask import current_app


@pytest.fixture(scope="module")
def app_with_context():
    file_path = find_dotenv(".env.test")
    load_dotenv(file_path, override=True)

    # Set the environment variable to use the mock database for testing
    os.environ['USE_MOCK_DB'] = 'True'

    # Disable authentication for testing
    os.environ['LOGIN_DISABLED'] = 'True'

    application = app.create_app()
    with application.app_context():
        yield application

@pytest.fixture(scope="module")
def mongo_access(app_with_context):
    with app_with_context.app_context():
        yield current_app.mongo_access

@pytest.fixture(scope="module")
def cardsCollection(mongo_access):
    return mongo_access.cardsCollection

@pytest.fixture(scope="module")
def boardsCollection(mongo_access):
    return mongo_access.boardsCollection


# Convert timestamps for mock data
def convert_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp / 1000)

@pytest.fixture(autouse=True)
def setup_database(cardsCollection, boardsCollection):
    # Clear collections before each test
    cardsCollection.delete_many({})
    boardsCollection.delete_many({})
    
    # Insert mock data with converted timestamps
    boards_data = mock_boardsCollection()
    for board in boards_data:
        board['created'] = convert_timestamp(board['created']['$date'])
    boardsCollection.insert_many(boards_data)

    cards_data = mock_cardsCollection()
    for card in cards_data:
        card['due'] = convert_timestamp(card['due']['$date'])
        card['dateLastActivity'] = convert_timestamp(card['dateLastActivity']['$date'])
    cardsCollection.insert_many(cards_data)

@pytest.fixture
def create_items(cardsCollection):
    # Convert mock card data into ViewModel items
    items = [Item.create_card(obj) for obj in cardsCollection.find()]
    return ViewModel(items)

@pytest.fixture
def client(app_with_context):
    with app_with_context.test_client() as client:
        yield client



def test_add_card(cardsCollection):
    card_name = "Test Add Card"
    list_id = "testList123"
    desc = "A test card"
    due = datetime.now()
    board = "testBoard123"
    result = add_card(list_id, card_name, desc, due, board, cardsCollection)
    assert result['_id'] is not None
    assert cardsCollection.count_documents({}) == 3  # Assuming starting with 2 cards

def test_delete_board_by_name(cardsCollection, boardsCollection):
    boardsCollection.insert_one({
        "_id": "661bd26783cc1295b454f39711",
        "name" : "Board to Delete",
        "description" : "",
        "created" :datetime.fromtimestamp(1713102967938 / 1000.0),
        "boards" : "1"
    })
    cardsCollection.insert_one({
        "_id" :"661bda5e1f5971bd6842416444",
        "listId" : "657c834ff1b03a6ddfeadc94",
        "name" : "First Item",
        "due" :datetime.fromtimestamp(1713102967938 / 1000.0),
        "dateLastActivity" : datetime.fromtimestamp(1713102967938 / 1000.0),
        "desc" : "ewqe",
        "boards" : [
            "661bd26783cc1295b454f3971"
        ]
    })
    success = delete_board_by_name("Board to Delete", cardsCollection, boardsCollection)
    assert success is True
   
def test_get_boards(boardsCollection):
    boardsCollection.insert_many([{"name": "Board1"}, {"name": "Board2"}])
    boards = get_boards(boardsCollection)
    assert len(boards) == 4

def test_update_card(cardsCollection):
    cardsCollection.insert_one({"_id": "card123", "listId": "oldList"})
    result = update_card("card123", "Done", cardsCollection)
    assert result["status"] == "success"
    updated_card = cardsCollection.find_one({"_id": "card123"})
    assert updated_card["listId"] == "Done"

def test_delete_card(cardsCollection):
    cardsCollection.insert_one({"_id": "card123"})
    result = delete_card("card123", cardsCollection)
    assert result["status"] == "success"
    assert cardsCollection.count_documents({}) == 2

