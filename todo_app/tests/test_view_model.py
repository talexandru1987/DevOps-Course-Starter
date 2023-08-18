# import sys

# print(sys.executable)

# UNIT Tests
import requests
import pytest
from .conftest import *


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
