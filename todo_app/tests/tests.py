import unittest
from todo_app.data.trello_items import *


class TestMyFunction(unittest.TestCase):
    def test_get_boardID(self):
        result = get_boardLists("4124123f213qrf3124r")
        print(result)
        self.assertEqual(result, None)
