from flask import Flask, render_template, request, redirect

from todo_app.flask_config import Config

from .data.session_items import *


app = Flask(__name__)
app.config.from_object(Config())


@app.route("/")
def index():
    return render_template("index.html", results=get_items())


@app.route("/", methods=["POST"])
def add_new_item():
    item = request.form["item"]
    add_item(item)
    return redirect("/")
