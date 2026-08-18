class Tarefa:
    def __init__(self,tarefa_id,descricao):
        self.tarefa_id = tarefa_id
        self.descricao = descricao
        self.status = "pendente"
        self.responsavel = None
        self.tags = set()

def atribuir_responsavel(self, nome:str):
    self.responsavel = nome

def adicionar_tag(self,tag: str):
        self.tags.append(tag)

def resumo(self):
    responsavel = self.responsavel or "Nao atribuido"
    tags = ", ".join(sorted(self.tags)) if self.tags else "Nenhuma"

    return(
         f"Tarefa: {self.tarefa_id}: {self.descricao}"
         f"Status: {self.status} |"
         f"Responsavel: {responsavel} |"
         f"Tags: {tags}"
    )

tarefa = Tarefa(1,"Analisar imagem X")
tarefa.atribuir_responsavel("Cauê")
tarefa.adicionar_tag("Celula")
tarefa.adicionar_tag("microscopio")
tarefa.concluir()

print(tarefa.resumo())