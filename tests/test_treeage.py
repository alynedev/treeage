import sys
from pathlib import Path
import tempfile
import unittest
from models.ticket import Ticket
from services import storage
from services.triage import Triage
from structures.decision_tree import DecisionTree
from structures.linked_list import LinkedList
from structures.queue import Queue

# rodar testes: python -m unittest discover -s tests -v

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

class TestDecisionTree(unittest.TestCase):
    def setUp(self):
        self.tree = DecisionTree()

    def test_caminho_vazio_retorna_pergunta_raiz_e_sem_resultado(self):
        pergunta = self.tree.obter_pergunta([])
        self.assertIsNotNone(pergunta)
        self.assertIn("segurança", pergunta.lower())
        self.assertIsNone(self.tree.obter_resultado([]))

    def test_poda_imediata_incidente_seguranca_prioridade_alta(self):
        caminho = [True]
        self.assertIsNone(self.tree.obter_pergunta(caminho))
        prioridade, justificativa = self.tree.obter_resultado(caminho)
        self.assertEqual(prioridade, "Alta")
        self.assertTrue(len(justificativa) > 0)

    def test_coletivo_indisponibilidade_total_prioridade_alta(self):
        caminho = [False, True, True]
        self.assertIsNone(self.tree.obter_pergunta(caminho))
        prioridade, _ = self.tree.obter_resultado(caminho)
        self.assertEqual(prioridade, "Alta")

    def test_coletivo_sem_indisponibilidade_total_prioridade_media(self):
        caminho = [False, True, False]
        prioridade, _ = self.tree.obter_resultado(caminho)
        self.assertEqual(prioridade, "Média")

    def test_individual_bloqueio_sem_alternativa_prioridade_media(self):
        caminho = [False, False, True, False]
        prioridade, _ = self.tree.obter_resultado(caminho)
        self.assertEqual(prioridade, "Média")

    def test_individual_bloqueio_com_alternativa_prioridade_baixa(self):
        caminho = [False, False, True, True]
        prioridade, _ = self.tree.obter_resultado(caminho)
        self.assertEqual(prioridade, "Baixa")

    def test_individual_sem_bloqueio_essencial_prioridade_baixa(self):
        caminho = [False, False, False]
        prioridade, _ = self.tree.obter_resultado(caminho)
        self.assertEqual(prioridade, "Baixa")

    def test_caminho_com_passos_extras_apos_folha(self):
        caminho = [True, True, False]
        self.assertIsNone(self.tree.obter_pergunta(caminho))
        prioridade, _ = self.tree.obter_resultado(caminho)
        self.assertEqual(prioridade, "Alta")

class TestQueueAndTriage(unittest.TestCase):
    def test_fila_vazia_limites(self):
        fila = Queue()
        self.assertTrue(fila.esta_vazia())
        self.assertIsNone(fila.ver_topo())
        self.assertIsNone(fila.remover())
        self.assertEqual(fila.size, 0)
        self.assertEqual(fila.para_lista(), [])

    def test_fila_com_um_elemento_e_remocao(self):
        fila = Queue()
        t1 = Ticket("Unico", "Descricao", ticket_id=1)
        fila.inserir(t1)
        self.assertFalse(fila.esta_vazia())
        self.assertEqual(fila.size, 1)
        self.assertEqual(fila.ver_topo(), t1)
        self.assertIsNotNone(fila.head)
        self.assertIsNotNone(fila.tail)

        removido = fila.remover()
        self.assertEqual(removido, t1)
        self.assertTrue(fila.esta_vazia())
        self.assertEqual(fila.size, 0)
        self.assertIsNone(fila.head)
        self.assertIsNone(fila.tail)

    def test_hierarquia_prioridades_e_fifo_por_nivel(self):
        triage = Triage()
        b1 = Ticket("Baixa 1", "Desc", ticket_id=1)
        b1.priority = "Baixa"
        m1 = Ticket("Media 1", "Desc", ticket_id=2)
        m1.priority = "Média"
        a1 = Ticket("Alta 1", "Desc", ticket_id=3)
        a1.priority = "Alta"
        m2 = Ticket("Media 2", "Desc", ticket_id=4)
        m2.priority = "Média"
        a2 = Ticket("Alta 2", "Desc", ticket_id=5)
        a2.priority = "Alta"

        for t in (b1, m1, a1, m2, a2):
            triage.adicionar_ticket(t)
        ordem_esperada = [a1, a2, m1, m2, b1]
        ordem_obtida = []

        while True:
            iniciado = triage.iniciar_ticket()
            if iniciado is None:
                break
            self.assertEqual(iniciado.status, "Em atendimento")
            self.assertIsNone(triage.iniciar_ticket())
            ordem_obtida.append(iniciado)

            resolvido = triage.resolver_ticket()
            self.assertEqual(resolvido, iniciado)
            self.assertEqual(resolvido.status, "Resolvido")

        self.assertEqual(ordem_obtida, ordem_esperada)
        self.assertIsNone(triage.iniciar_ticket())
        self.assertIsNone(triage.resolver_ticket())

    def test_prioridade_invalida_levanta_value_error(self):
        triage = Triage()
        t = Ticket("Invalido", "Desc", ticket_id=1)
        t.priority = "Urgentíssima"
        with self.assertRaises(ValueError):
            triage.adicionar_ticket(t)

    def test_reconstruir_filas_com_varios_status(self):
        lista = LinkedList()

        t_aberto_baixa = Ticket("Aberto Baixa", "D", ticket_id=1)
        t_aberto_baixa.priority = "Baixa"
        t_aberto_baixa.status = "Aberto"

        t_resolvido = Ticket("Resolvido", "D", ticket_id=2)
        t_resolvido.priority = "Alta"
        t_resolvido.status = "Resolvido"

        t_em_atendimento = Ticket("Em curso", "D", ticket_id=3)
        t_em_atendimento.priority = "Média"
        t_em_atendimento.status = "Em atendimento"

        t_aberto_alta = Ticket("Aberto Alta", "D", ticket_id=4)
        t_aberto_alta.priority = "Alta"
        t_aberto_alta.status = "Aberto"

        for t in (t_aberto_baixa, t_resolvido, t_em_atendimento, t_aberto_alta):
            lista.inserir(t)
        triage = Triage()
        triage.reconstruir_filas(lista)

        self.assertEqual(triage.current_ticket, t_em_atendimento)
        self.assertEqual(triage.high.para_lista(), [t_aberto_alta])
        self.assertEqual(triage.medium.para_lista(), [])
        self.assertEqual(triage.low.para_lista(), [t_aberto_baixa])

class TestLinkedListTicketAndStorage(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_data_file = storage.DATA_FILE
        storage.DATA_FILE = Path(self.temp_dir.name) / "tickets.json"

    def tearDown(self):
        storage.DATA_FILE = self.original_data_file
        self.temp_dir.cleanup()

    def test_ticket_id_invalido(self):
        for invalido in (None, 0, -3, "1", True, False):
            with self.assertRaises(ValueError):
                Ticket("Titulo", "Descricao", ticket_id=invalido)

    def test_linked_list_busca_inicio_meio_fim_e_inexistente(self):
        lista = LinkedList()
        self.assertIsNone(lista.buscar(1))
        t1 = Ticket("Primeiro", "D1", ticket_id=10)
        t2 = Ticket("Meio", "D2", ticket_id=20)
        t3 = Ticket("Ultimo", "D3", ticket_id=30)

        for t in (t1, t2, t3):
            lista.inserir(t)

        self.assertEqual(lista.size, 3)
        self.assertEqual(lista.buscar(10), t1)
        self.assertEqual(lista.buscar(20), t2)
        self.assertEqual(lista.buscar(30), t3)
        self.assertIsNone(lista.buscar(999))

    def test_gerar_proximo_id_lista_vazia_e_ids_fora_de_ordem(self):
        lista = LinkedList()
        self.assertEqual(storage.gerar_proximo_id(lista), 1)

        lista.inserir(Ticket("A", "D", ticket_id=5))
        lista.inserir(Ticket("B", "D", ticket_id=2))
        lista.inserir(Ticket("C", "D", ticket_id=9))
        self.assertEqual(storage.gerar_proximo_id(lista), 10)

    def test_storage_arquivo_inexistente_e_vazio(self):
        self.assertEqual(storage.carregar_tickets(), [])
        storage.DATA_FILE.write_text("   \n  ", encoding="utf-8")
        self.assertEqual(storage.carregar_tickets(), [])

    def test_salvar_e_carregar_acentos_e_caracteres_especiais(self):
        lista = LinkedList()
        t = Ticket(
            "Computador não liga — setor financeiro",
            "Falha com acentuação: ç, ã, é, ô e aspas 'simples' / \"duplas\".",
            ticket_id=1
        )

        t.priority = "Alta"
        t.justification = "Justificativa com acentos."
        lista.inserir(t)
        storage.salvar_tickets(lista)
        carregados = storage.carregar_tickets()
        self.assertEqual(len(carregados), 1)
        reconstruido = Ticket.do_dicionario(carregados[0])
        
        self.assertEqual(reconstruido.id, 1)
        self.assertEqual(reconstruido.title, t.title)
        self.assertEqual(reconstruido.description, t.description)
        self.assertEqual(reconstruido.priority, "Alta")
        self.assertEqual(reconstruido.status, "Aberto")

if __name__ == "__main__":
    unittest.main()
    