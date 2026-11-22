class Node:
    def __init__(self, ticket):
        self.ticket = ticket
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def inserir(self, ticket):
        n = Node(ticket)
        if self.head is None:
            self.head = n
            self.tail = n
        else:
            self.tail.next = n
            self.tail = n
        self.size += 1

    def buscar(self, id):
        current = self.head
        while current is not None:
            if current.ticket.id == id:
                return current.ticket
            current = current.next
        return None

    def para_lista(self):
        tickets = []
        current = self.head
        while current is not None:
            tickets.append(current.ticket)
            current = current.next
        return tickets