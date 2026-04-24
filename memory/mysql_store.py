import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="dev_iachat",
        password="dev_iachat",
        database="ia_conhecimentos"
    )

def salvar_lote(domain, textos):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO knowledge_base (domain, pergunta, resposta, avaliacao)
    VALUES (%s, %s, %s, %s)
    """

    dados = [(domain, texto, texto, "like") for texto in textos]

    print(f"💾 Inserindo {len(dados)} registros no banco...")

    cursor.executemany(query, dados)

    conn.commit()

    print("✅ Inserção finalizada!")

    cursor.close()
    conn.close()


def buscar_conhecimento(domain):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT pergunta, resposta 
    FROM knowledge_base 
    WHERE domain = %s AND avaliacao = 'like'
    """

    cursor.execute(query, (domain,))
    resultados = cursor.fetchall()

    cursor.close()
    conn.close()

    return [f"Pergunta: {p}\nResposta: {r}" for p, r in resultados]