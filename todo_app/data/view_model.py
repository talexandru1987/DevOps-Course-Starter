class ViewModel:
    def __init__(self, items):
        self._items = items

    @property
    def items(self):
        return self._items

    @property
    def done_items(self):
        return list(filter(lambda item: item.status == "Done", self._items))

    @property
    def todo_items(self):
        return list(filter(lambda item: item.status == "To Do", self._items))

    @property
    def doing_items(self):
        return list(filter(lambda item: item.status == "Doing", self._items))
