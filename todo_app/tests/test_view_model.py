# import sys
# print(sys.executable)

# UNIT Tests
from .conftest import *
from datetime import datetime
from todo_app.data.mongo_items import get_boards, get_cards
from bson.objectid import ObjectId



def test_view_model_done_property(create_items):
    # arrange
    testModel = create_items

    # act
    orderedList = testModel.done_items

    # assert
    # assert orderedList, "list is empty"
    assert all(
        item.listName == "Done" for item in orderedList
    ), "Not all items have a status of Done"


def test_view_model_to_do_property(create_items):
    # arrange
    testModel = create_items
    # act
    orderedList = testModel.todo_items

    # assert
    # assert orderedList, "list is empty"
    assert all(
        item.listName == "To Do" for item in orderedList
    ), "Not all items have a status of To Do"


def test_view_model_doing_property(create_items):
    # arrange
    testModel = create_items

    # act
    orderedList = testModel.doing_items

    # assert
    # assert orderedList, "list is empty"
    assert all(
        item.listName == "Doing" for item in orderedList
    ), "Not all items have a status of Doing"


def test_recent_done_items(create_items):
    # arrange
    testModel = create_items
    # act
    orderedList = testModel.recent_done_items
    today_date = datetime.now().date().strftime("%d/%m/%y")
    # assert
    assert all(
        item.listName == "Done" and item.date == today_date for item in orderedList
    ), "Not all items have a status of Done and today's date"


def test_older_done_items(create_items):
    # arrange
    testModel = create_items
    # act
    orderedList = testModel.older_done_items

    today_date = datetime.now().date().strftime("%d/%m%y")
    # assert
    assert all(
        item.listName == "Done" and item.date != today_date for item in orderedList
    ), "Not all items have a status of Done and older than today's date"


# # Integration Tests
# def test_index_page(monkeypatch, client):

#    # Mocked response that looks like MongoDB output
#     mocked_response = [{
#         '_id': '661bd26783cc1295b454f321',
#         'name': 'Test Integration',
#         'description': '',
#         'created': datetime(2024, 4, 14, 13, 56, 7, 938000),
#         'boards': '1'
#     }]
    

#     # Function to replace the actual database call
#     def mock_get_boards():
        
#         return mocked_response
    
#     # Replace the get_boards function with mock data
#     monkeypatch.setattr('todo_app.data.mongo_items.get_boards', mock_get_boards)

#     # Make a request to app's index page
#     response = client.get("/")

#     # Assert the status code
#     assert response.status_code == 200

#     # Decode the response data and assert the contents
#     data = response.data.decode()
#     assert "Test Integration" in data
#     assert "661bd26783cc1295b454f321" in data


# def test_cards_page(monkeypatch, client):
#     # Mock response simulating the MongoDB documents
#     mock_response = [
#         {
#             '_id': ObjectId(),
#             'listId': '657c834ff1b03a6ddfeadc94',
#             'name': 'Integration Item 1',
#             'due': datetime(2024, 4, 17, 0, 0),
#             'dateLastActivity': datetime(2024, 4, 14, 14, 30, 6, 532000),
#             'desc': 'ewqe',
#             'boards': ['661bd26783cc1295b454f321']
#         },
#         {
#             '_id': ObjectId(),
#             'listId': '657c834ff1b03a6ddfeadc93',
#             'name': 'Integration Item 2',
#             'due': datetime(2024, 4, 22, 0, 0),
#             'dateLastActivity': datetime(2024, 4, 22, 17, 37, 59, 557000),
#             'desc': 'w',
#             'boards': ['661bd26783cc1295b454f321']
#         }
#     ]

#     # Function to replace the actual database call
#     def mock_get_cards():
#         # Assume Item.create_card() and ViewModel are properly defined somewhere in your application
#         cards = [Item.create_card(obj) for obj in mock_response]
#         return ViewModel(cards)

#     # Replace the get_cards function with mock data
#     monkeypatch.setattr('todo_app.data.mongo_items.get_cards', mock_get_cards)

#     # Simulate a GET request to the specific route
#     response = client.get("/testCards")

#     # Assertions to check if the status code and the body of the response are as expected
#     assert response.status_code == 200
#     assert 'Integration Item 1' in response.data.decode()