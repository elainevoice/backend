import glob
import os
import pathlib
from datetime import datetime, timedelta

import sounddevice as sd
import soundfile as sf
import speech_recognition as sr

default_fs = 44100
default_length_recording = 10

class SpeechToText:
    def _find_last_modified_recording(self):
        return max(
            glob.iglob(R"./src/assets/data/recordings/*.wav"), key=os.path.getmtime
        )

    def _select_input_device(self):
        devices = sd.query_devices()
        input_d, _ = sd.default.device

        print(f"devices: {devices}")
        corr = "n"
        while corr == "n":
            input_d = int(input("Input correct input: "))
            print(f"input: {devices[input_d]['name']}")
            corr = input("input correct? (y/n) ")
        sd.default.device = input_d

    def classify_wav(self, path=None):
        path = self._find_last_modified_recording() if path is None else path

        recognizer = sr.Recognizer()
        try:
            with sr.WavFile(path) as source:
                audio = recognizer.record(source)
        except Exception as e:
            raise e

        try:
            txt = recognizer.recognize_google(audio, None, "nl_NL")
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

        self._select_input_device()

        save_path = f"./src/assets/data/recordings/{filename}"
        record_voice = sd.rec(int(second * fs), samplerate=fs, channels=2)
        sd.wait()
        sf.write(save_path, record_voice, fs)
        print(f"Saved at: {save_path}")

    def record_and_classify(self):
        self.record_and_save_wav()
        self.classify_wav()


stt = SpeechToText()
stt.classify_wav()
