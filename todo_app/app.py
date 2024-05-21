from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_required, login_user
import os
from todo_app.flask_config import Config

from .data.mongo_items import *

from .data.session_items import *

from datetime import datetime

from .data.view_model import *



# Define the User class
class User(UserMixin):
    def __init__(self, id):
        self.id = id

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    # Set LOGIN_DISABLED based on the environment variable
    app.config['LOGIN_DISABLED'] = os.getenv('LOGIN_DISABLED') == 'True'

    login_manager = LoginManager()

    @login_manager.unauthorized_handler
    def unauthenticated():
        github_auth_url = construct_github_url()
        return redirect(github_auth_url)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)

    login_manager.init_app(app)


    @app.route('/.auth/login/github/callback')
    def github_callback():
        # Extract the 'code' from the query parameters
        code = request.args.get('code')
        if not code:
            return 'Authorization request failed', 400

        # Exchange the code for an access token
        access_token = exchange_code_for_token(code)

        
        if not access_token:
            return 'Failed to fetch access token', 400
        
        #Get the authenticated user
        authenticated_user = get_github_user(access_token)
        

        if not authenticated_user:
            return 'Failed to fetch the authenticated user', 400
        
        # Construct a new instance of the User class
        user = User(authenticated_user['id'])
        login_user(user)

        # Store the access token in a session or a secure place
        session['access_token'] = access_token
        session['user_info'] = authenticated_user

        # Redirect to a secure page or a dashboard
        return redirect('/')

    @app.route("/")
    @login_required
    def index():
        status = True
        boardsList = get_boards()
        return render_template("index.html", boardsList=boardsList, status=status)

    @app.route("/<id>")
    @login_required
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
    @login_required
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
    @login_required
    def update_item():
        boardId = session["boardID"]
        cardId = request.form.get("card_id")
        listId = request.form.get("updateList")
        update_card(cardId, listId)

        return redirect(f"/{boardId}")

    @app.route("/delete", methods=["POST"])
    @login_required
    def delete_an_item():
        boardId = session["boardID"]
        cardId = request.form.get("card_id")
        delete_card(cardId)
        return redirect(f"/{boardId}")
    
    @app.route("/addBoard", methods=["POST"])
    @login_required
    def create_new_board():
        boardName = request.form.get("inputItem")
        boardDescription = request.form.get("itemDescription")
        create_board(boardName,boardDescription )
        return redirect("/")
    
    @app.route("/deleteBoard", methods=["POST"])
    @login_required
    def delete_board():
        boardName = request.form.get("deleteItem")
        delete_board_by_name(boardName)
        return redirect("/")

    return app
