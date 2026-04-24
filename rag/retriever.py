from config.settings import TOP_K

def retrieve_context(db, pergunta, k=2):
    resultados = db.similarity_search(pergunta, k=k)
    return "\n".join([doc.page_content for doc in resultados])