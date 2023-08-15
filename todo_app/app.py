from flask import Flask, render_template, request, redirect

from todo_app.flask_config import Config

from .data.trello_items import *

from .data.session_items import *

from datetime import datetime

from .data.viewModel import *

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
    cardsList = ViewModel(get_cards(id)).items
    cardsList.sort(key=lambda x: x.status)
    boardLists = get_boardLists(id)
    # add to session items
    save_board_id(id)

    return render_template(
        "index.html",
        cardsList=cardsList,
        status=status,
        boardLists=boardLists,
        boardId=id,
    )


@app.route("/add", methods=["POST"])
def add_new_item():
    boardId = session["boardID"]
    inputItem = request.form.get("inputItem")
    selectedList = request.form.get("selectedList")
    itemDescription = request.form.get("itemDescription")
    dueDate = request.form.get("dueDate")
    date_object = datetime.strptime(dueDate, "%d-%m-%y").date()
    if inputItem:
        add_card(selectedList, inputItem, itemDescription, date_object)

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
