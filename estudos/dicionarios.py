tarefa = {
    "id": 1,
    "descricao": "Analisar imagem X",
    "status": "concluida",
    "responsavel": "Cauê", 
}

print(tarefa["id"])
print(tarefa["descricao"])
print(tarefa["status"])
print(tarefa["responsavel"])

def mostrar_tarefa(tarefa):
    print(f"Tarefa: {tarefa['id']}: {tarefa['descricao']} | Stauts: {tarefa['status']}")

tarefas = []
tarefas.append({

    "task":"Analisar imagem X"
}
)
tarefas.append({
    "task":"Analisar celulas Y"
}
)

tarefas.append({
    "task":"Revisar imagem X e celulas Y"
}
)

for i in range(len(tarefas)):
    print(f"Task: {i+1}: {tarefas[i]['task']}")