from structures.queue import Queue

class Triage:
    def __init__(self):
        self.high = Queue()
        self.medium = Queue()
        self.low = Queue()
        self.current_ticket = None

    def adicionar_ticket(self, ticket):
        if ticket.priority == "Alta":
            self.high.inserir(ticket)
        elif ticket.priority == "Média":
            self.medium.inserir(ticket)
        elif ticket.priority == "Baixa":
            self.low.inserir(ticket)
        else:
            raise ValueError("O chamado não possui prioridade válida.")

    def proximo_ticket(self):
        if not self.high.esta_vazia():
            return self.high.remover()
        elif not self.medium.esta_vazia():
            return self.medium.remover()
        elif not self.low.esta_vazia():
            return self.low.remover()
        return None

    def iniciar_ticket(self):
        if self.current_ticket is not None:
            return None
        ticket = self.proximo_ticket()
        if ticket is None:
            return None
        ticket.status = "Em atendimento"
        self.current_ticket = ticket
        return ticket

    def resolver_ticket(self):
        if self.current_ticket is None:
            return None
        ticket = self.current_ticket
        ticket.status = "Resolvido"
        self.current_ticket = None
        return ticket

    def reconstruir_filas(self, ticket_list):
        self.high = Queue()
        self.medium = Queue()
        self.low = Queue()
        self.current_ticket = None

        for ticket in ticket_list.para_lista():
            if ticket.status == "Aberto":
                self.adicionar_ticket(ticket)
            elif ticket.status == "Em atendimento" and self.current_ticket is None:
                self.current_ticket = ticket
                