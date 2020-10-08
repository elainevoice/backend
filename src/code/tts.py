import glob
import os
import pathlib

from gtts import gTTS
from datetime import datetime
from config import lang
from stt import SpeechToText

class textToSpeech:
    def _find_last_modified_recording(self):
        return max(
            glob.iglob(R"./src/assets/data/recordings/*.wav"), key=os.path.getmtime
        )
    
    def _classify_last_modified_wav(self):
        stt = SpeechToText()
        return stt.classify_wav()

    def create_wav(
        self,
        text = None,
        filename=f'result_{str(datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))}.wav',
    ):
        text = self._classify_last_modified_wav() if text is None else text
        save_path = f"./src/assets/data/results/{filename}"
        speechResult = gTTS(text=text, lang= lang, slow=False)
        speechResult.save(save_path)
        print(f"Saved at: {save_path}")
