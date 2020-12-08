from fastapi import APIRouter, File, HTTPException, UploadFile, Header
from fastapi.responses import (FileResponse, HTMLResponse,)
from pydantic.main import List

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


@router.post('/taco')
def text_to_tacotron_audio_file(data: TTSModel, model=Header(None)):
    try:
        wav_audio_file_path = controller.text_to_tacotron_audio_file(data.text, model)
        return FileResponse(str(wav_audio_file_path))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/taco_audio')
async def audio_to_tacotron_audio_file(file: UploadFile = File(...), model=Header(None)):
    try:
        bytes = await file.read()
        if len(bytes) == 1:
            raise NotImplementedError(
                "No audio has been provided, check your microphone."
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
        return controller.get_models()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
