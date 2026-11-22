class Node:
    def __init__(self, ticket):
        self.ticket = ticket
        self.next = None

class Queue:
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

    def remover(self):
        if self.head is None:
            return None
        ticket = self.head.ticket
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self.size -= 1
        return ticket

    def ver_topo(self):
        if self.head is None:
            return None
        return self.head.ticket

    def esta_vazia(self):
        return self.head is None

    def para_lista(self):
        tickets = []
        current = self.head
        while current is not None:
            tickets.append(current.ticket)
            current = current.next
        return tickets