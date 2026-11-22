import streamlit as st
from models.ticket import Ticket
from structures.linked_list import LinkedList
from structures.decision_tree import DecisionTree
from services.triage import Triage
from services.storage import carregar_tickets, salvar_tickets, gerar_proximo_id

st.set_page_config(
    page_title="Treeage | Cadastro",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
    /* Botão de iniciar triagem */
    [data-testid="stFormSubmitButton"] button {
        background-color: #3985F7;
        color: white;
        border: 1px solid #3985F7;
    }

    [data-testid="stFormSubmitButton"] button:hover {
        background-color: #2569D8;
        border-color: #2569D8;
        color: white;
    }

    /* Botão Sim: contorno verde */
    .st-key-resposta-sim button {
        background-color: transparent;
        color: #48C58B;
        border: 1px solid #36A875;
    }

    .st-key-resposta-sim button:hover {
        background-color: rgba(54, 168, 117, 0.12);
        color: #65D9A4;
        border-color: #48C58B;
    }

    /* Botão Não: contorno vermelho */
    .st-key-resposta-nao button {
        background-color: transparent;
        color: #F06A70;
        border: 1px solid #E05259;
    }

    .st-key-resposta-nao button:hover {
        background-color: rgba(224, 82, 89, 0.12);
        color: #FF858A;
        border-color: #F06A70;
    }

    /* Resultado da prioridade */
    .st-key-prioridade-alta [data-testid="stMetricValue"] {
        color: #F06A70;
    }

    .st-key-prioridade-media [data-testid="stMetricValue"] {
        color: #5D9BFA;
    }

    .st-key-prioridade-baixa [data-testid="stMetricValue"] {
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

# Inicialização da triagem
if "caminho_triagem" not in st.session_state:
    st.session_state.caminho_triagem = []
if "titulo_chamado" not in st.session_state:
    st.session_state.titulo_chamado = ""
if "descricao_chamado" not in st.session_state:
    st.session_state.descricao_chamado = ""
if "triagem_iniciada" not in st.session_state:
    st.session_state.triagem_iniciada = False

# Mensagem de confirmação do cadastro
cadastro_ticket_id = st.session_state.pop(
    "cadastro_ticket_id", None
)
if cadastro_ticket_id is not None:
    st.success(f"Chamado #{cadastro_ticket_id} cadastrado com sucesso!")

# Cabeçalho
st.title("Treeage")
st.caption("Sistema de triagem e gerenciamento de chamados")

st.divider()

st.header("Cadastro de chamados")
st.write(
    "Descreva o problema que você está enfrentando. "
    "Em seguida, responda às perguntas para determinar "
    "a prioridade do chamado."
)

# Formulário 
if not st.session_state.triagem_iniciada:
    with st.form("formulario_chamado"):
        titulo = st.text_input(
            "Título do chamado",
            placeholder="Ex.: Computador não liga"
        )
        descricao = st.text_area(
            "Descrição do problema",
            placeholder="Descreva o problema com mais detalhes...",
            height=150
        )
        enviar = st.form_submit_button(
            "Iniciar triagem",
            use_container_width=True,
            type="primary"
        )
        if enviar:
            if not titulo.strip() or not descricao.strip():
                st.error("Preencha o título e a descrição do chamado.")
            else:
                st.session_state.titulo_chamado = titulo.strip()
                st.session_state.descricao_chamado = descricao.strip()
                st.session_state.caminho_triagem = []
                st.session_state.triagem_iniciada = True
                st.rerun()

# Perguntas 
if st.session_state.triagem_iniciada:
    st.divider()
    st.subheader("Triagem do chamado")
    st.markdown(
        f"**Chamado:** {st.session_state.titulo_chamado}"
    )
    st.write(st.session_state.descricao_chamado)
    arvore = st.session_state.decision_tree
    caminho = st.session_state.caminho_triagem
    pergunta = arvore.obter_pergunta(caminho)

    if pergunta is not None:
        numero_pergunta = len(caminho) + 1
        st.progress(
            min(len(caminho) / 4, 1.0),
            text=f"Pergunta {numero_pergunta}"
        )
        st.markdown(f"### {pergunta}")
        with st.container(key="respostas-triagem"):
            coluna_sim, coluna_nao = st.columns(2)
            with coluna_sim:
                with st.container(key="resposta-sim"):
                    if st.button("Sim", use_container_width=True):
                        caminho.append(True)
                        st.rerun()
            with coluna_nao:
                with st.container(key="resposta-nao"):
                    if st.button("Não", use_container_width=True):
                        caminho.append(False)
                        st.rerun()
    else:
        prioridade, justificativa = arvore.obter_resultado(caminho)
        chave_prioridade = {
            "Alta": "prioridade-alta",
            "Média": "prioridade-media",
            "Baixa": "prioridade-baixa"
        }[prioridade]
        with st.container(key=chave_prioridade):
            st.metric("Prioridade definida", prioridade)
        st.info(justificativa)
        st.write(
            "Confira o resultado e confirme o cadastro do chamado."
        )
        coluna_confirmar, coluna_reiniciar = st.columns(2)
        with coluna_confirmar:
            if st.button(
                "Confirmar cadastro",
                use_container_width=True,
                type="primary"
            ):
                proximo_id = gerar_proximo_id(st.session_state.ticket_list)
                ticket = Ticket(
                    st.session_state.titulo_chamado,
                    st.session_state.descricao_chamado,
                    ticket_id=proximo_id
                )
                ticket.priority = prioridade
                ticket.justification = justificativa
                st.session_state.ticket_list.inserir(ticket)
                st.session_state.triage.adicionar_ticket(ticket)
                salvar_tickets(st.session_state.ticket_list)
                st.session_state.cadastro_ticket_id = ticket.id
                st.session_state.titulo_chamado = ""
                st.session_state.descricao_chamado = ""
                st.session_state.caminho_triagem = []
                st.session_state.triagem_iniciada = False
                st.rerun()
        with coluna_reiniciar:
            if st.button(
                "Reiniciar cadastro",
                use_container_width=True
            ):
                st.session_state.titulo_chamado = ""
                st.session_state.descricao_chamado = ""
                st.session_state.caminho_triagem = []
                st.session_state.triagem_iniciada = False
                st.rerun()
                