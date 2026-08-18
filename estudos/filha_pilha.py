from collections import deque
filas_tarefas = deque()
filas_tarefas.append("Analisar a imagem X")
filas_tarefas.append("Validar imagem Y")
filas_tarefas.append("Registrar resultado Z")

def adicionar_tarefa(fila,descricao):
    fila.append(descricao)

def atender_tarefa(fila):
    if not fila:
        return "Nenhuma tarefa pendente"
    return fila.popleft()

historico = []
historico.append("Cadastrou tarefa")
historico.append("Registrou a tarefa atendida")
historico.append("Concluiu tarefa")

def desfazer_ultima_acao(historico):
    if not historico:
        return "Nenhuma ação para desfazer"

    return historico.pop()

print(atender_tarefa(filas_tarefas))
print(atender_tarefa(filas_tarefas))
print(desfazer_ultima_acao(historico))
print(desfazer_ultima_acao(historico))