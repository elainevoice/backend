import glob
import os
import pathlib
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
from datetime import datetime, timedelta
from config import lang, default_fs, default_length_recording

class SpeechToText:
    def _find_last_modified_recording(self):
        return max(
            glob.iglob(R"./src/assets/data/recordings/*.wav"), key=os.path.getmtime
        )

    def classify_wav(self, path=None):
        path = self._find_last_modified_recording() if path is None else path

        recognizer = sr.Recognizer()
        try:
            with sr.WavFile(path) as source:
                audio = recognizer.record(source)
        except Exception as e:
            raise e

        try:
            txt = recognizer.recognize_google(audio, None, lang)
            print(f"You said: {txt}")
            return txt
        except sr.UnknownValueError:
            raise ValueError("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            raise Exception(
                f"Could not request results from Google Speech Recognition service: {e}"
            )

    def record_and_save_wav(
        self,
        fs=default_fs,
        second=default_length_recording,
        filename=f'recording_{str(datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))}.wav',
    ):

        save_path = f"./src/assets/data/recordings/{filename}"
        record_voice = sd.rec(int(second * fs), samplerate=fs, channels=2)
        sd.wait()
        sf.write(save_path, record_voice, fs)
        print(f"Saved at: {save_path}")

    def record_and_classify(self):
        self.record_and_save_wav()
        self.classify_wav()

