import json

from fastapi import HTTPException
from groq import Groq

from src.app.core.config import get_settings

SYSTEM_PROMPT = """
Eres un traductor de comandos de voz a peticiones HTTP para una API de lista de tareas.
Recibirás una frase hablada por el usuario, en español o en inglés.
Responde ÚNICAMENTE con un objeto JSON válido, sin texto antes ni después, sin explicaciones y sin bloques de código markdown.

Formato exacto:
{"endpoint": "<ruta>", "method": "<GET|POST|PUT|PATCH|DELETE>", "params": { ... }}

Endpoints disponibles:
- GET /tasks → ver todas las tareas. params: {}
- POST /tasks → crear una tarea. params: {"title": "<texto>"}
- PUT /tasks/{id} → reemplazar una tarea completa. params: {"title": "<texto>", "done": <true|false>}
- PATCH /tasks/{id} → marcar como hecha o cambiar el título. params: solo los campos que cambian
- DELETE /tasks/{id} → eliminar una tarea. params: {}

Reglas:
- Si la frase no tiene relación con la lista de tareas, responde exactamente: {"endpoint": "unsupported", "method": "NONE", "params": {}}
- El número de la tarea va dentro de "endpoint" (ejemplo: "/tasks/3"), nunca dentro de "params".
- "method" siempre en mayúsculas.
- Si no hay parámetros, usa "params": {}.
- El título se escribe limpio, sin palabras como "añade" o "a mi lista".

Ejemplos:
"añade comprar leche a mi lista" → {"endpoint": "/tasks", "method": "POST", "params": {"title": "Comprar leche"}}
"muéstrame mis tareas" → {"endpoint": "/tasks", "method": "GET", "params": {}}
"marca la tarea 2 como hecha" → {"endpoint": "/tasks/2", "method": "PATCH", "params": {"done": true}}
"cambia la tarea 3 a llamar al dentista" → {"endpoint": "/tasks/3", "method": "PATCH", "params": {"title": "Llamar al dentista"}}
"elimina la tarea 1" → {"endpoint": "/tasks/1", "method": "DELETE", "params": {}}
"delete task 4" → {"endpoint": "/tasks/4", "method": "DELETE", "params": {}}
"¿cuál es la capital de Colombia?" → {"endpoint": "unsupported", "method": "NONE", "params": {}}
"""


def get_instruction(transcription: str) -> dict:
    settings = get_settings()
    client = Groq(
        api_key=settings.groq_api_key,
        timeout=settings.request_timeout_seconds,
    )
    response = client.chat.completions.create(
        model=settings.groq_model,
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": transcription},
        ],
    )
    try:
        return json.loads(response.choices[0].message.content or "")
    except json.JSONDecodeError as error:
        raise HTTPException(
            status_code=502,
            detail="Groq returned invalid JSON for the instruction",
        ) from error