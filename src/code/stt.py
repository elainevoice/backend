import speech_recognition as sr
import sounddevice as sd
import soundfile as sf
from datetime import datetime


class SpeechToText:
    def __init__(self, path):
        self.path = path

    def classify_wav(self, path):
        r = sr.Recognizer()
        try:
            with sr.WavFile(path) as source:
                audio = r.record(source)
        except Exception as e:
            raise e

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

    def record_wav(self):
        # get input and output devices
        devices = sd.query_devices()
        input_d, output_d = sd.default.device
        input_device = devices[input_d]['name']
        output_device = devices[output_d]['name']

        print(f'devices: {devices}')
        print(f'input: {input_device}, output: {output_device}')

        # give user the possibility to change settings
        while True:
            corr = input('Setting correct? (y/n)')
            if corr == 'y':
                break
            else:
                put = input('input or output? (i/o)')
                num = input('correct number?')
                if put == 'i':
                    input_d = int(num)
                elif put == 'o':
                    output_d = int(num)
                else:
                    print('incorrect try again')

        # set new output and input devices
        print(output_d, input_d, type(output_d), type(input_d))
        sd.default.device = input_d, output_d

        # recording
        fs = 44100
        second = 10
        record_voice = sd.rec(int(second * fs), samplerate=fs, channels=2)
        sd.wait()
        sf.write(self.path, record_voice, fs)

    def record_and_classify(self):
        self.record_wav()
        self.classify_wav(self.path)


#filename = f'recording_{str(datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))}.wav'
filename = 'recording_06-10-2020_19-38-33.wav'
filelocation = f'../assets/data/recordings/{filename}'

stt = SpeechToText(filelocation)
stt.classify_wav(filelocation)