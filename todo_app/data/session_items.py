from flask import session


def save_board_id(id):
    """
    Saved the board id to the session item.

    Returns:
       The saved id.
    """
    session["boardID"] = id

    return id


def save_board_lists(id):
    """
    Saved the board id to the session item.

    Returns:
       The saved id.
    """
    session["boardLists"] = id

    return id
