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
    print(cardsList)

    return render_template("index.html", cardsList=cardsList, status=status)


@app.route("/", methods=["POST"])
def add_new_item():
    item = request.form["item"]
    add_item(item)
    return redirect("/")


@app.route("/check", methods=["POST"])
def update_item():
    data = request.get_json()
    item = get_item(data["id"])
    item["status"] = "Completed"
    save_item(item)
    response = {"message": "Item updated successfully", "item": item}
    return jsonify(response), 200


@app.route("/delete", methods=["POST"])
def delete_an_item():
    data = request.get_json()
    id = get_item(data["id"])
    print(id["id"])
    result = delete_item(id["id"])

    if result:
        response = {"message": "Item deleted successfully", "id": id}

    else:
        response = {"message": "Item not found", "id": id}

    return jsonify(response), 200
