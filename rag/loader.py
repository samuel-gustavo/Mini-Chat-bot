from langchain_community.document_loaders import TextLoader

def load_documents(path):
    loader = TextLoader(path)
    return loader.load()