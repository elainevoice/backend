from gtts import gTTS
from config import lang

text = str(input("What do you want to tts? "))

tts = gTTS(text=text, lang=lang)
tts.save(f'tts_{str(datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))}.wav')