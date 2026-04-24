from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

def create_vectorstore_from_domain(domain):
    embeddings = OllamaEmbeddings(model="mistral")

    print("📂 Carregando base vetorial existente...")

    return Chroma(
        persist_directory=f"./chroma_{domain}",
        embedding_function=embeddings
    )