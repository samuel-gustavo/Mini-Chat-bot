from ingestion.loader import carregar_txt_para_chunks
from memory.mysql_store import salvar_lote

def ingerir_txt_mysql(caminho, domain):
    print("🚀 Iniciando ingestão...")

    textos = carregar_txt_para_chunks(caminho)

    print(f"📄 Total de chunks: {len(textos)}")

    # 💾 SALVA NO MYSQL
    salvar_lote(domain, textos)

    print("🎉 Ingestão concluída!")