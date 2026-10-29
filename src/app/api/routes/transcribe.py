import re

from fastapi import APIRouter, HTTPException, Request
from groq import AsyncGroq, GroqError
from pydantic import ValidationError
from starlette.concurrency import run_in_threadpool
from starlette.datastructures import UploadFile

from src.app.api.routes.tasks import (
    create_task,
    delete_task,
    get_tasks,
    replace_task,
    update_task,
)
from src.app.core.config import get_settings
from src.app.schemas.voice import (
    InstructionPayload,
    InstructionRequest,
    TaskCreate,
    TaskReplace,
    TaskUpdate,
    TranscribeFlowResponse,
)
from src.app.services.instruction_service import get_instruction
from src.app.utils.language import normalize_transcription_language

router = APIRouter(tags=["transcribe"])


@router.get("/")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/transcribe", response_model=TranscribeFlowResponse)
async def transcribe_and_run_flow(request: Request) -> TranscribeFlowResponse:
    content_type = request.headers.get("content-type", "").split(";", 1)[0].strip().lower()

    if content_type == "application/json":
        try:
            payload = InstructionRequest.model_validate(await request.json())
        except (ValueError, ValidationError) as error:
            raise HTTPException(
                status_code=400,
                detail="Expected JSON with a non-empty 'transcription' string.",
            ) from error
        transcription = payload.transcription.strip()
    elif content_type == "multipart/form-data":
        async with request.form() as form:
            audio_file = form.get("file")
            if not isinstance(audio_file, UploadFile):
                raise HTTPException(status_code=400, detail="Missing audio file in 'file'.")
            language = normalize_transcription_language(form.get("language"))
            audio = await audio_file.read()
            if not audio:
                raise HTTPException(status_code=400, detail="The audio file is empty.")
            filename = audio_file.filename or "audio.webm"
            audio_content_type = audio_file.content_type or "application/octet-stream"

        settings = get_settings()
        try:
            async with AsyncGroq(
                api_key=settings.groq_api_key,
                timeout=settings.request_timeout_seconds,
            ) as client:
                response = await client.audio.transcriptions.create(
                    file=(filename, audio, audio_content_type),
                    model=settings.groq_transcription_model,
                    response_format="json",
                    **({"language": language} if language else {}),
                )
        except GroqError as error:
            raise HTTPException(
                status_code=502,
                detail="Groq could not transcribe the audio.",
            ) from error
        transcription = response.text.strip()
        if not transcription:
            raise HTTPException(status_code=502, detail="Groq returned an empty transcription.")
    else:
        raise HTTPException(
            status_code=415,
            detail="Use application/json or multipart/form-data.",
        )

    if not transcription:
        raise HTTPException(status_code=400, detail="The transcription must not be blank.")

    try:
        raw_instruction = await run_in_threadpool(get_instruction, transcription)
    except GroqError as error:
        raise HTTPException(
            status_code=502,
            detail="Groq could not generate an instruction.",
        ) from error
    try:
        instruction = InstructionPayload.model_validate(raw_instruction)
    except ValidationError as error:
        raise HTTPException(
            status_code=502,
            detail="Groq returned an invalid instruction: expected endpoint, method and object params.",
        ) from error

    if instruction.endpoint == "unsupported":
        raise HTTPException(
            status_code=400,
            detail="Solo puedo ayudarte con tu lista de tareas. Puedes decir, por ejemplo: 'añade comprar leche', 'muéstrame mis tareas', 'marca la tarea 1 como hecha' o 'elimina la tarea 2'.",
        )

    task_match = re.fullmatch(r"/tasks/([0-9]+)", instruction.endpoint)
    try:
        if instruction.method == "GET" and instruction.endpoint == "/tasks":
            result = get_tasks()
        elif instruction.method == "POST" and instruction.endpoint == "/tasks":
            result = create_task(TaskCreate(**instruction.params))
        elif instruction.method == "PUT" and task_match:
            result = replace_task(int(task_match.group(1)), TaskReplace(**instruction.params))
        elif instruction.method == "PATCH" and task_match:
            result = update_task(int(task_match.group(1)), TaskUpdate(**instruction.params))
        elif instruction.method == "DELETE" and task_match:
            result = delete_task(int(task_match.group(1)))
        else:
            raise HTTPException(
                status_code=502,
                detail=f"Groq returned an unsupported instruction: {instruction.method} {instruction.endpoint}",
            )
    except (ValidationError, ValueError) as error:
        raise HTTPException(
            status_code=502,
            detail="Groq returned invalid task parameters or a task identifier that cannot be used.",
        ) from error

    return TranscribeFlowResponse(
        transcription=transcription,
        instruction=instruction,
        result=result,
    )
