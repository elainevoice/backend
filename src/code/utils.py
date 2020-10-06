import pathlib
from os import path
from pydub import AudioSegment


class Utils:

    @staticmethod
    def mp3_to_wav():
        for path in pathlib.Path("../assets/data/sounds_mp3/sentences").iterdir():
            sound = AudioSegment.from_mp3(path)
            filename = str(path).split('\\')[-1].split('.')[0]
            dest = f"../assets/data/sounds_wav/sentences/{filename}.wav"
            sound.export(dest, format="wav")

        for path in pathlib.Path("../assets/data/sounds_mp3/words").iterdir():
            sound = AudioSegment.from_mp3(path)
            filename = str(path).split('\\')[-1].split('.')[0]
            dest = f"../assets/data/sounds_wav/words/{filename}.wav"
            sound.export(dest, format="wav")