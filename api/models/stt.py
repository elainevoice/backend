import io
import shutil
from datetime import datetime

import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
from api.config import default_fs, default_length_recording, lang


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

    def recognize_wav(self, spooled_temp_file):
        recognizer = sr.Recognizer()
        try:
            with sr.WavFile(spooled_temp_file) as audio_data:
                audio = recognizer.record(audio_data)
        except Exception as e:
            raise e
        return self._recognize_audio(recognizer, audio)




class sttAdapter:
    def __init__(self):
        self.stt = _SpeechToText()

    def recognize_audio_memory(self, spooled_temp_file):
        try:
            text = self.stt.recognize_wav(spooled_temp_file)
        except Exception as e:
            raise Exception(e)
        finally:
            spooled_temp_file.close()
        return text

    # Linelenght 135 yikes
    def recognize_audio_disk(self, spooled_temp_file, file_name=f'recording_{str(datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))}.wav'):
        try:
            destination = f"./assets/data/results/{filename}"
            with open(destination, 'wb+') as file:
                # Kon nergens goed vinden hoe memory intensive dit is, dus misschien moet dit in chunks maar idk
                file.write(spooled_temp_file.read())
                text = self.stt.recognize_wav(destination)
        except Exception as e:
            print(e)
        finally:
            spooled_temp_file.close()
            file.close()
        print(text)
        return destination, text
