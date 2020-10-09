import glob
import os
import pathlib
import sounddevice as sd
import soundfile as sf

class AudioPlayer:
    def _find_last_modified_result(self):
        return max(
            glob.iglob(R"./src/assets/data/results/*.wav"), key=os.path.getmtime
        )
    
    def play_wav(self, wav = None):
        try:
            wav = self._find_last_modified_result() if wav is None else wav
            data, fs = sf.read(wav, dtype='float32')
            sd.play(data, fs)
            status = sd.wait()
        except Exception as e:
            raise e
