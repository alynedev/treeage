# Treeage

Sistema interativo de triagem e gerenciamento de chamados de suporte técnico, desenvolvido com estruturas de dados implementadas do zero (Árvore Binária de Decisão, Filas Encadeadas e Lista Encadeada).

## 🚀 Demonstração

[Live Demo - Treeage](#)

## 📌 Funcionalidades

- Triagem guiada de chamados com Árvore Binária de Decisão (`Alta`, `Média` e `Baixa`) e justificativa automática
- Priorização de atendimento com múltiplas filas encadeadas respeitando ordem FIFO dentro de cada nível
- Controle do ciclo de vida do chamado (`Aberto`, `Em atendimento` e `Resolvido`)
- Histórico completo armazenado em Lista Encadeada com busca por ID, título ou descrição e filtros por prioridade e status
- Persistência local em JSON com reconstrução automática das filas ao iniciar a aplicação
- Suíte de testes automatizados cobrindo casos representativos e situações limite

## 🛠️ Tecnologias Utilizadas

- Python
- Streamlit
- JSON (persistência de dados)
- `unittest` (testes automatizados)
- Estruturas de dados próprias (`DecisionTree`, `Queue` e `LinkedList`)

## 📈 Melhorias Futuras

- Classificação automática da categoria do chamado (_redes, manutenção, software_, etc.) usando Aprendizado de Máquina / NLP a partir de palavras-chave
- Sistema de autenticação e separação de perfis (solicitante e técnico)
- Migração da persistência em JSON para banco de dados com suporte a múltiplos atendimentos simultâneos
- Índice auxiliar com Tabela Hash para busca por ID em tempo $O(1)$ médio e política de _aging_ para evitar _starvation_
- Suporte a versão em inglês

## 💻 Como Executar

1. Instale as dependências necessárias:

```bash
pip install streamlit
```

2. Execute a aplicação na raiz do projeto:

```bash
streamlit run Cadastro.py
```

Os chamados cadastrados são salvos automaticamente em `data/tickets.json`.

## 🧪 Executando os Testes

O repositório inclui uma suíte com 18 testes unitários validando a árvore de decisão, filas, lista encadeada, geração de IDs e persistência.

Para rodar todos os testes, execute na raiz do projeto:

```bash
python -m unittest discover -s tests -v
```
