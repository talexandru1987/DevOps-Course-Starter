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

#database connection
class MongoAccess():
    def __init__(self):
        conn_str = os.environ.get("CONNECTION_STRING")
        client= MongoClient(conn_str)
        db = client['ToDo-Database']
        self.cardsCollection = db['todo-cards']
        self.boardsCollection = db['todo-boards']

#One item contains all the data for 1 card
class Item:
    def __init__(
        self,
        id,
        name,
        date,
        dueDate=None,
        description=None,
        listName="To Do",
    ):
        self.id = id
        self.name = name
        self.listName = listName
        self.date = date
        self.dueDate = dueDate if dueDate is not None else "12-12-12"
        self.description = (
            description if description is not (None or "") else "No description"
        )

    @classmethod
    def create_card(cls, card):
        lastActiveDate = card["dateLastActivity"].strftime("%d/%m/%y")
        if card.get("due"):
            dueDate = card["due"].strftime(
                "%d/%m/%y"
            )
        else:
            dueDate = None
        
        listName = "To Do"
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

def add_card(listId, cardName, desc, due, board, addedCollection = None):
    mongo_access = MongoAccess()
    collection = mongo_access.cardsCollection if addedCollection is None else addedCollection

    card_document = {
        "listId": listId,
        "name": cardName,
        "due": due,
        "dateLastActivity": datetime.now(),
        "desc": desc,
        "boards" : [board]
    }
    
    try:
        # Insert the document into the collection
        result = collection.insert_one(card_document)
        response = {"_id": str(result.inserted_id)}
    except Exception as exception:
        print(f"An error occured: {exception}")
        response = False

    return response

# get cards on a board
def get_cards(id, addedCollection = None):
    mongo_access = MongoAccess()
    collection = mongo_access.cardsCollection if addedCollection is None else addedCollection

    #get all the documents
    documentsList = collection.find({"boards": id})
 
    classItems = []

    try:
        for document in documentsList:
            item = Item.create_card(document)
            classItems.append(item)

    except requests.exceptions.RequestException as exception:
        print(f"An error occured: {exception}")
        classItems = []
    return classItems

# create a new board
def create_board(boardName, description, addedCollection = None):

    mongo_access = MongoAccess()
    collection = mongo_access.boardsCollection if addedCollection is None else addedCollection
    board_document = {
        "name": boardName,
        "description": description,
        "created": datetime.now(),
        "boards": "1"
    }
    
    try:
        # Insert the document into the collection
        result = collection.insert_one(board_document)
        response = {"_id": str(result.inserted_id)}
    except Exception as exception:
        print(f"An error occured: {exception}")
        response = False

    return response

#Delete a document from the boards collection
def delete_board_by_name(boardName, addedCollectionCard = None, addedCollectionBoard = None):

    mongo_access = MongoAccess()
    collectionCard = mongo_access.cardsCollection if addedCollectionCard is None else addedCollectionCard
    collectionBoard = mongo_access.boardsCollection if addedCollectionBoard is None else addedCollectionBoard
    if addedCollectionCard is not None:
        collectionCard= addedCollectionCard
        collectionBoard = addedCollectionBoard
    try:
        # First, find the document to get its _id
        board = collectionBoard.find_one({"name": boardName}, {"_id": 1})
        if board:
            board_id_str = str(board['_id'])
            # Attempt to delete the document by name
            result = collectionBoard.delete_one({"_id": board['_id']})
            
            if result.deleted_count > 0:
                print(f"Board '{boardName}' was deleted successfully.")

                # Now, delete all related cards that have this board's _id in their 'boards' property
                related_cards_result = collectionCard.delete_many({"boards": {"$in": [board_id_str]}})
                print(f"Related cards deleted count: {related_cards_result.deleted_count}")

                return True
            else:
                print(f"No board found with the name '{boardName}'.")
                return False
        else:
            print(f"No board found with the name '{boardName}', nothing to delete.")
            return False
    except Exception as exception:
        print(f"An error occurred: {exception}")
        return False

# Get all document from the boards collection
def get_boards(addedCollection = None):

    mongo_access = MongoAccess()
    collection = mongo_access.boardsCollection if addedCollection is None else addedCollection
    if addedCollection is not None:
        collection = addedCollection
    try:
        boards = list(collection.find({})) 
        return boards  
    except Exception as exception:
        print(f"An error occurred: {exception}")
        return None
    
# update a card on the board
def update_card(boardID, listId, addedCollection = None):

    mongo_access = MongoAccess()
    collection = mongo_access.cardsCollection if addedCollection is None else addedCollection
    
    try:
        # The update_one method is used to update a single document.
        result = collection.update_one(
            {"_id": boardID},
            {"$set": {"listId": listId}}
        )
        if result.modified_count > 0:
            return {"status": "success", "message": "Document updated."}
        else:
            return {"status": "error", "message": "No document found with the specified _id."}
    except Exception as exception:
        print(f"An error occurred: {exception}")
        return {"status": "error", "message": "An error occurred during the update operation."}

# update a card on the board
def delete_card(cardId, addedCollection = None):
    mongo_access = MongoAccess()
    collection = mongo_access.cardsCollection if addedCollection is None else addedCollection

    try:
        # The delete_one method attempts to delete the first document that matches the provided filter
        result = collection.delete_one({"_id": cardId})
        if result.deleted_count > 0:
            return {"status": "success", "message": "The document was deleted successfully."}
        else:
            return {"status": "error", "message": "No document found with the specified _id or deletion was unsuccessful."}
    except Exception as exception:
        print(f"An error occurred: {exception}")
        return {"status": "error", "message": "An error occurred during the deletion process."}


