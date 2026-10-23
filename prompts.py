from langchain_core.prompts import ChatPromptTemplate

from esquemas import parser
from ingesta import obtener_vectorstore
from retriever import crear_retriever

SISTEMA = """Eres un asistente técnico experto en fotografía analógica.
Responde SOLO con la información del CONTEXTO proporcionado.
No uses conocimiento propio ni completes con suposiciones.
Si la respuesta no está en el contexto, responde exactamente "No lo sé" y deja la lista de referencias vacía.
Si respondes, cita en referencias los nombres de los archivos que usaste.

{formato}"""

prompt = ChatPromptTemplate.from_messages([
    ("system", SISTEMA),
    ("human", "CONTEXTO:\n{contexto}\n\nPREGUNTA: {pregunta}"),
]).partial(formato=parser.get_format_instructions())


def formatear_contexto(docs):
    return "\n\n".join(
        f"[Fuente: {d.metadata['fuente']}]\n{d.page_content}" for d in docs
    )


if __name__ == "__main__":
    vectorstore = obtener_vectorstore()
    retriever = crear_retriever(vectorstore)

    pregunta = "¿Qué es la regla Sunny 16?"
    docs = retriever.invoke(pregunta)

    mensaje = prompt.invoke({
        "contexto": formatear_contexto(docs),
        "pregunta": pregunta,
    })
    print(mensaje.to_string())