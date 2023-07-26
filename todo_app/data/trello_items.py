from flask import session
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, date

load_dotenv()
# globals
query = {"key": os.getenv("TRELLO_KEY"), "token": os.getenv("TRELLO_TOKEN")}
baseUrl = "https://api.trello.com/1/"
headers = {"Accept": "application/json"}


# get boards avaialble to the user
def get_boards():
    searchUrl = baseUrl + "members/me/boards?fields=name"

    try:
        response = requests.request("GET", searchUrl, params=query)
        response.raise_for_status()
        response = response.json()
    except requests.exceptions.RequestException as exception:
        print(f"An error occured: {exception}")
        response = None
    return response


# get the cards in a specific list
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


# get all cards on a board
def get_cards(id):
    listSearchUrl = f"{baseUrl}boards/{id}/lists"
    responseObj = []
    found = False

    try:
        # get all lists for the board
        response = requests.request("GET", listSearchUrl, headers=headers, params=query)
        response.raise_for_status()
        boardLists = response.json()

        # get the cards for each list
        if len(boardLists) > 0:
            for obj in boardLists:
                cardsList = get_list_cards(obj["id"])
                for cardObj in cardsList:
                    # if responseObj is empty code will not execute so need an if
                    for card in responseObj:
                        if cardObj["id"] == card["id"]:
                            found = True
                            break
                        else:
                            found = False
                    if found == False:
                        date = datetime.strptime(
                            cardObj["dateLastActivity"], "%Y-%m-%dT%H:%M:%S.%fZ"
                        )
                        responseObj.append(
                            {
                                "id": cardObj["id"],
                                "title": cardObj["name"],
                                "list": obj["name"],
                                "date": date.strftime("%d/%m/%y"),
                            }
                        )
    except requests.exceptions.RequestException as exception:
        print(f"An error occured: {exception}")
        responseObj = []
    return responseObj


def get_boardLists(id):
    searchUrl = f"{baseUrl}boards/{id}/lists"

    try:
        response = requests.request("GET", searchUrl, params=query)
        response.raise_for_status()
        response = response.json()
    except requests.exceptions.RequestException as exception:
        print(f"An error occured: {exception}")
        response = None

    return response


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


def add_list_item(listId, cardName):
    searchUrl = baseUrl + "cards"

    addQuery = {
        "key": os.getenv("TRELLO_KEY"),
        "token": os.getenv("TRELLO_TOKEN"),
        "idList": listId,
        "name": cardName,
    }
    try:
        response = requests.request("POST", searchUrl, params=addQuery)
        response.raise_for_status()
        response = response.json()
    except requests.exceptions.RequestException as exception:
        print(f"An error occured: {exception}")
        response = False

    return response


# boardItem = next((obj for obj in response if obj["name"] == name), None)
