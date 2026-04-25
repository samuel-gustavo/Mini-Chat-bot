import time
import re
from langchain_ollama import OllamaLLM
from config.settings import MODEL_NAME, MAX_TOKENS
from rag.retriever import retrieve_context
from memory.memory_store import get_memory, save_memory
from rag.vectorstore import create_vectorstore_from_domain
from memory.mysql_store import buscar_conhecimento
from tools.tool_executor import executar_tool


class ChatService:

    def __init__(self, domain):
        print("🚀 Inicializando ChatService...")

        self.llm = OllamaLLM(
            model=MODEL_NAME,
            num_predict=MAX_TOKENS,
            temperature=0.1
        )

        print("📦 Carregando vectorstore...")
        self.db = create_vectorstore_from_domain(domain)

        self.domain = domain

        # 🔥 carrega UMA VEZ só
        print("💾 Cache MySQL...")
        self.conhecimento_mysql = "\n".join(
            buscar_conhecimento(domain)
        )

        self.cache = {}

        print("✅ ChatService pronto!")

    def ask(self, user_id, question):
        start = time.time()

        # ⚡ CACHE
        if question in self.cache:
            print("⚡ Cache hit")
            return self.cache[question]

        # ⚡ TOOL DIRETA (sem IA)
        if "," in question and "ord" in question.lower():
            return executar_tool("ordenar_lista", question)

        if "," in question and "soma" in question.lower():
            return executar_tool("soma", question)

        # 🔍 contexto leve
        contexto = retrieve_context(self.db, question)
        contexto = contexto[:300]

        memoria = get_memory(user_id)

        # 🔥 PROMPT MINIMALISTA (CRÍTICO)
        prompt = f"""
Responda em português, curto.

Pergunta: {question}

Contexto: {contexto}
"""

        print("🤖 Gerando resposta...")
        resposta_completa = ""

        print("IA: ", end="", flush=True)

        for chunk in self.llm.stream(prompt):
            print(chunk, end="", flush=True)
            resposta_completa += chunk

        print()
        print()

        print(f"⏱️ Tempo total: {time.time() - start:.2f}s")

        # salvar memória leve
        if len(question) < 100:
            save_memory(user_id, f"P: {question}")
            save_memory(user_id, f"R: {resposta_completa}")

        self.cache[question] = resposta_completa

        return resposta_completa