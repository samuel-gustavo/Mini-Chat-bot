from tools.tools import ordenar_lista, soma_numeros

def executar_tool(nome, entrada):
    if nome == "ordenar_lista":
        return ordenar_lista(entrada)

    elif nome == "soma":
        return soma_numeros(entrada)

    return "Tool não encontrada"