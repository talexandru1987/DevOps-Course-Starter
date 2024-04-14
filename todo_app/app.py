from flask import Flask, render_template, request, redirect

from todo_app.flask_config import Config

from .data.trello_items import *

from .data.session_items import *

from datetime import datetime

from .data.view_model import *


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    @app.route("/")
    def index():
        status = True
        boardsList = get_boards()
        return render_template("index.html", boardsList=boardsList, status=status)

    @app.route("/<id>")
    def render_cards(id):
        status = False

        #get all cards for the board id
        allCardsModel = ViewModel(get_cards(id))

        #add to session items
        save_board_id(id)

        return render_template(
            "index.html",
            doneCardsList=allCardsModel.done_items,
            toDoCardsList=allCardsModel.todo_items,
            doingCardsList=allCardsModel.doing_items,
            status=status,
            boardId=id,
            #the list selection for the add card form
            boardLists =[{"id":"657c834ff1b03a6ddfeadc94", "name": "Done"},{"id":"657c834ff1b03a6ddfeadc93", "name": "Doing"},{"id":"657c834gg1b03a6ddfeadc84", "name": "To Do"}]
        )

    @app.route("/add", methods=["POST"])
    def add_new_item():
        boardId = session["boardID"]
        inputItem = request.form.get("inputItem")
        selectedList = request.form.get("selectedList")
        itemDescription = request.form.get("itemDescription")
        dueDate = request.form.get("dueDate")
        date_object = datetime.strptime(dueDate, "%d-%m-%y").date()
        # Convert the datetime.date object to a datetime.datetime object by adding a default time
        due_datetime = datetime.combine(date_object, datetime.min.time())

        if inputItem:
            add_card(selectedList, inputItem, itemDescription, due_datetime, boardId)

        return redirect(f"/{boardId}")

    @app.route("/update", methods=["POST"])
    def update_item():
        boardId = session["boardID"]
        cardId = request.form.get("card_id")
        listId = request.form.get("updateList")
        update_card(cardId, listId)

        return redirect(f"/{boardId}")

    @app.route("/delete", methods=["POST"])
    def delete_an_item():
        boardId = session["boardID"]
        cardId = request.form.get("card_id")
        delete_card(cardId)
        return redirect(f"/{boardId}")
    
    @app.route("/addBoard", methods=["POST"])
    def create_new_board():
        boardName = request.form.get("inputItem")
        boardDescription = request.form.get("itemDescription")
        create_board(boardName,boardDescription )
        return redirect("/")
    
    @app.route("/deleteBoard", methods=["POST"])
    def delete_board():
        boardName = request.form.get("deleteItem")
        delete_board_by_name(boardName)
        return redirect("/")

    return app
