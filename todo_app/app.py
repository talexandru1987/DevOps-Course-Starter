from flask import Flask, render_template, request, redirect, jsonify, session

from todo_app.flask_config import Config

from .data.session_items import *

from .data.trello_items import *

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
    cardsList = get_cards(id)
    boardLists = get_boardLists(id)

    return render_template(
        "index.html",
        cardsList=cardsList,
        status=status,
        boardLists=boardLists,
        boardId=id,
    )


@app.route("/add", methods=["POST"])
def add_new_item():
    boardId = request.form.get("board_id")
    inputItem = request.form.get("inputItem")
    selectedList = request.form.getlist("selectedList")[0]

    if inputItem:
        add_list_item(selectedList, inputItem)

    return redirect(f"/{boardId}")


@app.route("/update", methods=["POST"])
def update_item():
    print(f"Add to this id+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(request.form)

    return "nothing"


@app.route("/delete", methods=["POST"])
def delete_an_item():
    data = request.get_json()
    id = get_item(data["id"])

    result = delete_item(id["id"])

    if result:
        response = {"message": "Item deleted successfully", "id": id}

    else:
        response = {"message": "Item not found", "id": id}

    return jsonify(response), 200
