from services.chat_service import ChatService
from memory.mysql_store import salvar_lote
from ingestion.mysql_ingest import ingerir_txt_mysql

user_id = "user_1"

modo = input("Deseja ingerir dados? (s/n): ")

if modo.lower() == "s":
    ingerir_txt_mysql("meus_textos.txt", "programacao")

print("👉 Cheguei aqui depois da ingestão")  # DEBUG

domain = "programacao"
chat = ChatService(domain)

print("🤖 Chat iniciado! Digite sua pergunta (ou 'sair').")

while True:
    pergunta = input("\nVocê: ")

    if pergunta.lower() in ["sair", "exit"]:
        print("Encerrando chat...")
        break

    print("⏳ Pensando...\n")
    resposta = chat.ask(user_id, pergunta)

    print("Juninho:", resposta)

    feedback = input("\nAvaliação (s/n ou Enter para pular): ")

    if feedback == "":
        continue

    if feedback == "s":
        if len(resposta) > 5:
            print("💾 Salvando resposta no banco...")
            salvar_lote(domain, [resposta])

            print("🧠 Atualizando memória vetorial...")
            # chat.db.add_texts([resposta])

            print("✅ Aprendizado salvo!")

    elif feedback == "n":
        correcao = input("Qual seria a resposta correta? ")

        if len(correcao) > 5:
            print("💾 Salvando correção no banco...")
            salvar_lote(domain, [correcao])

            print("🧠 Atualizando memória vetorial...")
            # chat.db.add_texts([correcao])

            print("✅ Correção salva!")