import asyncio

from rag import get_rag_response

PRUEBAS = [
    ("EN LOS DOCUMENTOS", "¿A qué temperatura se revela la película de color con el proceso C-41?"),
    ("TRAMPA DIFÍCIL", "¿Cuánto cuesta una Leica M6 hoy?"),
    ("TRAMPA FÁCIL", "¿Cuál es la capital de Francia?"),
]


async def main():
    for tipo, pregunta in PRUEBAS:
        resultado = await get_rag_response(pregunta)
        print(f"=== {tipo} ===")
        print(f"Pregunta: {pregunta}")
        print(f"Respuesta: {resultado.respuesta}")
        print(f"Referencias: {resultado.referencias}")
        print()


if __name__ == "__main__":
    asyncio.run(main())