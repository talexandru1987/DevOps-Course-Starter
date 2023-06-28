from flask import session
import requests
import os
from dotenv import load_dotenv

load_dotenv()
# globals
query = {"key": os.getenv("TRELLO_KEY"), "token": os.getenv("TRELLO_TOKEN")}
baseUrl = "https://api.trello.com/1/"


def get_boardID(name):
    searchUrl = baseUrl + "members/me/boards?fields=name"

    try:
        response = requests.request("GET", searchUrl, params=query)
        response.raise_for_status()
        response = response.json()
    except requests.exceptions.RequestException as exception:
        print(f"An error occured: {exception}")
        response = None

    if response:
        boardItem = next((obj for obj in response if obj["name"] == name), None)
        if boardItem:
            return boardItem["id"]
        else:
            return None

    return response


def get_items():
    """
    Fetches all cards from the trello board.

    Returns:
        list: The list of saved items.
    """
    return session.get("items", _DEFAULT_ITEMS.copy())
