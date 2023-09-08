import pytest
from dotenv import load_dotenv, find_dotenv
from ..data.trello_items import Item
from ..data.view_model import ViewModel
from .mock_data import *
from .. import app
import requests
import os

testData = mock_cards()


@pytest.fixture
def create_items():
    items = [Item.from_trello_card(obj["card"], obj["list"]) for obj in testData]
    return ViewModel(items)


@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv(".env.test")
    load_dotenv(file_path, override=True)

    # Create the new app.
    test_app = app.create_app()

    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client


class StubResponse:
    def __init__(self, fake_response_data, status_code=200):
        self.fake_response_data = fake_response_data
        self.status_code = status_code

    def json(self):
        return self.fake_response_data

    def raise_for_status(self):
        if 400 <= self.status_code < 600:
            raise requests.HTTPError(f"HTTP error occured: {self.status_code}")


# Stub replacement for requests.get(url)
def stub(method, url, **kwargs):
    assert method == "GET"
    fake_response_data = None
    boardId = "testCards"
    listId = "64fwqdffe670fca0"
    if url == f"https://api.trello.com/1/members/me/boards?fields=name":
        fake_response_data = [
            {"id": "fake7ffe670fc99", "name": "DevOps"},
            {"id": "fakec631dc72cbe0a", "name": "Live Project"},
        ]
        return StubResponse(fake_response_data, status_code=200)
    elif url == f"https://api.trello.com/1/boards/{boardId}/lists":
        fake_response_data = mock_board_lists()
        return StubResponse(fake_response_data, status_code=200)

    elif url == f"https://api.trello.com/1/lists/{listId}/cards":
        fake_response_data = mock_list_cards()
        return StubResponse(fake_response_data, status_code=200)

    raise Exception(f'Integration test did not expect URL "{url}"')
