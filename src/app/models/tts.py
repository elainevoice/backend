from gtts import gTTS
from datetime import datetime
from app.config import lang


class _textToSpeech:
    def create_wav(self, text, filename=f'result_{str(datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))}.wav'):
        save_path = f"./src/assets/data/results/{filename}"
        speechResult = gTTS(text=text, lang=lang, slow=False)
        speechResult.save(save_path)
        print(f"Saved at: {save_path}")
        return save_path


class ttsAdapter:
    def __init__(self):
        self.tts = _textToSpeech()

    def create_wav(self, text):
        return self.tts.create_wav(text=text)
