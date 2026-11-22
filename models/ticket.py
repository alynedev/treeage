class Ticket:
    def __init__(self, title, description, ticket_id):
        if (
            ticket_id is None
            or not isinstance(ticket_id, int)
            or isinstance(ticket_id, bool)
            or ticket_id < 1
        ):
            raise ValueError("ticket_id deve ser um inteiro positivo.")
        self.id = ticket_id
        self.title = title
        self.description = description
        self.priority = None
        self.justification = None
        self.status = "Aberto"

    def __str__(self):
        return (
            f"Chamado: #{self.id}\n"
            f"Título: {self.title}\n"
            f"Descrição: {self.description}\n"
            f"Prioridade: {self.priority or 'Não Definida'}\n"
            f"Justificativa: {self.justification or 'Não definida'}\n"
            f"Status: {self.status}"
        )

    def para_dicionario(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "justification": self.justification,
            "status": self.status
        }

    @classmethod
    def do_dicionario(cls, data):
        ticket = cls(
            data["title"],
            data["description"],
            data["id"]
        )

        ticket.priority = data["priority"]
        ticket.justification = data["justification"]
        ticket.status = data["status"]

        return ticket
