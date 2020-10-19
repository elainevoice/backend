import glob
import os

import pyglet
import sounddevice as sd
import soundfile as sf
from helpers import find_last_modified_result


class AudioPlayer:
    count = 0
   
    def play_wav(self, wav = None):
        try:
            wav = find_last_modified_result() if wav is None else wav
            data, fs = sf.read(wav, dtype='float32')
            sd.play(data, fs)
            sd.wait()
        except Exception as e:
            m = pyglet.media.load(wav)
            m.play()
