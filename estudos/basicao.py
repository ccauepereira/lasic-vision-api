from .nivel_python import nivel_python


nome = "Cauê Pereira"
semestre_ccomp = 2
semestre_tecinfor = 3
bolsa_lasic = 700.0
estudando_python = True

print(nome)
print(semestre_ccomp)
print(semestre_tecinfor)
print(bolsa_lasic)
print(estudando_python)

if bolsa_lasic >= 700:
   print("Bolsa massa")
else:
   print("Bolsa nada massa")

if nivel_python >= 8:  
    print("Python avançado")
elif nivel_python >= 5: 
    print("Python basico")
else: 
    print("Python ruim")