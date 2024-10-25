from linked_list_item import LinkedListItem


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    # def append(self, item):
    #     """Добавление элемента в конец списка."""
    #     new_node = LinkedListItem(item)
    #     if self.head is None:
    #         self.head = new_node
    #         self.tail = new_node
    #     else:
    #         self.tail.next_item = new_node
    #         self.tail = new_node

    def append_left(self, item):
        """Добавление элемента в начало списка."""
        new_node = Node(item)
        new_node.next = self.head
        self.head = new_node

    def append_right(self, item):
        """Добавление элемента в конец списка."""
        new_node = Node(item)
        if self.head is None:
            self.head = new_node
            return

        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def append(self, item):
        """Алиас для append_right."""
        self.append_right(item)

    def remove(self, item):
        """Удаление элемента. Возбуждает ValueError, если элемент отсутствует."""
        if self.head is None:
            raise ValueError("Список пуст")

        if self.head.data == item:
            self.head = self.head.next
            return

        current = self.head
        while current.next:
            if current.next.data == item:
                current.next = current.next.next
                return
            current = current.next
        raise ValueError(f"Элемент '{item}' не найден в списке")

    def insert(self, previous, item):
        """Вставка элемента item после элемента previous."""
        if self.head is None:
            raise ValueError("Список пуст")

        new_node = Node(item)

        current = self.head
        while current:
            if current.data == previous:
                new_node.next = current.next
                current.next = new_node
                return
            current = current.next
        raise ValueError(f"Элемент '{previous}' не найден в списке")

    def last(self):
        """Получение последнего элемента списка."""
        if self.head is None:
            return None
        current = self.head
        while current.next:
            current = current.next
        return current.data

    def __len__(self):
        """Длина списка."""
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def __iter__(self):
        """Получение итератора."""
        self.current = self.head
        return self

    def __next__(self):
        """Получение следующего элемента."""
        if self.current is None:
            raise StopIteration
        item = self.current.data
        self.current = self.current.next
        return item

    def __getitem__(self, index):
        """Получение элемента по индексу."""
        if index < 0 or index >= len(self):
            raise IndexError("Индекс за пределами диапазона")

        count = 0
        current = self.head
        while current:
            if count == index:
                return current.data
            count += 1
            current = current.next

    def __contains__(self, item):
        """Поддержка оператора in."""
        current = self.head
        while current:
            if current.data == item:
                return True
            current = current.next
        return False

    def __reversed__(self):
        """Поддержка функции reversed."""
        reversed_list = LinkedList()
        current = self.head
        while current:
            reversed_list.append_left(current.data)
            current = current.next
        return reversed_list
