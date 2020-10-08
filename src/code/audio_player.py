import glob
import os
import pathlib
import sounddevice as sd
import soundfile as sf

class AudioPlayer:
    def _find_last_modified_recording(self):
        return max(
            glob.iglob(R"./src/assets/data/recordings/*.wav"), key=os.path.getmtime
        )
    
    def play_wav(self, wav = None):
        wav = self._find_last_modified_recording() if wav is None else wav
        data, fs = sf.read(wav, dtype='float32')  
        sd.play(data, fs)
        status = sd.wait()