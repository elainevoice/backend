from api.models.stt import sttAdapter
from api.models.taco_adapter import TacoTronAdapter
from api.models.tts import ttsAdapter


def stt_recognize_binary_audio_on_disk(spooled_temp_file):
    stt_adapter = sttAdapter()
    path_name, text = stt_adapter.recognize_audio_disk(spooled_temp_file)
    return path_name, text


def stt_recognize_binary_audio_in_memory(spooled_temp_file):
    stt_adapter = sttAdapter()
    return stt_adapter.recognize_audio_memory(spooled_temp_file)


def tts_create_audio_from_text(text):
    tts_adapter = ttsAdapter()
    audio_path = tts_adapter.create_wav(text)
    return audio_path


def text_to_tacotron_audio_file(text):
    tta = TacoTronAdapter()
    absolute_file_path = tta.generate_wav(text)
    return absolute_file_path
    