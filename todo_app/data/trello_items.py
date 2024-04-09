import requests
import os
from datetime import datetime
from pymongo import MongoClient

from .session_items import *


#Get Connection sTrign for Mongo

def get_connection_string():
    return os.environ.get("CONNECTION_STRING")

def get_collection(databaseNem, collectionName):
    return databaseNem[collectionName]

#Globals
client= MongoClient(get_connection_string())
db = client['ToDo-Database']
cardsCollection = get_collection(db, 'todo-cards')
boardsCollection = get_collection(db, 'todo-boards')

#An item contains all the data for 1 card
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
    def from_trello_card(cls, card):
        listName = "To Do"
        lastActiveDate = card["dateLastActivity"].strftime("%d/%m/%y")
        if card.get("due"):
            dueDate = card["due"].strftime(
                "%d/%m/%y"
            )
        else:
            dueDate = None

        #get list name
        if card["listId"] == "657c834ff1b03a6ddfeadc94":
            listName = "Done"
        elif card["listId"] == "657c834ff1b03a6ddfeadc93":
            listName = "Doing"


        return cls(
            card["_id"],
            card["name"],
            lastActiveDate,
            dueDate,
            card["desc"],
            listName,
        )


# Add a new document to the DBcard
def add_card(listId, cardName, desc, due):
    
    card_document = {
        "listId": listId,
        "name": cardName,
        "due": due,
        "dateLastActivity": datetime.now(),
        "desc": desc,
        "boards" : "TestBoard"
    }
    
    try:
        # Insert the document into the collection
        result = cardsCollection.insert_one(card_document)
        response = {"_id": str(result.inserted_id)}
    except Exception as exception:
        print(f"An error occured: {exception}")
        response = False

    return response

# get cards on a board
def get_cards(id):
    #get all the documents
    documentsList = cardsCollection.find({})
    classItems = []

    try:
        for document in documentsList:
            item = Item.from_trello_card(document)
            classItems.append(item)

    except requests.exceptions.RequestException as exception:
        print(f"An error occured: {exception}")
        classItems = []
    return classItems

# create a new board
def create_board(boardName, description):
    board_document = {
        "name": boardName,
        "description": description,
        "created": datetime.now(),
        "boards": "1"
    }
    
    try:
        # Insert the document into the collection
        result = boardsCollection.insert_one(board_document)
        response = {"_id": str(result.inserted_id)}
    except Exception as exception:
        print(f"An error occured: {exception}")
        response = False

    return response

#Delete a document from the boards collection
def delete_board_by_name(boardName):
    try:
        # Attempt to delete the document by name
        result = boardsCollection.delete_one({"name": boardName})
        
        if result.deleted_count > 0:
            print(f"Board '{boardName}' was deleted successfully.")
            return True
        else:
            print(f"No board found with the name '{boardName}'.")
            return False
    except Exception as exception:
        print(f"An error occurred: {exception}")
        return False

# Get all document from the boards collection
def get_boards():
    try:
        boards = list(boardsCollection.find({}))  
        return boards  
    except Exception as exception:
        print(f"An error occurred: {exception}")
        return None
    


# globals
baseUrl = "https://api.trello.com/1/"
headers = {"Accept": "application/json"}




def get_query():
    return {
        "key": os.environ.get("TRELLO_KEY"),
        "token": os.environ.get("TRELLO_TOKEN"),
    }


# get boards avaialble to the user
# def get_boards():
#     searchUrl = baseUrl + "members/me/boards?fields=name"
#     try:
#         response = requests.request(
#             "GET", searchUrl, headers=headers, params=get_query()
#         )
#         response.raise_for_status()
#         response = response.json()
#         print(response)
#     except requests.exceptions.RequestException as exception:
#         print(f"An error occured: {exception}")
#         response = None
#     return response


# get the cards in a list
# def get_list_cards(id):
#     searchUrl = baseUrl + f"lists/{id}/cards"

#     try:
#         response = requests.request(
#             "GET", searchUrl, headers=headers, params=get_query()
#         )
#         response.raise_for_status()
#         response = response.json()
    
#     except requests.exceptions.RequestException as exception:
#         print(f"An error occured: {exception}")
#         response = None
#     return response


# get the lists on  board
# def get_boardLists(id):
#     searchUrl = f"{baseUrl}boards/{id}/lists"

#     try:
#         response = requests.request(
#             "GET", searchUrl, headers=headers, params=get_query()
#         )
#         response.raise_for_status()
#         response = response.json()
#     except requests.exceptions.RequestException as exception:
#         print(f"An error occured: {exception}")
#         response = None

#     return response


# # get cards on a board
# def get_cards(id):
#     classItems = []

#     try:
#         # get all lists for the board
#         boardLists = get_boardLists(id)
        

#         # add to session items
#         save_board_lists(boardLists)

#         # get the cards for each list
#         if len(boardLists) > 0:
#             for obj in boardLists:
#                 cardsList = get_list_cards(obj["id"])
#                 print(f"This is the object: ${obj}")
#                 for cardList in cardsList:
#                     print(f"This is the cardList: ${obj}")
#                     item = Item.from_trello_card(cardList, obj)
#                     classItems.append(item)
#     except requests.exceptions.RequestException as exception:
#         print(f"An error occured: {exception}")
#         classItems = []
#     return classItems


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


# # create a new board
# def create_board(boardName):
#     if boardName:
#         searchUrl = baseUrl + "boards/"
#         query = get_query()
#         query["name"] = boardName

#         try:
#             response = requests.request("POST", searchUrl, params=query)
#             response.raise_for_status()
#             response = response.json()["id"]
#         except requests.exceptions.RequestException as exception:
#             print(f"An error occured: {exception}")
#             response = False
#     else:
#         response = False
#     return response


# delete a board
# def delete_board(boardId):
#     if boardId:
#         searchUrl = baseUrl + f"boards/{boardId}"
#         query = get_query()

#         try:
#             response = requests.request("DELETE", searchUrl, params=query)
#             response.raise_for_status()
#             response = response.json()
#         except requests.exceptions.RequestException as exception:
#             print(f"An error occured: {exception}")
#             response = False
#     else:
#         response = False

#     return response
