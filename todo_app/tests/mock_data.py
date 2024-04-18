def mock_boardsCollection():
    return [
       {
        "_id": "661bd26783cc1295b454f321",
        "name" : "Test 1",
        "description" : "",
        "created" : {
            "$date" : 1713102967938
        },
        "boards" : "1"
    },
    {
        "_id": "661bd26783cc1295b454f311",
        "name" : "Test 2",
        "description" : "",
        "created" : {
            "$date" : 1713102967938
        },
        "boards" : "1"
    }
    ]


def mock_cardsCollection():
    return [
       {
        "_id" :"661bda5e1f5971bd6842416f",
        "listId" : "657c834ff1b03a6ddfeadc94",
        "name" : "First Item",
        "due" : {
            "$date" : 1713312000000
        },
        "dateLastActivity" : {
            "$date" : 1713105006532
        },
        "desc" : "ewqe",
        "boards" : [
            "661bd26783cc1295b454f311"
        ]
    },
    {
        "_id" :"661bda5e1f5971bd684241644",
        "listId" : "657c834ff1b03a6ddfeadc94",
        "name" : "First Item",
        "due" : {
            "$date" : 1713312000000
        },
        "dateLastActivity" : {
            "$date" : 1713105006532
        },
        "desc" : "ewqe",
        "boards" : [
            "661bd26783cc1295b454f321"
        ]
    }

    ]



