import streamlit as st
from models.ticket import Ticket
from structures.linked_list import LinkedList
from structures.decision_tree import DecisionTree
from services.triage import Triage
from services.storage import carregar_tickets

st.set_page_config(
    page_title="Treeage | Histórico",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
    /* Campo de busca */
    [data-testid="stTextInput"] input {
        border-color: #3985F7;
    }

    [data-testid="stTextInput"] input:focus {
        border-color: #5D9BFA;
        box-shadow: 0 0 0 1px #3985F7;
    }

    /* Filtros */
    [data-testid="stSelectbox"] div[data-baseweb="select"] {
        border-color: #3985F7;
    }

    /* Total de chamados */
    [data-testid="stMetricValue"] {
        color: #5D9BFA;
    }

    /* Cards do histórico */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: #343943;
        border-radius: 12px;
    }

    /* Prioridade alta */
    [class*="st-key-card-"][class*="-prioridade-alta"] {
        border-color: #E05259;
    }

    /* Prioridade média */
    [class*="st-key-card-"][class*="-prioridade-media"] {
        border-color: #3985F7;
    }

    /* Prioridade baixa */
    [class*="st-key-card-"][class*="-prioridade-baixa"] {
        border-color: #36A875;
    }

    /* Títulos dos chamados */
    [data-testid="stVerticalBlockBorderWrapper"] h3 {
        color: #5D9BFA;
    }

    /* Mensagens de resultado */
    [data-testid="stAlert"] {
        border-radius: 10px;
    }

</style>
""", unsafe_allow_html=True)

# Inicialização dos dados da aplicação
if "ticket_list" not in st.session_state:
    ticket_list = LinkedList()
    saved_data = carregar_tickets()
    for data in saved_data:
        ticket = Ticket.do_dicionario(data)
        ticket_list.inserir(ticket)
    st.session_state.ticket_list = ticket_list
if "triage" not in st.session_state:
    triage = Triage()
    triage.reconstruir_filas(st.session_state.ticket_list)
    st.session_state.triage = triage
if "decision_tree" not in st.session_state:
    st.session_state.decision_tree = DecisionTree()

ticket_list = st.session_state.ticket_list
st.title("Histórico de Chamados")
st.caption("Consulte e localize todos os chamados já registrados")

st.divider()

tickets = ticket_list.para_lista()
st.metric("Total de chamados registrados", len(tickets))

# Campos de busca e filtro
coluna_busca, coluna_prioridade, coluna_status = st.columns([2, 1, 1])
with coluna_busca:
    busca = st.text_input(
        "Buscar chamado",
        placeholder="Pesquise por ID, título ou descrição..."
    )
with coluna_prioridade:
    prioridade_filtro = st.selectbox(
        "Filtrar por prioridade",
        ["Todas", "Alta", "Média", "Baixa"]
    )
with coluna_status:
    status_filtro = st.selectbox(
        "Filtrar por status",
        ["Todos", "Aberto", "Em atendimento", "Resolvido"]
    )

# Aplicação dos filtros
tickets_filtrados = tickets
if busca.strip():
    termo = busca.strip().lower()
    tickets_filtrados = [
        ticket
        for ticket in tickets_filtrados
        if (
            termo in str(ticket.id).lower()
            or termo in ticket.title.lower()
            or termo in ticket.description.lower()
        )
    ]
if prioridade_filtro != "Todas":
    tickets_filtrados = [
        ticket
        for ticket in tickets_filtrados
        if ticket.priority == prioridade_filtro
    ]
if status_filtro != "Todos":
    tickets_filtrados = [
        ticket
        for ticket in tickets_filtrados
        if ticket.status == status_filtro
    ]

st.divider()

# Exibição dos resultados
if not tickets:
    st.info("Ainda não existem chamados registrados.")
elif not tickets_filtrados:
    st.warning("Nenhum chamado encontrado com esses critérios.")
else:
    st.caption(
        f"Exibindo {len(tickets_filtrados)} de {len(tickets)} chamado(s)."
    )
    tickets_ordenados = list(reversed(tickets_filtrados))
    for i in range(0, len(tickets_ordenados), 2):
        colunas = st.columns(2)
        for coluna, ticket in zip(
            colunas,
            tickets_ordenados[i:i + 2]
        ):
            with coluna:
                chave_prioridade = {
                    "Alta": "prioridade-alta",
                    "Média": "prioridade-media",
                    "Baixa": "prioridade-baixa"
                }[ticket.priority]
                with st.container(key=f"card-{ticket.id}-{chave_prioridade}", border=True):
                    st.subheader(f"#{ticket.id} - {ticket.title}")
                    st.write(ticket.description)
                    cores_prioridade = {
                        "Alta": "#F06A70",
                        "Média": "#5D9BFA",
                        "Baixa": "#48C58B"
                    }
                    cor = cores_prioridade.get(ticket.priority, "#F2F2F2")
                    st.markdown(
                        f'**Prioridade:** <span style="color: {cor}; font-weight: 600;">'
                        f'{ticket.priority}</span>',
                        unsafe_allow_html=True
                    )
                    st.write(f"**Status:** {ticket.status}")
