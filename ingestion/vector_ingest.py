from rag.vectorstore import create_vectorstore_from_domain

def atualizar_vectorstore(chat, caminho):
    from ingestion.loader import carregar_txt_para_chunks

    textos = carregar_txt_para_chunks(caminho)

    chat.db.add_texts(textos)