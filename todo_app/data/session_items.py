from flask import session


def save_board_id(id):
    """
    Saved the board id to the session item.

    Returns:
       The saved id.
    """
    session["boardID"] = id

    return id
