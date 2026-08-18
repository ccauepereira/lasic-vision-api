class Tarefa:
    def __init__(self, tarefa_id: int, descricao: str):
        descricao_formatada = descricao.strip()

        if not descricao_formatada:
            raise ValueError("A descricao nao pode ser vazia")

        self.tarefa_id = tarefa_id
        self.descricao = descricao_formatada
        self.status = "pendente"
        self.responsavel = None
        self.tags = set()
        self.historico = []
        self.dados_imagem = {}

        self.historico.append("Tarefa criada")

    def atribuir_responsavel(self, nome: str):
        nome_formatado = nome.strip()

        if not nome_formatado:
            raise ValueError("O responsavel nao pode ser vazio")

        self.responsavel = nome_formatado
        self.historico.append(
            f"Responsavel atribuido: {nome_formatado}"
        )

    def adicionar_tag(self, tag: str):
        tag_formatada = tag.strip().lower()

        if not tag_formatada:
            raise ValueError("A tag nao pode ser vazia")

        if tag_formatada not in self.tags:
            self.tags.add(tag_formatada)
            self.historico.append(
                f"Tag adicionada: {tag_formatada}"
            )

    def registrar_dado(self, chave: str, valor):
        chave_formatada = chave.strip().lower()

        if not chave_formatada:
            raise ValueError("A chave nao pode ser vazia")

        self.dados_imagem[chave_formatada] = valor
        self.historico.append(
            f"Dado registrado: {chave_formatada}={valor}"
        )

    def iniciar(self):
        self.status = "em_andamento"
        self.historico.append(
            "Status alterado para em_andamento"
        )

    def concluir(self):
        self.status = "concluida"
        self.historico.append(
            "Status alterado para concluida"
        )

    def resumo(self) -> str:
        responsavel = self.responsavel or "Nao atribuido"

        tags_string = (
            ", ".join(sorted(self.tags))
            if self.tags
            else "Nenhuma"
        )

        dados_string = (
            str(self.dados_imagem)
            if self.dados_imagem
            else "Nenhum"
        )

        linhas = [
            f"ID: {self.tarefa_id}",
            f"Descricao: {self.descricao}",
            f"Status: {self.status}",
            f"Responsavel: {responsavel}",
            f"Tags: {tags_string}",
            f"Dados da imagem: {dados_string}",
            f"Historico: {len(self.historico)} registros",
        ]

        return "\n".join(linhas)