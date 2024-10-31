class LinkedListItem:
    def __init__(self, track, next_item=None, previous_item=None):
        self.track = track  # элемент Composition
        self._next = next_item
        self._previous = previous_item

    @property
    def next_item(self):
        return self._next

    @next_item.setter
    def next_item(self, value):
        self._next = value

    @property
    def previous_item(self):
        return self._previous

    @previous_item.setter
    def previous_item(self, value):
        self._previous = value
