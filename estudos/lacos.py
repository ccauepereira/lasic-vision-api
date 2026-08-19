for i in range(1,11):
    print(i)

for par in range(21):
    if par % 2 == 0:
        print(par)

for num in range(1, 6):
    print("Tarefa",num,"Cadastrada")

cont = 1
while cont <=5:
    print(cont)
    cont += 1

while True:
    nivel = int(input("Qual nivel do seu Python? Seja sincero (0 a 10): "))
    if nivel < 0 or nivel > 10:
        print("Invalido")
        continue

    if nivel >= 8:
        print("Avançado, parabens")
        break
    elif nivel >= 5:
        print("Intermediario, melhore")
        break
    else:
        print("SABE NADA, estude muito")    