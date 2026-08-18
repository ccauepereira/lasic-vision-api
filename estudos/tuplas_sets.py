dimensao_imagem = (1920,1080)
largura, altura = dimensao_imagem

print(largura)
print(altura)

coordenada_pixel = (120,80)
x,y = coordenada_pixel
print(x)
print(y)

tags_imagem = set()
tags_imagem.add("celula")
tags_imagem.add("microscopia")
tags_imagem.add("analise")
tags_imagem.add("celula")

if "celula" in tags_imagem and "virus" in tags_imagem:
    print(tags_imagem)

def adicionar_tag(tags, nova_tag):
    if nova_tag in tags:
        return "Tag ja existe"

    tags.add(nova_tag)
    return "Tag adicionada"

print(adicionar_tag(tags_imagem, "celula"))
print(adicionar_tag(tags_imagem, "virus"))
print(tags_imagem)