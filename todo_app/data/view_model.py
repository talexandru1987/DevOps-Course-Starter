from datetime import datetime


class ViewModel:
    def __init__(self, items):
        self._items = items

    def _is_today(self, dateStr):
        dateStamp = datetime.strptime(dateStr, "%d/%m/%y").date()
        today_date = datetime.now().date()
        return dateStamp == today_date

    @property
    def items(self):
        return self._items

    @property
    def todo_items(self):
        return list(filter(lambda item: item.status == "To Do", self._items))

    @property
    def doing_items(self):
        return list(filter(lambda item: item.status == "Doing", self._items))

    @property
    def done_items(self):
        return list(filter(lambda item: item.status == "Done", self._items))

    @property
    def recent_done_items(self):
        test = list(
            filter(
                lambda item: item.status == "Done" and self._is_today(item.date),
                self._items,
            )
        )
        test1 = test[0].status
        test2 = test[0].date
        return list(
            filter(
                lambda item: item.status == "Done" and self._is_today(item.date),
                self._items,
            )
        )

    @property
    def older_done_items(self):
        return list(
            filter(
                lambda item: item.status == "Done" and not (self._is_today(item.date)),
                self._items,
            )
        )
