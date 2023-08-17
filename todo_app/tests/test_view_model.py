# import sys

# print(sys.executable)


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
