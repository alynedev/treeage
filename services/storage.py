import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "tickets.json"

def gerar_proximo_id(ticket_list):
    next_id = 0
    for ticket in ticket_list.para_lista():
        if isinstance(ticket.id, int) and ticket.id > next_id:
            next_id = ticket.id
    return next_id + 1

def salvar_tickets(ticket_list):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    tickets = [
        ticket.para_dicionario()
        for ticket in ticket_list.para_lista()
    ]
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(tickets, file, ensure_ascii=False, indent=4)

def carregar_tickets():
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        conteudo = file.read().strip()
        if not conteudo:
            return []
        return json.loads(conteudo)
        