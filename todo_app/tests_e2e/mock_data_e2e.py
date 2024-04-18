import datetime


def mock_boardsCollection_e2e():
    return [
       {
        "_id": "661bd26783cc1295b454f321",
        "name" : "Test 1",
        "description" : "",
        "created" : datetime.datetime.now(),
        "boards" : "1"
    },
    {
        "_id": "661bd26783cc1295b454f311",
        "name" : "Test 2",
        "description" : "",
        "created" : datetime.datetime.now(),
        "boards" : "1"
    }
    ]


def mock_cardsCollection_e2e():
    return [
       {
        "_id" :"661bda5e1f5971bd6842416f",
        "listId" : "657c834ff1b03a6ddfeadc94",
        "name" : "First Item",
        "due" : datetime.datetime.now(),
        "dateLastActivity" : datetime.datetime.now(),
        "desc" : "ewqe",
        "boards" : [
            "661bd26783cc1295b454f311"
        ]
    },
    {
        "_id" :"661bda5e1f5971bd684241644",
        "listId" : "657c834ff1b03a6ddfeadc94",
        "name" : "First Item",
        "due" : datetime.datetime.now(),
        "dateLastActivity" : datetime.datetime.now(),
        "desc" : "ewqe",
        "boards" : [
            "661bd26783cc1295b454f321"
        ]
    }

    ]



