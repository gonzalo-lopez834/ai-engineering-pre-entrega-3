from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser


class RespuestaRAG(BaseModel):
    respuesta: str = Field(
        description="Respuesta a la pregunta, basada solo en el contexto"
    )
    referencias: list[str] = Field(
        description="Nombres de los archivos fuente usados para responder. "
        "Si no sabes la respuesta, devuelve una lista vacía."
    )


parser = PydanticOutputParser(pydantic_object=RespuestaRAG)


if __name__ == "__main__":
    print(parser.get_format_instructions())

    texto_falso = '{"respuesta": "La regla Sunny 16 es un método clásico de la fotografía para calcular la exposición correcta al aire libre sin utilizar un fotómetro.", "referencias": ["01_fundamentos_camara_analogica.txt"]}'
    resultado = parser.parse(texto_falso)
    texto_roto = '{"respuesta": "Hola"}'
    parser.parse(texto_roto)

    print(resultado)
    print(resultado.respuesta)
    print(resultado.referencias)