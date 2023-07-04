from flask import session
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, date

load_dotenv()
# globals
query = {"key": os.getenv("TRELLO_KEY"), "token": os.getenv("TRELLO_TOKEN")}
baseUrl = "https://api.trello.com/1/"


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


def get_cards(id):
    searchUrl = f"{baseUrl}boards/{id}/cards"
    idOfBoardLists = []
    responseObj = []

    try:
        response = requests.request("GET", searchUrl, params=query)
        response.raise_for_status()
        response = response.json()
        if len(response) > 0:
            # get all the list id's in the reponse
            found = False
            for obj in response:
                listID = obj["idList"]
                for id in idOfBoardLists:
                    if id["id"] == listID:
                        found = True
                        break
                    else:
                        found = False
                if found == False:
                    idOfBoardLists.append({"id": listID})
            # foar each list id get the list name
            for obj in idOfBoardLists:
                searchListurl = f"{baseUrl}lists/{obj['id']}"
                responseList = requests.request("GET", searchListurl, params=query)
                responseList.raise_for_status()
                responseList = responseList.json()
                obj["name"] = responseList["name"]

            # create the return card objects
            for obj in idOfBoardLists:
                for card in response:
                    if obj["id"] == card["idList"]:
                        date = datetime.strptime(
                            card["dateLastActivity"], "%Y-%m-%dT%H:%M:%S.%fZ"
                        )
                        responseObj.append(
                            {
                                "title": card["name"],
                                "list": obj["name"],
                                "date": date.strftime("%d/%m/%y"),
                            }
                        )
            # searchListurl = f"{baseUrl}lists/{obj['idList']}"
            # responseList = requests.request("GET", searchListurl, params=query)
            # responseList.raise_for_status()
            # responseList = responseList.json()
            # date = datetime.strptime(
            #     obj["dateLastActivity"], "%Y-%m-%dT%H:%M:%S.%fZ"
            # )
            # responseObj.append(
            #     {
            #         "title": obj["name"],
            #         "list": responseList["name"],
            #         "date": date.strftime("%d/%m/%y"),
            #     }
            # )

        print(responseObj)

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

    # def get_items():
    """
    Fetches all cards from the trello board.

    Returns:
        list: The list of saved items.
    """
    # return session.get("items", _DEFAULT_ITEMS.copy())


# boardItem = next((obj for obj in response if obj["name"] == name), None)
