def mock_cards():
    return [
        {
            "card": {
                "id": "1",
                "name": "Test1",
                "dateLastActivity": "2023-08-26T00:00:00.000Z",
                "due": "2023-08-26T00:00:00.000Z",
                "desc": "card1",
            },
            "list": {"name": "To Do"},
        },
        {
            "card": {
                "id": "2",
                "name": "Test1",
                "dateLastActivity": "2023-08-26T00:00:00.000Z",
                "due": "2023-08-26T00:00:00.000Z",
                "desc": "card2",
            },
            "list": {"name": "Done"},
        },
        {
            "card": {
                "id": "3",
                "name": "Test1",
                "dateLastActivity": "2023-08-26T00:00:00.000Z",
                "due": "2023-08-26T00:00:00.000Z",
                "desc": "card3",
            },
            "list": {"name": "Doing"},
        },
        {
            "card": {
                "id": "4",
                "name": "Test1",
                "dateLastActivity": "2023-08-27T00:00:00.000Z",
                "due": "2023-08-26T00:00:00.000Z",
                "desc": "card4",
            },
            "list": {"name": "Done"},
        },
    ]


def mock_board_lists():
    return [
        {
            "id": "64fwqdffe670fca0",
            "name": "To Do",
            "closed": "false",
            "idBoard": "649984e03dwqdfe670fc99",
            "pos": 16384,
            "subscribed": "false",
            "softLimit": "null",
            "status": "null",
        },
        {
            "id": "64fwqdffe670fca0",
            "name": "Doing",
            "closed": "fake",
            "idBoard": "6dwqdwq7ffe670fc99",
            "pos": 32768,
            "subscribed": "fake",
            "softLimit": "fake",
            "status": "fake",
        },
        {
            "id": "64fwqdffe670fca0",
            "name": "Done",
            "closed": "fake",
            "idBoard": "64dqwdqwdwqf7ffe670fc99",
            "pos": 49152,
            "subscribed": "fake",
            "softLimit": "fake",
            "status": "fake",
        },
    ]


def mock_list_cards():
    return [
        {
            "id": "64fwqdffe670fca0",
            "badges": {
                "attachmentsByType": {"trello": {"board": 0, "card": 0}},
                "location": "fake",
                "votes": 0,
                "viewingMemberVoted": "fake",
                "subscribed": "fake",
                "fogbugz": "",
                "checkItems": 0,
                "checkItemsChecked": 0,
                "checkItemsEarliestDue": "fake",
                "comments": 0,
                "attachments": 0,
                "description": "fake",
                "due": "2023-08-26T00:00:00.000Z",
                "dueComplete": "fake",
                "start": "fake",
            },
            "checkItemStates": [],
            "closed": "fake",
            "dueComplete": "fake",
            "dateLastActivity": "2023-08-13T09:54:19.406Z",
            "desc": "6kl67",
            "descData": {"emoji": {}},
            "due": "2023-08-26T00:00:00.000Z",
            "dueReminder": "fake",
            "email": "fake",
            "idBoard": "649984e03dadf7ffe670fc99",
            "idChecklists": [],
            "idList": "649984e03dadf7ffe670fca0",
            "idMembers": [],
            "idMembersVoted": [],
            "idShort": 29,
            "idAttachmentCover": "fake",
            "labels": [],
            "idLabels": [],
            "manualCoverAttachment": "fake",
            "name": "asdfg",
            "pos": 65536,
            "shortLink": "j2jPi3hZ",
            "shortUrl": "https://trello.com/c/j2jPi3hZ",
            "start": "fake",
            "subscribed": "fake",
            "url": "https://trello.com/c/j2jPi3hZ/29-asdfg",
            "cover": {
                "idAttachment": "fake",
                "color": "fake",
                "idUploadedBackground": "fake",
                "size": "normal",
                "brightness": "dark",
                "idPlugin": "fake",
            },
            "isTemplate": "fake",
            "cardRole": "fake",
        }
    ]
