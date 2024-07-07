from pymongo import MongoClient
import os
import mongomock

# Database connection
class MongoAccess():
    def __init__(self):
        use_mock_db = os.environ.get('USE_MOCK_DB')
        if use_mock_db == 'True':
            self.client = mongomock.MongoClient()
        else:
            # Explicitly check for the CONNECTION_STRING environment variable
            conn_str = os.environ.get('CONNECTION_STRING')
            if not conn_str:
                raise ValueError("The CONNECTION_STRING environment variable is not set.")
            if not conn_str.startswith('mongodb://') and not conn_str.startswith('mongodb+srv://'):
                raise ValueError("Invalid MongoDB connection string. It must begin with 'mongodb://' or 'mongodb+srv://'")
            self.client = MongoClient(conn_str)
        
        db = self.client['ToDo-Database']
        self.cardsCollection = db['todo-cards']
        self.boardsCollection = db['todo-boards']
