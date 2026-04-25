def retrieve_context(db, pergunta, k=1):
    resultados = db.similarity_search(pergunta, k=k)

    # 🔥 limita tamanho do texto
    return "\n".join([doc.page_content[:200] for doc in resultados])