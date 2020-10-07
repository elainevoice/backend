import speech_recognition as sr
import sounddevice as sd
import soundfile as sf
import pathlib
import glob
import os
from datetime import datetime, timedelta


class SpeechToText:
    # def __init__(self):
    def find_last_modified_recording(self):
        return max(
            glob.iglob(R"./src/assets/data/recordings/*.wav"), key=os.path.getmtime
        )

    def classify_wav(self, path=None):
        if path is None:
            path = self.find_last_modified_recording()

        r = sr.Recognizer()
        try:
            with sr.WavFile(path) as source:
                audio = r.record(source)
        except Exception as e:
            raise e

        try:
            txt = r.recognize_google(audio, None, "nl_NL")
            print(f"You said: {txt}")
            return txt
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return None
        except sr.RequestError as e:
            print(
                "Could not request results from Google Speech Recognition service; {0}".format(
                    e
                )
            )
            return None

    # fs = 44100 - 48000
    # seconds = 10
    def record_wav(
        self,
        fs=44100,
        second=10,
        filename=f'recording_{str(datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))}.wav',
    ):
        # get input and output devices
        devices = sd.query_devices()
        input_d, output_d = sd.default.device
        print(f"devices: {devices}")

        # give user the possibility to change settings
        while True:
            print(f"input: {devices[input_d]['name']}")
            corr = input("input correct? (y/n)")
            if corr == "y":
                break
            else:
                input_d = int(input("correct number?"))

        # set new output and input devices
        sd.default.device = input_d

        # recording
        record_voice = sd.rec(int(second * fs), samplerate=fs, channels=2)
        sd.wait()
        sf.write(f"./src/assets/data/recordings/{filename}", record_voice, fs)

    def record_and_classify(self):
        self.record_wav()
        self.classify_wav()


stt = SpeechToText()
stt.classify_wav()
# stt.classify_wav()
