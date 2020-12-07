from datetime import datetime
import speech_recognition as sr
from api.config import lang


class _SpeechToText:
    @staticmethod
    def _recognize_audio(recognizer, audio):
        try:
            return recognizer.recognize_google(audio, None, lang)
        except sr.UnknownValueError:
            raise ValueError(
                "Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            raise Exception(
                f"Could not request results from Google Speech Recognition service: {e}")

    async def recognize_wav(self, spooled_temp_file):
        recognizer = sr.Recognizer()
        print('a)')
        try:
            with sr.WavFile(spooled_temp_file) as audio_data:
                audio = recognizer.record(audio_data)
        except Exception as e:
            print('Exception in rec wav')
            print(e)
            raise e
        return self._recognize_audio(recognizer, audio)


class SttAdapter:
    def __init__(self):
        self.stt = _SpeechToText()

    async def recognize_audio_memory(self, path):
        try:
            text = await self.stt.recognize_wav(path)
            print(f'aaa{text}')
        except Exception as e:
            raise Exception(e)
        return text

    async def recognize_audio_disk(self, spooled_temp_file,
                                   file_name=f'recording_{str(datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))}.wav'):
        try:
            destination = f"./assets/data/results/{file_name}"
            with open(destination, 'wb+') as file:
                # Kon nergens goed vinden hoe memory intensive dit is, dus misschien moet dit in chunks maar idk
                file.write(spooled_temp_file.read())
                print(spooled_temp_file.read())
                text = await self.stt.recognize_wav(file)
        except Exception as e:
            print(e)
        finally:
            spooled_temp_file.close()
            file.close()
        return destination, text
