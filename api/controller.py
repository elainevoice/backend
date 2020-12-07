from api.models.stt import SttAdapter
from api.models.taco_adapter import TacoTronAdapter
from api.models.tts import TtsAdapter


async def stt_recognize_binary_audio_on_disk(spooled_temp_file):
    stt_adapter = SttAdapter()
    path_name, text = await stt_adapter.recognize_audio_disk(spooled_temp_file)
    return path_name, text


async def stt_recognize_binary_audio_in_memory(spooled_temp_file):
    stt_adapter = SttAdapter()
    return await stt_adapter.recognize_audio_memory(spooled_temp_file)


def tts_create_audio_from_text(text):
    tts_adapter = TtsAdapter()
    audio_path = tts_adapter.create_wav(text)
    return audio_path


def text_to_tacotron_audio_file(text):
    tta = TacoTronAdapter()
    absolute_file_path = tta.generate_wav(text)
    return absolute_file_path
