nivel = input("Digite o nivel em Python (0 a 10)")
bolsa = input("Digite o valor da bolsa: ")

if nivel < 0 or nivel > 10:
    print("Invalido")
elif nivel >= 8:
    print("Avançado")
elif nivel >= 5:
    print("Intermediario")
else:
    print("iniciante")

if bolsa >= 700:
    print("Interessante")
else:
    print("Nada massa")