import os
from langchain_community.document_loaders import TextLoader
from rag.splitter import split_documents

def carregar_txt_para_chunks(caminho):
    # pega o caminho da pasta do projeto (segundo_chat)
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    # monta caminho completo do arquivo
    file_path = os.path.join(BASE_DIR, caminho)

    print("📄 Carregando arquivo:", file_path)  # debug

    loader = TextLoader(file_path)
    docs = loader.load()

    chunks = split_documents(docs)

    return [chunk.page_content for chunk in chunks]