import pytest
from dotenv import load_dotenv, find_dotenv
from ..data.trello_items import Item
from ..data.view_model import ViewModel
from .. import app
import requests
import os

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
        fake_response_data = [
            {
                "id": "64fwqdffe670fca0",
                "name": "To Do",
                "closed": "false",
                "idBoard": "649984e03dwqdfe670fc99",
                "pos": 16384,
                "subscribed": "false",
                "softLimit": "null",
                "status": "null",
            },
            {
                "id": "64fwqdffe670fca0",
                "name": "Doing",
                "closed": "fake",
                "idBoard": "6dwqdwq7ffe670fc99",
                "pos": 32768,
                "subscribed": "fake",
                "softLimit": "fake",
                "status": "fake",
            },
            {
                "id": "64fwqdffe670fca0",
                "name": "Done",
                "closed": "fake",
                "idBoard": "64dqwdqwdwqf7ffe670fc99",
                "pos": 49152,
                "subscribed": "fake",
                "softLimit": "fake",
                "status": "fake",
            },
        ]
        return StubResponse(fake_response_data, status_code=200)

    elif url == f"https://api.trello.com/1/lists/{listId}/cards":
        fake_response_data = [
            {
                "id": "64fwqdffe670fca0",
                "badges": {
                    "attachmentsByType": {"trello": {"board": 0, "card": 0}},
                    "location": "fake",
                    "votes": 0,
                    "viewingMemberVoted": "fake",
                    "subscribed": "fake",
                    "fogbugz": "",
                    "checkItems": 0,
                    "checkItemsChecked": 0,
                    "checkItemsEarliestDue": "fake",
                    "comments": 0,
                    "attachments": 0,
                    "description": "fake",
                    "due": "2023-08-26T00:00:00.000Z",
                    "dueComplete": "fake",
                    "start": "fake",
                },
                "checkItemStates": [],
                "closed": "fake",
                "dueComplete": "fake",
                "dateLastActivity": "2023-08-13T09:54:19.406Z",
                "desc": "6kl67",
                "descData": {"emoji": {}},
                "due": "2023-08-26T00:00:00.000Z",
                "dueReminder": "fake",
                "email": "fake",
                "idBoard": "649984e03dadf7ffe670fc99",
                "idChecklists": [],
                "idList": "649984e03dadf7ffe670fca0",
                "idMembers": [],
                "idMembersVoted": [],
                "idShort": 29,
                "idAttachmentCover": "fake",
                "labels": [],
                "idLabels": [],
                "manualCoverAttachment": "fake",
                "name": "asdfg",
                "pos": 65536,
                "shortLink": "j2jPi3hZ",
                "shortUrl": "https://trello.com/c/j2jPi3hZ",
                "start": "fake",
                "subscribed": "fake",
                "url": "https://trello.com/c/j2jPi3hZ/29-asdfg",
                "cover": {
                    "idAttachment": "fake",
                    "color": "fake",
                    "idUploadedBackground": "fake",
                    "size": "normal",
                    "brightness": "dark",
                    "idPlugin": "fake",
                },
                "isTemplate": "fake",
                "cardRole": "fake",
            }
        ]
        return StubResponse(fake_response_data, status_code=200)

    raise Exception(f'Integration test did not expect URL "{url}"')
