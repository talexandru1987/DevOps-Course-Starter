from flask import Flask, render_template, request, redirect, jsonify

from todo_app.flask_config import Config

from .data.session_items import *


app = Flask(__name__)
app.config.from_object(Config())


@app.route("/")
def index():
    itemsList = sorted(get_items(), key=lambda x: x["status"])
    return render_template("index.html", results=itemsList)


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
