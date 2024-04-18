import os
from time import sleep
from threading import Thread

import mongomock
from todo_app import app
import pytest
from selenium import webdriver
from dotenv import load_dotenv, find_dotenv

from todo_app.tests_e2e.mock_data_e2e import mock_boardsCollection_e2e, mock_cardsCollection_e2e

from ..data.trello_items import *

@pytest.fixture(scope="module")
def app_with_temp_board():
    # Load environment variables
    file_path = find_dotenv(".env")
    load_dotenv(file_path, override=True)

    # Setup Mock MongoDB client
    mock_client = mongomock.MongoClient()
    app.db = mock_client.db  # Assuming the app has a db attribute

    # Clear existing data and insert mock data
    boardsCollection = app.db.boards
    cardsCollection = app.db.cards
    boardsCollection.delete_many({})
    cardsCollection.delete_many({})
    boardsCollection.insert_many(mock_boardsCollection_e2e())
    cardsCollection.insert_many(mock_cardsCollection_e2e())

    # Optionally set environment variable for MongoDB collection
    os.environ["MONGODB_COLLECTION"] = 'boards'

    # Construct and start the Flask application in a separate thread
    application = app.create_app()
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    sleep(1)  # Allow time for the app to start

    yield application

    # Teardown the application and database
    thread.join(1)
    boardsCollection.drop()
    cardsCollection.drop()



@pytest.fixture(scope="module")
def driver():
    opts = webdriver.ChromeOptions()
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    with webdriver.Chrome(options=opts) as driver:
        yield driver
