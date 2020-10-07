import pathlib
from pydub import AudioSegment


class Utils:
    @staticmethod
    def mp3_to_wav():
        for path in pathlib.Path("../assets/data/sounds_mp3/sentences").iterdir():
            sound = AudioSegment.from_mp3(path)
            dest = f"../assets/data/sounds_wav/sentences/{path.stem}.wav"
            sound.export(dest, format="wav")

        for path in pathlib.Path("../assets/data/sounds_mp3/words").iterdir():
            sound = AudioSegment.from_mp3(path)
            dest = f"../assets/data/sounds_wav/words/{path.stem}.wav"
            sound.export(dest, format="wav")
