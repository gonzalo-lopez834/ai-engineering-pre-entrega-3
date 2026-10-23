from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

CARPETA_DB = "./vectorstore"
COLECCION = "camaras"


def cargar_y_fragmentar(carpeta: str):
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=500,
        chunk_overlap=50,
    )

    documentos = []
    for ruta in Path(carpeta).glob("*.txt"):
        texto = ruta.read_text(encoding="utf-8")
        trozos = splitter.create_documents(
            [texto],
            metadatas=[{"fuente": ruta.name}],
        )
        documentos.extend(trozos)

    return documentos


def obtener_vectorstore():
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

    vectorstore = Chroma(
        collection_name=COLECCION,
        embedding_function=embeddings,
        persist_directory=CARPETA_DB,
    )

    if vectorstore._collection.count() == 0:
        print("Base vacía; indexando...")
        docs = cargar_y_fragmentar("data")
        vectorstore.add_documents(docs)
        print(f"Indexados {len(docs)} chunks")
    else:
        print("La base ya existe, no se reindexa")

    return vectorstore


if __name__ == "__main__":
    vectorstore = obtener_vectorstore()
    print(f"Chunks en la base: {vectorstore._collection.count()}")