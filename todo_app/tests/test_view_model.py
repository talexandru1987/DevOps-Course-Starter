# import sys
# print(sys.executable)

# UNIT Tests
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