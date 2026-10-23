# Sistema RAG local: asistente de fotografía analógica

Sistema de recuperación semántica (RAG) de punta a punta. Recibe una pregunta, busca los fragmentos relevantes en una base vectorial local (ChromaDB) y genera una respuesta usando **exclusivamente** esa información. Si la respuesta no está en los documentos, responde "No lo sé".

## Tecnologías

- Python 3.12
- LangChain (LCEL) + Gemini (`gemini-3.5-flash-lite`) para la generación
- Gemini Embeddings (`models/gemini-embedding-001`) para indexar y consultar
- ChromaDB como base vectorial persistente
- Pydantic + `PydanticOutputParser` para la salida estructurada

## Estructura del proyecto

```
.
├── data/                # Dataset de ejemplo: 4 archivos .txt sobre cámaras analógicas
├── ingesta.py           # Chunking + persistencia en ChromaDB
├── retriever.py         # Retriever (top_k = 4)
├── esquemas.py          # Modelo Pydantic de la respuesta + parser
├── prompts.py           # Prompt de veracidad + formateo del contexto
├── rag.py               # Cadena LCEL asíncrona y get_rag_response(query)
├── pruebas.py           # Pregunta con respuesta + 2 preguntas trampa
├── requirements.txt
└── README.md
```

## Instalación

Requiere Python 3.12.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Creá un archivo `.env` en la raíz del proyecto con tu clave de Gemini:

```
GOOGLE_API_KEY=tu_clave_aqui
```

## Ejecución

**1. Ingesta (opcional).** La base se crea automáticamente la primera vez que se usa el sistema. Para forzarla:

```powershell
python ingesta.py
```

Si la carpeta `vectorstore/` ya tiene contenido, no se vuelve a indexar. Para reindexar desde cero, borrá esa carpeta.

**2. Una consulta:**

```powershell
python rag.py
```

**3. Pruebas (pregunta normal + trampas):**

```powershell
python pruebas.py
```

**Uso desde otro script:**

```python
import asyncio
from rag import get_rag_response

resultado = asyncio.run(get_rag_response("¿Qué es la regla Sunny 16?"))
print(resultado.respuesta)
print(resultado.referencias)
```

## Cómo funciona

1. **Ingesta:** se leen los `.txt` de `data/` y se fragmentan con `RecursiveCharacterTextSplitter` medido en tokens (`chunk_size=500`, `chunk_overlap=50`). Cada chunk conserva en su metadata el nombre del archivo de origen.
2. **Indexación:** los chunks se guardan en una colección de ChromaDB (`camaras`) dentro de `./vectorstore`. El mismo modelo de embeddings se usa para indexar y para consultar.
3. **Recuperación:** la pregunta se convierte en embedding y se recuperan los 4 fragmentos más cercanos.
4. **Generación grounded:** una cadena LCEL (`retriever → prompt → LLM → parser`) arma el prompt con los fragmentos, cada uno marcado con su `[Fuente: archivo]`. El prompt de sistema obliga al modelo a usar solo el contexto y a responder "No lo sé" con referencias vacías si la respuesta no está.
5. **Salida estructurada:** `PydanticOutputParser` valida la respuesta contra el modelo `RespuestaRAG`, con los campos `respuesta` (texto) y `referencias` (lista de archivos usados).

## Resultados de las pruebas

| Tipo | Pregunta | Respuesta | Referencias |
|---|---|---|---|
| En los documentos | ¿A qué temperatura se revela la película de color con el proceso C-41? | Alrededor de 38 °C | `03_peliculas_y_revelado.txt` |
| Trampa difícil (mismo tema, dato ausente) | ¿Cuánto cuesta una Leica M6 hoy? | No lo sé | `[]` |
| Trampa fácil (fuera de tema) | ¿Cuál es la capital de Francia? | No lo sé | `[]` |

En ambas preguntas trampa el modelo no inventó información ni citó archivos.