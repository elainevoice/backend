from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import (FileResponse, HTMLResponse, JSONResponse,
                               PlainTextResponse)

from app import app, controller
from app.config import application_name

router = APIRouter()
# Todo in memory file obje2ct!


@router.get("/", response_class=HTMLResponse)
def home():
    return f"<body><h1>API of {application_name}</h1></body>"


@router.post('/recognize_audio_disk')
def post_recording_disk(file: UploadFile = File(...), response_class=JSONResponse):
    try:
        spooled_temp_file = file.file
        path_name, text = controller.stt_recognize_binary_audio_on_disk(
            spooled_temp_file)
        return {
            "path": path_name,
            "text": text,
        }
    # To do  test what exceptions to actually catch
    except Exception as e:
        print(e)
        raise HTTPException(status_code=418,
                            detail="Something went wrong")

# Niet helemaal in memory want als UploadFile te groot is wordt het op schijf opgeslagen, zie https://fastapi.tiangolo.com/tutorial/request-files/
@router.post('/recognize_audio_memory')
def post_recording_memory(file: UploadFile = File(...), response_class=PlainTextResponse):
    try:
        spooled_temp_file = file.file
        text = controller.stt_recognize_binary_audio_in_memory(
            spooled_temp_file)
        return text
    # To do  test what exceptions to actually catch
    except Exception as e:
        raise HTTPException(status_code=418, detail=str(e))


@router.get('/create_audio')
def create_audio_from_text(text: str, response_class=FileResponse):
    try:
        audio_path = controller.tts_create_audio_from_text(text)

        return FileResponse(audio_path)
    # To do  test what exceptions to actually catch
    except Exception as e:
        print(e)
        raise HTTPException(status_code=418, detail=str(e))
