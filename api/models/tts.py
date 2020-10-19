from datetime import datetime

from api.config import lang
from gtts import gTTS
import os

class _TextToSpeech:
    def create_wav(self, text, file_name=f'result_{str(datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))}.wav'):
        
        save_path = f"./assets/data/results/{file_name}"
        speechResult = gTTS(text=text, lang=lang, slow=False)
        speechResult.save(save_path)
        return save_path


class ttsAdapter:
    def __init__(self):
        self.tts = _TextToSpeech()

    def create_wav(self, text):
        return self.tts.create_wav(text=text)
