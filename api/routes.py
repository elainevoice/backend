from fastapi import APIRouter, File, HTTPException, UploadFile, Header
from fastapi.responses import (FileResponse, HTMLResponse, JSONResponse,
                               PlainTextResponse)
from pydantic.main import List
from starlette.requests import Request

from api import controller
from api.config import application_name
from api.models.TTS_model import TTSModel

import os
import uuid
import ffmpeg

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def home():
    return f"<body><h1>API of {application_name}</h1></body>"


@router.post("/recognize_audio_disk")
async def post_recording_disk(file: UploadFile = File(...)):
    try:
        spooled_temp_file = file.file
        path_name, text = await controller.stt_recognize_binary_audio_on_disk(
            spooled_temp_file
        )
        return JSONResponse(
            {
                "path": path_name,
                "text": text,
            }
        )
    # To do  test what exceptions to actually catch
    except Exception as e:
        raise HTTPException(status_code=500, detail="Something went wrong")


# Niet helemaal in memory want als UploadFile te groot is wordt het op schijf opgeslagen, zie https://fastapi.tiangolo.com/tutorial/request-files/
@router.post("/recognize_audio_memory")
async def post_recording_memory(file: UploadFile = File(...)):
    try:
        spooled_temp_file = file.file
        text = await controller.stt_recognize_binary_audio_in_memory(spooled_temp_file)
        return PlainTextResponse(text)
    # To do  test what exceptions to actually catch
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create_audio")
def create_audio_from_text(text: str):
    try:
        audio_path = controller.tts_create_audio_from_text(text)
        return FileResponse(audio_path)
    # To do  test what exceptions to actually catch
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/crack_create_audio")
def crack_create_audio_from_text(text: str, request: Request):
    try:
        audio_path = controller.tts_create_audio_from_text(text)
        return (
            str(request.url).split("/crack_create")[0]
            + "/crack_audio_oplossing?audio_name="
            + audio_path
        )
    # To do  test what exceptions to actually catch
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/crack_audio_oplossing")
def crack_audio_oplossing(audio_name: str):
    return FileResponse(audio_name)


@router.post('/taco')
def text_to_tacotron_audio_file(data: TTS_model, model = Header(None)):
    try:
        wav_audio_file_path = controller.text_to_tacotron_audio_file(data.text, model)
        return FileResponse(str(wav_audio_file_path))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/taco_audio')
async def audio_to_tacotron_audio_file(file: UploadFile = File(...), model = Header(None)):

    try:
        bytes = await file.read()
        if len(bytes) == 1:
            raise NotImplementedError(
                "We cannot provide translations of no sound, check your mic settings tyvm"
            )
        unique_filename = str(uuid.uuid4())
        path = "temp/" + unique_filename + ".webm"
        new_path = "temp/" + unique_filename + ".wav"
        with open(path, mode="wb+") as f:
            f.write(bytes)
            f.close()

        stream = ffmpeg.input(path)
        output = stream.output(new_path, format="wav")
        output.run()

        text = await controller.stt_recognize_binary_audio_in_memory(new_path)
        wav_audio_file_path = controller.text_to_tacotron_audio_file(text, model)

        os.remove(path)
        os.remove(new_path)

        return FileResponse(str(wav_audio_file_path))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/get_models', response_model=List[str])
def get_available_models():
    try:
        result = controller.get_models()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
