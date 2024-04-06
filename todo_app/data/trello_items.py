import requests
import os
from datetime import datetime
from pymongo import MongoClient

from .session_items import *


#Get Connection sTrign for Mongo

def get_connection_string():
    return os.environ.get("CONNECTION_STRING")


#Globals
client= MongoClient(get_connection_string())
db = client['ToDo-Database']
collection = db['todo-boards']



# add a new card to the board
def add_card(listId, cardName, desc, due):
    

    card_document = {
        "listId": listId,
        "name": cardName,
        "desc": desc,
        "due": due,
        "boards" : "TestBoard",
        "updated": datetime.now()
    }
    
    try:
        # Insert the document into the collection
        result = collection.insert_one(card_document)
        response = {"_id": str(result.inserted_id)}
        print (response)
    except Exception as exception:
        print(f"An error occured: {exception}")
        response = False

    return response








# globals
baseUrl = "https://api.trello.com/1/"
headers = {"Accept": "application/json"}


class Item:
    def __init__(
        self,
        id,
        name,
        date,
        dueDate=None,
        description=None,
        status="To Do",
    ):
        self.id = id
        self.name = name
        self.status = status
        self.date = date
        self.dueDate = dueDate if dueDate is not None else "12-12-12"
        self.description = (
            description if description is not (None or "") else "No description"
        )

    @classmethod
    def from_trello_card(cls, card, list):
        lastActiveDate = datetime.strptime(
            card["dateLastActivity"], "%Y-%m-%dT%H:%M:%S.%fZ"
        ).strftime("%d/%m/%y")
        if card.get("due"):
            dueDate = datetime.strptime(card["due"], "%Y-%m-%dT%H:%M:%S.%fZ").strftime(
                "%d/%m/%y"
            )
        else:
            dueDate = None

        return cls(
            card["id"],
            card["name"],
            lastActiveDate,
            dueDate,
            card["desc"],
            list["name"],
        )


def get_query():
    return {
        "key": os.environ.get("TRELLO_KEY"),
        "token": os.environ.get("TRELLO_TOKEN"),
    }


# get boards avaialble to the user
def get_boards():
    searchUrl = baseUrl + "members/me/boards?fields=name"
    try:
        response = requests.request(
            "GET", searchUrl, headers=headers, params=get_query()
        )
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
        response = requests.request(
            "GET", searchUrl, headers=headers, params=get_query()
        )
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
        response = requests.request(
            "GET", searchUrl, headers=headers, params=get_query()
        )
        response.raise_for_status()
        response = response.json()
    except requests.exceptions.RequestException as exception:
        print(f"An error occured: {exception}")
        response = None

    return response


# get cards on a board
def get_cards(id):
    classItems = []

    try:
        # get all lists for the board
        boardLists = get_boardLists(id)

        # add to session items
        save_board_lists(boardLists)

        # get the cards for each list
        if len(boardLists) > 0:
            for obj in boardLists:
                cardsList = get_list_cards(obj["id"])
                for cardList in cardsList:
                    item = Item.from_trello_card(cardList, obj)
                    classItems.append(item)
    except requests.exceptions.RequestException as exception:
        print(f"An error occured: {exception}")
        classItems = []
    return classItems


# # add a new card to the board
# def add_card(listId, cardName, desc, due):
#     searchUrl = baseUrl + "cards"

#     addQuery = {
#         "key": os.getenv("TRELLO_KEY"),
#         "token": os.getenv("TRELLO_TOKEN"),
#         "idList": listId,
#         "name": cardName,
#         "desc": desc,
#         "due": due,
#     }
#     try:
#         response = requests.request("POST", searchUrl, headers=headers, params=addQuery)
#         response.raise_for_status()
#         response = response.json()
#     except requests.exceptions.RequestException as exception:
#         print(f"An error occured: {exception}")
#         response = False

#     return response


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
        response = requests.request("DELETE", searchUrl, params=get_query())
        response.raise_for_status()
        response = response.json()
    except requests.exceptions.RequestException as exception:
        print(f"An error occured: {exception}")
        response = False

    return response


# create a new board
def create_board(boardName):
    if boardName:
        searchUrl = baseUrl + "boards/"
        query = get_query()
        query["name"] = boardName

        try:
            response = requests.request("POST", searchUrl, params=query)
            response.raise_for_status()
            response = response.json()["id"]
        except requests.exceptions.RequestException as exception:
            print(f"An error occured: {exception}")
            response = False
    else:
        response = False
    return response


# delete a board
def delete_board(boardId):
    if boardId:
        searchUrl = baseUrl + f"boards/{boardId}"
        query = get_query()

        try:
            response = requests.request("DELETE", searchUrl, params=query)
            response.raise_for_status()
            response = response.json()
        except requests.exceptions.RequestException as exception:
            print(f"An error occured: {exception}")
            response = False
    else:
        response = False

    return response
