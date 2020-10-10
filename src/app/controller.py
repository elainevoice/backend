from app.models.stt import sttAdapter
from app.models.tts import ttsAdapter


def stt_recognize_binary_audio_on_disk(binary_audio):
    stt_adapter = sttAdapter()
    return stt_adapter.recognize_audio_disk(binary_audio)


def stt_recognize_binary_audio_in_memory(binary_audio):
    stt_adapter = sttAdapter()
    return stt_adapter.recognize_audio_memory(binary_audio)


def tts_create_audio_from_text(text):
    tts_adapter = ttsAdapter()
    audio_path = tts_adapter.create_wav(text)
    return audio_path
