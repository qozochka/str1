from linked_list_item import LinkedListItem


# class Node:
#     def __init__(self, data):
#         self.data = data
#         self.next = None


class LinkedList:
    def __init__(self, first_item):
        self.first_item = first_item
        self.last_item = first_item

    def append_left(self, item):
        """Добавление элемента в начало списка."""
        new_node = LinkedListItem(item)
        new_node.next_item = self.first_item
        self.first_item = new_node

    def append_right(self, data):
        """Добавление элемента в конец списка."""
        new_node = LinkedListItem(data)
        if self.first_item is None:
            self.first_item = new_node
            self.last_item = new_node
            return
        else:
            self.last_item.next_item = new_node
            self.last_item = new_node

    def append(self, item):
        """Алиас для append_right."""
        self.append_right(item)

    def remove(self, item):
        """Удаление элемента. Возбуждает ValueError, если элемент отсутствует."""
        if self.first_item is None:
            raise ValueError("Список пуст")

        if self.first_item.track == item:
            self.first_item = self.first_item.next_item
            return

        current = self.first_item
        while current.next_item:
            if current.next_item.track == item:
                current.next_item = current.next_item.next_item
                return
            current = current.next_item
        raise ValueError(f"Элемент '{item}' не найден в списке")

    def insert(self, previous, item):
        """Вставка элемента item после элемента previous."""
        if self.first_item is None:
            raise ValueError("Список пуст")

        new_node = LinkedListItem(item)

        current = self.first_item
        while current:
            if current.track == previous:
                new_node.next_item = current.next_item
                current.next_item = new_node
                return
            current = current.next_item
        raise ValueError(f"Элемент '{previous}' не найден в списке!")

    def last(self):
        """Получение последнего элемента списка."""
        if self.first_item is None:
            return None
        current = self.first_item
        while current.next_item:
            current = current.next_item
        return current

    def __len__(self):
        """Длина списка."""
        count = 0
        current = self.first_item
        while current:
            count += 1
            current = current.next_item
        return count

    def __iter__(self):
        """Получение итератора."""
        self.current = self.first_item
        return self

    def __next__(self):
        """Получение следующего элемента."""
        if self.current is None:
            raise StopIteration
        item = self.current.track
        self.current = self.current.next_item
        return item

    def __getitem__(self, index):
        """Получение элемента по индексу."""
        if index < 0 or index >= len(self):
            raise IndexError("Индекс за пределами диапазона")

        count = 0
        current = self.first_item
        while current and current.next_item is not self.first_item:
            if count == index:
                return current.track
            count += 1
            current = current.next_item

    def __contains__(self, item):
        """Поддержка оператора in."""
        current = self.first_item
        while current and current.next_item is not self.first_item:
            if current.track == item:
                return True
            current = current.next_item
        return False

    def __reversed__(self):
        """Поддержка функции reversed."""
        reversed_list = LinkedList()
        current = self.first_item
        while current and current.next_item is not self.first_item:
            reversed_list.append_left(current.track)
            current = current.next_item
        return reversed_list
