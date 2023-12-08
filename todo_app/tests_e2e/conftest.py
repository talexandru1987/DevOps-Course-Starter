import os
from time import sleep
from threading import Thread
from todo_app import app
import pytest
from selenium import webdriver
from dotenv import load_dotenv, find_dotenv

from ..data.trello_items import *


@pytest.fixture(scope="module")
def app_with_temp_board():
    file_path = find_dotenv(".env")
    load_dotenv(file_path, override=True)
    # Create the new board & update the board id environment variable
    board_id = create_board("testBoard")
    os.environ["TRELLO_BOARD_ID"] = board_id

    # Construct the new application
    application = app.create_app()

    # Start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    # Give the app a moment to start
    sleep(1)

    yield application

    # Tear Down
    thread.join(1)
    delete_board(board_id)


@pytest.fixture(scope="module")
def driver():
    opts = webdriver.ChromeOptions()
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    with webdriver.Chrome(options=opts) as driver:
        yield driver
