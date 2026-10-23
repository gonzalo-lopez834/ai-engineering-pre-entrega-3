import asyncio

from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI

from esquemas import parser
from ingesta import obtener_vectorstore
from prompts import prompt, formatear_contexto
from retriever import crear_retriever

llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", temperature=0)
retriever = crear_retriever(obtener_vectorstore())

cadena = (
    {
        "contexto": retriever | formatear_contexto,
        "pregunta": RunnablePassthrough(),
    }
    | prompt
    | llm
    | parser
)

async def get_rag_response(query: str):
    return await cadena.ainvoke(query)


if __name__ == "__main__":
    resultado = asyncio.run(get_rag_response("¿Qué es la regla Sunny 16?"))
    print(resultado.respuesta)
    print(resultado.referencias)