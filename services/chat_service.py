import time
import re
from langchain_ollama import OllamaLLM
from config.settings import MODEL_NAME, MAX_TOKENS, TEMPERATURE
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
            temperature=TEMPERATURE
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
        contexto = limitar_texto(contexto, limite=800)

        memoria = get_memory(user_id)

        # 🔥 PROMPT MINIMALISTA (CRÍTICO)
        prompt = f"""
Responda em português do Brasil.

Dê uma resposta completa e finalize totalmente o raciocínio.
Responda de uma forma Normal, interpretando falas.

Se for explicação:
- explique
- conclua com uma frase final clara

Se for passo a passo:
- vá até o último passo

Nunca pare no meio da frase.

Finalize sua resposta com:
[FIM]

Pergunta: {question}

Contexto:
{contexto}
"""

        print("🤖 Gerando resposta...")
        resposta_completa = ""

        print("IA: ", end="", flush=True)
        buffer = ""

        for chunk in self.llm.stream(prompt):
            buffer += chunk

            # 🔥 detecta marcador mesmo quebrado
            if "[FIM]" in buffer:
                parte = buffer.split("[FIM]")[0]

                print(parte, end="", flush=True)
                resposta_completa += parte
                break

            # 🔥 mantém buffer pequeno (evita duplicação)
            if len(buffer) > 10:
                print(buffer[:-5], end="", flush=True)
                resposta_completa += buffer[:-5]
                buffer = buffer[-5:]  # guarda só o final

        # limpeza final
        resposta_completa = resposta_completa.replace("[FIM]", "").strip()

        print("\n")

        print(f"⏱️ Tempo total: {time.time() - start:.2f}s")

        # salvar memória leve
        if len(question) < 100:
            save_memory(user_id, f"P: {question}")
            save_memory(user_id, f"R: {resposta_completa}")

        self.cache[question] = resposta_completa

        return resposta_completa

def limitar_texto(texto, limite=500):
    if len(texto) <= limite:
        return texto
    
    # corta até o último ponto final antes do limite
    corte = texto[:limite].rsplit(".", 1)[0]
    return corte + "."