import streamlit as st
from services.storage import salvar_tickets, carregar_tickets
from models.ticket import Ticket
from structures.linked_list import LinkedList
from structures.decision_tree import DecisionTree
from services.triage import Triage

st.set_page_config(
    page_title="Treeage | Chamados Atuais",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
    /* Coluna de alta prioridade */
    .st-key-prioridade-alta {
        border: 1px solid #E05259;
        border-radius: 12px;
        padding: 12px;
    }

    .st-key-prioridade-alta h3 {
        color: #F06A70;
    }

    /* Coluna de média prioridade */
    .st-key-prioridade-media {
        border: 1px solid #3985F7;
        border-radius: 12px;
        padding: 12px;
    }

    .st-key-prioridade-media h3 {
        color: #5D9BFA;
    }

    /* Coluna de baixa prioridade */
    .st-key-prioridade-baixa {
        border: 1px solid #36A875;
        border-radius: 12px;
        padding: 12px;
    }

    .st-key-prioridade-baixa h3 {
        color: #48C58B;
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
triage = st.session_state.triage
st.title("Chamados Atuais")
st.caption("Acompanhe os chamados pendentes e em atendimento") 

st.divider()

# Chamado em atendimento
st.header("Em atendimento")
if triage.current_ticket is None:
    st.info("Nenhum chamado está em atendimento.")
else:
    ticket = triage.current_ticket
    with st.container(border=True):
        st.subheader(f"#{ticket.id} - {ticket.title}")
        st.write(ticket.description)
        st.write(f"**Prioridade:** {ticket.priority}")
        if st.button("Resolver chamado", type="primary"):
            resolvido = triage.resolver_ticket()
            salvar_tickets(ticket_list)
            st.success(f"Chamado #{resolvido.id} resolvido!")
            st.rerun()

st.divider()

# Filas organizadas em colunas
st.header("Aguardando atendimento")
coluna_alta, coluna_media, coluna_baixa = st.columns(3)
filas = [
    (coluna_alta, "Alta", triage.high),
    (coluna_media, "Média", triage.medium),
    (coluna_baixa, "Baixa", triage.low)
]

for coluna, prioridade, fila in filas:
    with coluna:
        chave = {
            "Alta": "prioridade-alta",
            "Média": "prioridade-media",
            "Baixa": "prioridade-baixa"
        }[prioridade]
        with st.container(key=chave):
            tickets = fila.para_lista()
            st.subheader(prioridade)
            st.caption(f"{len(tickets)} chamado(s)")
            if not tickets:
                st.caption("Fila vazia.")
            else:
                for ticket in tickets:
                    with st.container(border=True):
                        st.markdown(f"**#{ticket.id}**")
                        st.markdown(f"**{ticket.title}**")

                        st.write(ticket.description)

                        st.caption(
                            f"Status: {ticket.status}"
                        )

st.divider()

# Iniciar próximo chamado
if triage.current_ticket is not None:
    st.button(
        "Iniciar próximo chamado",
        disabled=True,
        use_container_width=True,
        help="Resolva o chamado atual antes de iniciar outro."
    )
else:
    if st.button(
        "Iniciar próximo chamado",
        type="primary",
        use_container_width=True
    ):
        ticket = triage.iniciar_ticket()
        if ticket is None:
            st.warning("Não existem chamados aguardando atendimento.")
        else:
            salvar_tickets(ticket_list)
        st.rerun()
