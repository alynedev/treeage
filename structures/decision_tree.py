class TreeNode:
    def __init__(self, question=None, result=None, justification=None):
        self.question = question
        self.result = result
        self.justification = justification
        self.yes = None
        self.no = None

class DecisionTree:
    def __init__(self):
        self.root = TreeNode(
            question="Existe suspeita de incidente de segurança ou perda/corrupção de dados?"
        )
        self.root.no = TreeNode(
            question="O problema afeta várias pessoas ou setores?"
        )
        self.root.no.yes = TreeNode(
            question="Um serviço ou sistema essencial está totalmente indisponível?"
        )
        self.root.no.no = TreeNode(
            question="Um serviço ou sistema essencial está totalmente indisponível?"
        )
        self.root.no.no.yes = TreeNode(
            question="Existe alguma alternativa para continuar a atividade?"
        )

        self.root.yes = TreeNode(
            result="Alta",
            justification="O chamado envolve possível comprometimento da segurança ou da integridade dos dados."
        )
        self.root.no.yes.yes = TreeNode(
            result="Alta",
            justification="Um serviço essencial está totalmente indisponível e afeta várias pessoas ou setores."
        )
        self.root.no.yes.no = TreeNode(
            result="Média",
            justification="O problema afeta várias pessoas ou setores, mas não causa indisponibilidade total de um serviço essencial."
        )
        self.root.no.no.yes.no = TreeNode(
            result="Média",
            justification="Uma atividade essencial foi completamente bloqueada para o usuário/setor e não existe alternativa disponível."
        )
        self.root.no.no.yes.yes = TreeNode(
            result="Baixa",
            justification="A atividade foi bloqueada, mas existe uma alternativa para sua continuidade."
        )
        self.root.no.no.no = TreeNode(
            result="Baixa",
            justification="O problema não bloqueia completamente uma atividade essencial."
        )

    def obter_no(self, path):
        current = self.root
        for result in path:
            if current is None or current.result is not None:
                break
            if result:
                current = current.yes
            else:
                current = current.no
        return current

    def obter_pergunta(self, path):
        current = self.obter_no(path)
        if current is None or current.result is not None:
            return None
        return current.question

    def obter_resultado(self, path):
        current = self.obter_no(path)
        if current is None or current.result is None:
            return None
        return current.result, current.justification
