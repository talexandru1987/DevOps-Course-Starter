# import sys
# print(sys.executable)

# UNIT Tests
import requests
from .conftest import *
from datetime import datetime


def test_view_model_done_property(create_items):
    # arrange
    testModel = create_items

    # act
    orderedList = testModel.done_items

    # assert
    # assert orderedList, "list is empty"
    assert all(
        item.status == "Done" for item in orderedList
    ), "Not all items have a status of Done"


def test_view_model_to_do_property(create_items):
    # arrange
    testModel = create_items

    # act
    orderedList = testModel.todo_items

    # assert
    # assert orderedList, "list is empty"
    assert all(
        item.status == "To Do" for item in orderedList
    ), "Not all items have a status of To Do"


def test_view_model_doing_property(create_items):
    # arrange
    testModel = create_items

    # act
    orderedList = testModel.doing_items

    # assert
    # assert orderedList, "list is empty"
    assert all(
        item.status == "Doing" for item in orderedList
    ), "Not all items have a status of Doing"


def test_recent_done_items(create_items):
    # arrange
    testModel = create_items
    # act
    orderedList = testModel.recent_done_items
    today_date = datetime.now().date().strftime("%d/%m/%y")
    # assert
    assert all(
        item.status == "Done" and item.date == today_date for item in orderedList
    ), "Not all items have a status of Done and today's date"


def test_older_done_items(create_items):
    # arrange
    testModel = create_items
    # act
    orderedList = testModel.older_done_items

    today_date = datetime.now().date().strftime("%d/%m%y")
    # assert
    assert all(
        item.status == "Done" and item.date != today_date for item in orderedList
    ), "Not all items have a status of Done and older than today's date"


# Integration Tests
def test_index_page(monkeypatch, client):
    # Replace requests.get(url) with our own function
    monkeypatch.setattr(requests, "request", stub)

    # Make a request to our app's index page
    response = client.get("/")

    assert response.status_code == 200
    assert "DevOps" in response.data.decode()
    assert "fakec631dc72cbe0a" in response.data.decode()


def test_cards_page(monkeypatch, client):
    # Replace requests
    id = "testCards"
    monkeypatch.setattr(requests, "request", stub)

    # Make a request
    response = client.get(f"/{id}")

    assert response.status_code == 200
    assert "64fwqdffe670fca0" in response.data.decode()
