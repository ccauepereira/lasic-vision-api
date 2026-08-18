tarefas_pendentes = []

tarefas_pendentes.append("Tarefa 1")
tarefas_pendentes.append("Tarefa 2")
tarefas_pendentes.append("Tarefa 3")


print(tarefas_pendentes)

print(tarefas_pendentes [0])
print(tarefas_pendentes [-1])
print(len(tarefas_pendentes))

tarefas_pendentes.remove("Tarefa 2")
tarefa_concluida = tarefas_pendentes.pop()
print("A tarefa cocluida foi: " + tarefa_concluida)

def cadastrar_tarefa(tarefas, descricao):
    tarefas.append(descricao)
    return tarefas

tarefas = []
cadastrar_tarefa(tarefas,"Analisar imagem X")
cadastrar_tarefa(tarefas,"Validar imagem Y ")
cadastrar_tarefa(tarefas,"Registrar resultado Z")
print(tarefas)

def listar_tarefas(tarefas):
    for i in range(len(tarefas)):
        print(f"Tarefa {i + 1}: {tarefas[i]}")