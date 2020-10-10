import io
import os
from datetime import datetime

import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
from app.config import default_fs, default_length_recording, lang


class _SpeechToText:
    def _recognize_audio(self, recognizer, audio):
        try:
            txt = recognizer.recognize_google(audio, None, lang)
            return txt
        except sr.UnknownValueError:
            raise ValueError(
                "Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            raise Exception(
                f"Could not request results from Google Speech Recognition service: {e}")

    def recognize_wav(self, audio_data):
        recognizer = sr.Recognizer()
        try:
            with sr.WavFile(audio_data) as source:
                audio = recognizer.record(source)
        except Exception as e:
            raise e
        return self._recognize_audio(recognizer, audio)

    def _record_and_save_wav(self, fs=default_fs, second=default_length_recording, filename=f'recording_{str(datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))}.wav',):
        save_path = f"./src/assets/data/recordings/{filename}"
        record_voice = sd.rec(int(second * fs), samplerate=fs, channels=2)
        sd.wait()
        sf.write(save_path, record_voice, fs)
        print(f"Saved at: {save_path}")

    def record_and_recognize_wav(self):
        self._record_and_save_wav()
        self.recognize_wav()


class sttAdapter:
    def __init__(self):
        self.stt = _SpeechToText()

    def _recognize_wav(self, audio_data):
        return self.stt.recognize_wav(audio_data
                                      )

    def recognize_audio_memory(self, binary_audio):
        try:
            buffer = io.BytesIO(binary_audio)
            buffer.seek(0)
            text = self._recognize_wav(buffer)
        except Exception as e:
            raise Exception(
                "Something went wrong trying to recognize audio file from memory")
        finally:
            buffer.close()
        return text

    def recognize_audio_disk(self, binary_audio, file_name=f'recording_{str(datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))}.wav'):
        try:
            with open(f".\src\\assets\data\\recordings\\{file_name}", 'wb+') as file:
                file.write(binary_audio)
            text = self._recognize_wav(file.name)
        except Exception as e:
            print(e)
        finally:
            file.close()
        return text
