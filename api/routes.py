from fastapi import APIRouter, File, Header, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from pydantic.main import List

from api import controller
from api.config import application_name
from api.models.TTS_model import TTSModel

router = APIRouter()

MAX_CHARACTERS = 550

class NotVIPplsPAYError(Exception):
    pass


@router.get("/", response_class=HTMLResponse)
def home():
    return f"<body><h1>API of {application_name}</h1></body>"


@router.post("/taco")
def text_to_tacotron_audio_file(data: TTSModel, model=Header(None)):
    try:
        text = data.text
        if len(text) > MAX_CHARACTERS:
            raise NotVIPplsPAYError(
                "Too many chararacters."
            )
        wav_audio_file_path = controller.text_to_tacotron_audio_file(data.text, model)
        return FileResponse(str(wav_audio_file_path))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/taco_audio")
async def audio_to_tacotron_audio_file(
    file: UploadFile = File(...), model=Header(None)
):
    try:
        bytes = await file.read()
        if len(bytes) < 1:
            raise NotImplementedError(
                "No audio has been provided, check your microphone."
            )
        if len(bytes) > 120000:
            raise NotVIPplsPAYError(
                "Too many bytes."
            )

        wav_audio_file_path, text = await controller.audio_to_tacotron_audio_file(
            bytes, model
        )

        return FileResponse(str(wav_audio_file_path), headers={'text': text})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get_models", response_model=List[str])
def get_available_models():
    try:
        return controller.get_models()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
