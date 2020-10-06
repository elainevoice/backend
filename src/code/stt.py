import speech_recognition as sr


class SpeechToText:

    @staticmethod
    def classify_wav(path):
        r = sr.Recognizer()
        try:
            with sr.WavFile(path) as source:
                audio = r.record(source)
        except Exception as e:
            print(e)

        try:
            global txt
            txt = r.recognize_google(audio, None, "nl_NL")
            print(f"You said: {txt}")
            return txt
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return None
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return None


SpeechToText.classify_wav('../assets/record.wav')
