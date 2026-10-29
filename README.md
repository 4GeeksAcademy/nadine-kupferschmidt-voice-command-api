# Voice Command API at 4Geeks Academy

<!-- hide -->

By [@ehiber](https://github.com/ehiber) and [other contributors](https://github.com/4GeeksAcademy/voice-command-api/graphs/contributors) at [4Geeks Academy](https://4geeksacademy.com/)

[![build by developers](https://img.shields.io/badge/build_by-Developers-blue)](https://4geeks.com)
[![4Geeks Academy](https://img.shields.io/twitter/follow/4geeksacademy?style=social&logo=x)](https://x.com/4geeksacademy)

_Estas instrucciones tambien estan disponibles en [espanol](./README.es.md)._

**Before you start**: Read the [how to start a coding project](https://4geeks.com/lesson/how-to-start-a-project) guide before writing code.

> We need you! These exercises are built and maintained in collaboration with people like you. If you find any bug 🐞 or typo, please contribute and/or report it.

<!-- endhide -->

---

## 🎯 Your challenge

This repository is the starter template for the **Voice Command API** project.

The frontend is already built. It records up to **20 seconds** of audio in the browser, sends that audio to your backend, and shows:

- the transcription returned by the API
- the final task response returned by the API

Your job is to implement the backend so the full voice-to-action flow works end to end.

---

## How the project works

The frontend uses a single public entry point:

- `POST /transcribe`

The frontend does **not** resolve intents with the Web Speech API. It only captures audio (up to 20 seconds), sends the file to `POST /transcribe`, and shows the backend transcription to make debugging easier.

That endpoint must:

1. receive recorded audio from the frontend
2. transcribe it to text
3. reuse the same routing logic as `POST /instruction`
4. execute the corresponding task action in memory
5. return the transcription, the instruction payload, and the final result

Your backend must also expose:

- `POST /instruction`
- `GET /tasks`
- `POST /tasks`
- `PUT /tasks/{task_id}`
- `PATCH /tasks/{task_id}`
- `DELETE /tasks/{task_id}`

Important:

- Use **in-memory storage only**. No database and no files.
- The frontend is provided and should not be modified as part of the exercise.
- The backend included in this repository is only a template. You must implement the missing logic.

---

## Repository structure

```text
voice-command-api/
|-- .devcontainer/           # Codespaces setup
|-- frontend/                # Ready-made frontend
|   |-- public/
|   `-- src/
|-- src/
|   `-- app/
|       |-- api/routes/      # /transcribe, /instruction, /tasks
|       |-- core/            # Settings and config
|       |-- schemas/         # Request and response contracts
|       |-- services/        # Your implementation goes here
|       `-- utils/
|-- pyproject.toml
|-- README.md
`-- README.es.md
```

---

## 🌱 How to start the project

You can open this project in [GitHub Codespaces](https://codespaces.new/4GeeksAcademy/voice-command-api) or clone it locally.

If you use Codespaces, the repository already includes a `.devcontainer` prepared for Python, Node, FastAPI, and Vite.

### Option A: GitHub Codespaces

1. Open the repository in Codespaces.
2. Wait for the dev container to finish installing dependencies.
3. Create `.env` from `.env.example`.
4. Create `frontend/.env` from `frontend/.env.example`.
5. Run the backend and frontend from the terminal tabs.

### Option B: Local setup

```bash
git clone https://github.com/4GeeksAcademy/voice-command-api
cd voice-command-api
```

Create your own repository and update the remote:

```bash
git remote set-url origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY
```

### Backend setup

Create a `.env` file from `.env.example` and fill in your Groq credentials.

Install dependencies and run the API:

```bash
uv sync
uv run uvicorn src.main:app --reload
```

### Frontend setup

Create `frontend/.env` from `frontend/.env.example`.

Run the frontend:

```bash
cd frontend
npm install
npm run dev
```

---

## 💻 What you need to do

- [ ] Create a module-level `tasks` list with `id`, `title`, and `done`, using unique incremental IDs.
- [ ] Implement `GET /tasks`, `POST /tasks`, `PUT /tasks/{task_id}`, `PATCH /tasks/{task_id}`, and `DELETE /tasks/{task_id}` using in-memory state.
- [ ] Implement `POST /instruction` to receive `{ "transcription": "..." }`, call Groq, and return **only** routing JSON (no task execution):

```json
{
  "endpoint": "/tasks",
  "method": "POST",
  "params": { "title": "Buy groceries" }
}
```

- [ ] Implement `POST /transcribe` to accept `multipart/form-data`, convert audio to text, reuse `/instruction` logic, execute the selected action, and return `transcription`, `instruction`, and `result`.
- [ ] Do not hardcode intent matching with manual rules such as `if "add" in text`.

⚠️ **IMPORTANT:** The frontend does not resolve intents with Web Speech API. It only captures audio (up to 20 seconds), sends it to `POST /transcribe`, and shows backend transcription to debug STT vs. routing issues.

```json
{
  "transcription": "add buy groceries to my list",
  "instruction": {
    "endpoint": "/tasks",
    "method": "POST",
    "params": {
      "title": "Buy groceries"
    }
  },
  "result": {
    "id": 1,
    "title": "Buy groceries",
    "done": false
  }
}
```

---

## Debugging tip

If the transcription shown in the frontend is already wrong, the problem is in the audio capture or speech-to-text step.

If the transcription is correct but the action is wrong, the problem is in `/instruction`.

---

## ✅ What we will evaluate

- [ ] `POST /transcribe` accepts audio, transcribes it, and reuses `/instruction` routing logic.
- [ ] `POST /instruction` receives plain text and returns only routing JSON (no action execution).
- [ ] `GET /tasks`, `POST /tasks`, `PUT /tasks/{task_id}`, `PATCH /tasks/{task_id}`, and `DELETE /tasks/{task_id}` work correctly with in-memory state.
- [ ] The frontend displays the transcription returned by the backend to help distinguish STT errors from routing errors.

---

## 📦 How to submit this project

1. Push your solution to your GitHub repository.
2. Make sure backend and frontend are included and runnable locally.
3. Share the repository URL and a short video/GIF showing:
   - audio recording (20 seconds max),
   - transcription visible in the frontend,
   - correct task action execution.

---

This and many other projects are built by students as part of the [Coding Bootcamps](https://4geeksacademy.com/) at 4Geeks Academy. Learn more about the [Full-Stack Software Developer](https://4geeksacademy.com/en/career-programs/full-stack), [Data Science & Machine Learning](https://4geeksacademy.com/en/career-programs/data-science-ml), [Cybersecurity](https://4geeksacademy.com/en/career-programs/cybersecurity), and [AI Engineering](https://4geeksacademy.com/en/career-programs/ai-engineering) programs.

## Mi implementación

### 1. Cómo ejecutarlo

Desde la raíz del proyecto, instala las dependencias del backend y copia el archivo de ejemplo:

```bash
uv sync
cp .env.example .env
```

Completa `GROQ_API_KEY` en `.env` con tu propia clave de Groq y configura `GROQ_MODEL=openai/gpt-oss-20b`.

Arranca el backend:

```bash
uv run uvicorn src.main:app --reload
```

En otra terminal, prepara el frontend la primera vez:

```bash
cd frontend
npm install
cp .env.example .env
```

Configura `VITE_API_BASE_URL` en `frontend/.env` con la URL del backend. Para arrancar el frontend desde la raíz del proyecto:

```bash
cd frontend && npm run dev
```

### 2. Variables de entorno

El backend lee estas variables de `.env`, que se prepara a partir de `.env.example`:

- `GROQ_API_KEY`: clave para acceder a Groq, tanto para transcribir el audio como para generar la instrucción. Debe completarse con una clave propia y no compartirse.
- `GROQ_MODEL`: modelo que convierte el texto en una instrucción JSON. En mi implementación uso `openai/gpt-oss-20b`; hay que indicar ese valor en `.env`, porque el valor por defecto del código es otro.
- `GROQ_TRANSCRIPTION_MODEL`: modelo que convierte el audio en texto. El valor por defecto del código es `whisper-large-v3-turbo`.
- `REQUEST_TIMEOUT_SECONDS`: tiempo máximo, en segundos, para las peticiones a Groq. El valor por defecto es `45`.
- `ALLOWED_ORIGINS`: direcciones del frontend que pueden acceder al backend desde el navegador mediante CORS. Se pueden indicar varias, separadas por comas.

El frontend usa su propio archivo `frontend/.env`: `VITE_API_BASE_URL` indica la URL del backend. No debe contener la clave de Groq.

### 3. Archivos que implementé

- `src/app/api/routes/tasks.py`: implementa listar, crear, reemplazar, actualizar y eliminar tareas; las guarda en memoria, por lo que se pierden al reiniciar el backend.
- `src/app/api/routes/instruction.py`: recibe una transcripción en `POST /instruction` y devuelve la instrucción JSON del modelo, sin ejecutar la acción.
- `src/app/services/instruction_service.py`: define el system prompt, consulta el modelo de Groq y convierte su respuesta JSON en un diccionario.
- `src/app/api/routes/transcribe.py`: recibe audio o texto, transcribe el audio con Groq cuando corresponde, reutiliza el servicio de instrucciones, valida el JSON y ejecuta la acción sobre las tareas.

### 4. Cómo funciona el system prompt

El system prompt pide un formato exacto con `endpoint`, `method` y `params`, sin explicaciones ni Markdown. Así el backend puede leer y validar la respuesta como JSON.

Incluye la lista de acciones disponibles: `GET /tasks`, `POST /tasks`, `PUT /tasks/{id}`, `PATCH /tasks/{id}` y `DELETE /tasks/{id}`. También define reglas: el identificador va en la ruta, el método va en mayúsculas, los parámetros vacíos se representan con `{}` y los títulos no deben incluir las palabras usadas para dar la orden.

Los ejemplos muestran cómo convertir frases en español e inglés en ese formato. Se usa `temperature=0` para reducir la variación de las respuestas y favorecer un resultado consistente; esto no garantiza que todas las respuestas sean correctas, por eso también se validan.

No hay detección de intención en Python. El modelo decide qué acción representa la frase. El bloque `if/elif` de `transcribe.py` solo selecciona y ejecuta la operación indicada por el JSON validado; no busca palabras en la transcripción para decidir la intención.

### 5. Manejo de errores

- Se devuelve `404` cuando se intenta reemplazar, actualizar o eliminar una tarea que no existe.
- Se devuelve `502` si Groq devuelve JSON inválido o una instrucción no soportada. En el flujo de `/transcribe` también se comprueban la estructura de la instrucción y los parámetros antes de ejecutar la acción.

### 6. Notas para Codespaces

El puerto `8000` del backend debe estar marcado como **público** en la pestaña de puertos de Codespaces.

En `frontend/.env`, configura `VITE_API_BASE_URL` con la URL HTTPS que Codespaces asigna al puerto `8000`, sin añadir `/transcribe` ni otras rutas.

En el `.env` del backend, agrega la URL HTTPS del puerto `5173` a `ALLOWED_ORIGINS`. Debe ser el origen completo del frontend, sin rutas ni barra final; si mantienes otros orígenes, sepáralos por comas.

Reinicia el backend y el frontend después de cambiar sus variables de entorno.
