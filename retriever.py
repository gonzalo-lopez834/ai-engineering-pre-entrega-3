from ingesta import obtener_vectorstore


def crear_retriever(vectorstore, k: int = 4):
    return vectorstore.as_retriever(search_kwargs={"k": k})


if __name__ == "__main__":
    vectorstore = obtener_vectorstore()
    retriever = crear_retriever(vectorstore)

    pregunta = "¿Cuánto cuesta una Leica M6 hoy?"
    resultados = retriever.invoke(pregunta)

    for i, doc in enumerate(resultados, start=1):
        print(f"--- Resultado {i} | fuente: {doc.metadata['fuente']}")
        print(doc.page_content[:150])