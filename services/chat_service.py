import time
from langchain_ollama import OllamaLLM
from config.settings import MODEL_NAME
from rag.retriever import retrieve_context
from memory.memory_store import get_memory, save_memory
from rag.vectorstore import create_vectorstore_from_domain

class ChatService:

    def __init__(self, domain):
        print("🚀 Inicializando ChatService...")

        self.llm = OllamaLLM(model=MODEL_NAME)

        print("📦 Carregando vectorstore...")
        self.db = create_vectorstore_from_domain(domain)

        self.domain = domain

        print("✅ ChatService pronto!")

    def ask(self, user_id, question):
        start = time.time()

        print("🔍 Buscando contexto...")
        contexto = retrieve_context(self.db, question, k=2)
        print(f"⏱️ Contexto em {time.time() - start:.2f}s")

        memoria = get_memory(user_id)

        prompt = f"""
        Você é um especialista em {self.domain}.

        Use o contexto abaixo para responder.
        Se não souber, diga "não sei".

        Contexto:
        {contexto}

        Memória:
        {memoria}

        Pergunta: {question}
        """

        print("🤖 Gerando resposta...")
        resposta = self.llm.invoke(prompt)

        print(f"⏱️ Resposta em {time.time() - start:.2f}s\n")

        save_memory(user_id, f"Pergunta: {question}")
        save_memory(user_id, f"Resposta: {resposta}")

        return resposta