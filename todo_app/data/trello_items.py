import requests
import os
from dotenv import load_dotenv
from datetime import datetime, date

load_dotenv()
# globals
query = {"key": os.getenv("TRELLO_KEY"), "token": os.getenv("TRELLO_TOKEN")}
baseUrl = "https://api.trello.com/1/"
headers = {"Accept": "application/json"}


class Item:
    def __init__(self, id, name, date, status="To Do"):
        self.id = id
        self.name = name
        self.status = status
        self.date = date

    @classmethod
    def from_trello_card(cls, card, list):
        date = datetime.strptime(card["dateLastActivity"], "%Y-%m-%dT%H:%M:%S.%fZ")
        return cls(card["id"], card["name"], date.strftime("%d/%m/%y"), list["name"])


# get boards avaialble to the user
def get_boards():
    searchUrl = baseUrl + "members/me/boards?fields=name"

    try:
        response = requests.request("GET", searchUrl, headers=headers, params=query)
        response.raise_for_status()
        response = response.json()
    except requests.exceptions.RequestException as exception:
        print(f"An error occured: {exception}")
        response = None
    return response


# get the cards in a list
def get_list_cards(id):
    searchUrl = baseUrl + f"lists/{id}/cards"

    try:
        response = requests.request("GET", searchUrl, headers=headers, params=query)
        response.raise_for_status()
        response = response.json()
    except requests.exceptions.RequestException as exception:
        print(f"An error occured: {exception}")
        response = None
    return response


# get the lists on  board
def get_boardLists(id):
    searchUrl = f"{baseUrl}boards/{id}/lists"

    try:
        response = requests.request("GET", searchUrl, headers=headers, params=query)
        response.raise_for_status()
        response = response.json()
    except requests.exceptions.RequestException as exception:
        print(f"An error occured: {exception}")
        response = None

    return response


# get cards on a board
def get_cards(id):
    classItems = []
    found = False

    try:
        # get all lists for the board
        boardLists = get_boardLists(id)

        # get the cards for each list
        if len(boardLists) > 0:
            for obj in boardLists:
                cardsList = get_list_cards(obj["id"])
                for cardList in cardsList:
                    # if classItems is empty code will not execute so need an if
                    for card in classItems:
                        if cardList["id"] == card.id:
                            found = True
                            break
                        else:
                            found = False
                    if found == False:
                        date = datetime.strptime(
                            cardList["dateLastActivity"], "%Y-%m-%dT%H:%M:%S.%fZ"
                        )
                        # create the class items
                        item = Item.from_trello_card(cardList, obj)
                        classItems.append(item)
    except requests.exceptions.RequestException as exception:
        print(f"An error occured: {exception}")
        classItems = []
    return classItems


# add a new card to the board
def add_card(listId, cardName):
    searchUrl = baseUrl + "cards"

    addQuery = {
        "key": os.getenv("TRELLO_KEY"),
        "token": os.getenv("TRELLO_TOKEN"),
        "idList": listId,
        "name": cardName,
    }
    try:
        response = requests.request("POST", searchUrl, headers=headers, params=addQuery)
        response.raise_for_status()
        response = response.json()
    except requests.exceptions.RequestException as exception:
        print(f"An error occured: {exception}")
        response = False

    return response


# update a card on the board
def update_card(cardId, listId):
    searchUrl = baseUrl + f"cards/{cardId}"

    addQuery = {
        "key": os.getenv("TRELLO_KEY"),
        "token": os.getenv("TRELLO_TOKEN"),
        "idList": listId,
    }
    try:
        response = requests.request("PUT", searchUrl, headers=headers, params=addQuery)
        response.raise_for_status()
        response = response.json()
    except requests.exceptions.RequestException as exception:
        print(f"An error occured: {exception}")
        response = False

    return response


# update a card on the board
def delete_card(cardId):
    searchUrl = baseUrl + f"cards/{cardId}"

    try:
        response = requests.request("DELETE", searchUrl, params=query)
        response.raise_for_status()
        response = response.json()
    except requests.exceptions.RequestException as exception:
        print(f"An error occured: {exception}")
        response = False

    return response
