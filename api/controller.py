import os
import uuid

from api import helpers
from api.models.ffmpeg_adapter import FfmpegAdapter
from api.models.stt import SttAdapter
from api.models.taco_adapter import TacoTronAdapter


def text_to_tacotron_audio_file(text, model):
    tta = TacoTronAdapter()
    absolute_file_path = tta.generate_wav(text, model)
    return absolute_file_path


def get_models():
    return helpers.get_taco_models()


async def audio_to_tacotron_audio_file(bytes, model):
    unique_filename = str(uuid.uuid4())
    path = "temp/" + unique_filename + ".webm"
    new_path = "temp/" + unique_filename + ".wav"

    fa = FfmpegAdapter(bytes, path, new_path)
    fa.run()

    stt_adapter = SttAdapter()
    text = await stt_adapter.recognize_audio_memory(new_path)

    tta = TacoTronAdapter()
    wav_audio_file_path = tta.generate_wav(text, model)

    os.remove(path)
    os.remove(new_path)

    return wav_audio_file_path, text
