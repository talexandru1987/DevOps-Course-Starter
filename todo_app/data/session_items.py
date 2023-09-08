from flask import session


def save_board_id(id):
    """
    Saved the board id to the session item.

    Returns:
       The saved id.
    """
    session["boardID"] = id

    return id


def save_board_lists(boardLists):
    """
    Saved the lists attached to the current board to current session.

    Returns:
       The saved id.
    """
    session["boardLists"] = boardLists

    return boardLists
