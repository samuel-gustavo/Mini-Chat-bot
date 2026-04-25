import re

def ordenar_lista(texto):
    try:
        texto = texto.lower()

        if ":" in texto:
            texto = texto.split(":", 1)[1]

        texto = re.sub(r"(ordene|organize|ordenar|coloque em ordem|lista)", "", texto)

        itens = [i.strip() for i in texto.split(",") if i.strip()]

        return sorted(itens)
    except:
        return "Erro ao ordenar lista"


def soma_numeros(texto):
    try:
        if ":" in texto:
            texto = texto.split(":", 1)[1]

        nums = [float(n.strip()) for n in texto.split(",") if n.strip()]
        return sum(nums)
    except:
        return "Erro ao somar"