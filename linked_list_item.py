class LinkedListItem:
    def __init__(self, data, next_item=None, previous_item=None):
        self.data = data  # элемент Composition
        self._next_item = next_item
        self._previous_item = previous_item

    @property
    def next_item(self):
        return self._next_item

    @next_item.setter
    def next_item(self, value):
        self._next_item = value

    @property
    def previous_item(self):
        return self._previous_item

    @previous_item.setter
    def previous_item(self, value):
        self._previous_item = value
