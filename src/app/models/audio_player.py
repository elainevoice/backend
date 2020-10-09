import glob
import os
import pyglet
import sounddevice as sd
import soundfile as sf

class AudioPlayer:
    count = 0
    def _find_last_modified_result(self):
        return max(glob.iglob(R"./src/assets/data/results/*.wav"), key=os.path.getmtime)
    
    def play_wav(self, wav = None):
        try:
            wav = self._find_last_modified_result() if wav is None else wav
            data, fs = sf.read(wav, dtype='float32')
            sd.play(data, fs)
            status = sd.wait()
        except Exception as e:
            m = pyglet.media.load(wav)
            m.play()
