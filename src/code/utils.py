import pathlib
import pandas as pd
import os
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


    @staticmethod
    def rename_wav():
        words = pd.read_csv('../assets/data/words_dict_nl.csv')
        sentences = pd.read_csv('../assets/data/sentences_dict_nl.csv')

        directory = "../assets/data/sounds_wav/words"
        for filename in os.listdir(directory):
            print(filename)
            turks = filename[:-4].lower()
            match = words.loc[words['turks'] == f"sounds/words/{turks}.mp3"]
            print(match)
            nederlands = match['nederlands'].item().replace(' ', '_')

            print(nederlands)
            old_file = os.path.join(directory, filename)
            new_filename = old_file.replace(turks, nederlands)
            try:
                os.rename(old_file, new_filename)
            except:
                pass

        """
        for path in pathlib.Path("../assets/data/sounds_wav/words").iterdir():
            turks = path.stem
            ned = words[words['turks'].str.contains(turks)]
            print(ned)
        """



Utils.rename_wav()