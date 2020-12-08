from datetime import datetime

from api.config import lang
from gtts import gTTS


class _TextToSpeech:
    @staticmethod
    def create_wav(
        text,
        file_name=f'result_{str(datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))}.wav',
    ):

        save_path = f"./assets/data/results/{file_name}"
        speech_result = gTTS(text=text, lang=lang, slow=False)
        speech_result.save(save_path)
        return save_path


class TtsAdapter:
    def __init__(self):
        self.tts = _TextToSpeech()

    def create_wav(self, text):
        return self.tts.create_wav(text=text)
