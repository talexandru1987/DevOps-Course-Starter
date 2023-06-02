from flask import Flask, render_template

from todo_app.flask_config import Config

from .data.session_items import *


app = Flask(__name__)
app.config.from_object(Config())


@app.route("/")
def index():
    return render_template("index.html", results=get_items())
