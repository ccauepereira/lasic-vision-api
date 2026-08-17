def mostrar_boas_vindas():
    return "Bem-vindo ao LASIC VISION API"

def classificar_bolsa(valor_bolsa):
    if valor_bolsa < 0:
        return "Valor invalido"
    elif valor_bolsa >= 700:
        return "Bolsa interessante"
    elif valor_bolsa >= 400:
        return "Bolsa +/-"
    else:
        return "Bolsa baixa"

def classificar_nivel_python(nivel_python):
    if nivel_python < 0 or nivel_python > 10:
        return "invalido"
    if nivel_python >= 8:
        return "Avançado"
    elif nivel_python >= 5:
        return "Intermediario"
    else:
        return "Iniciante"

def criar_mensagem_tarefa(numero_tarefa):
    return f"Tarefa {numero_tarefa} cadastrada"  

print(mostrar_boas_vindas())
print(classificar_bolsa(700))
print(classificar_bolsa(300))
print(classificar_nivel_python(8))
print(classificar_nivel_python(4))
print(criar_mensagem_tarefa(3))